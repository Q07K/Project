"""DataControl Module"""

from io import StringIO
from typing import Union, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from streamlit.runtime.uploaded_file_manager import UploadedFile

from Utils.Text2DataFrame import KakaoTalk2DataFrame


class DataHandler:
    '''
    DataHendler Class
    '''

    def __init__(self, data: UploadedFile, bot_used: bool):
        data = StringIO(data.getvalue().decode('utf-8'))

        not_users = ['', '채팅방 관리자']
        if bot_used:
            not_users += ['방장봇']

        self.data = KakaoTalk2DataFrame(
            path=data,
            ispath=False,
            bot_used=bot_used,
            not_user=not_users,
        )

        # Convert Pandas
        self.df = self.data.data.to_pandas()

        # Info
        self.title = self.data.title
        self.save_point = self.data.save_point
        self.start_point, self.end_point = self.__date_point()
        self.users = self.data.users.to_numpy()
        self.user_size = self.data.participants_num
        self.chat_size = self.__chat_size()
        self.chat_last = self.data.data.tail(1)['date'][0]

    def __chat_size(self) -> int:
        '''

        Returns
        -------
        chat_size: int
        '''
        chat_size = self.df['chat'].notna().sum()
        return chat_size

    def __date_point(self):
        '''

        Returns
        -------

        '''
        start_date = self.df['date'].head(1).values[0].astype(datetime)
        end_date = self.df['date'].tail(1).values[0].astype(datetime)
        return start_date, end_date

    def dod_calculator(
            self,
            target_col: str,
            target_val: Optional[Union[str, list]] = None,
            unique: bool = False,
    ) -> Union[int, str]:
        '''

        Parameters
        ----------
        target_col: str
            target colume name
        target_val: Optional, [str, list]
            target colume value
            If None get all
        unique: bool, default False

        Returns
        -------
        today_size: int
        ratio: str
        '''
        today = pd.to_datetime(self.save_point)
        today = today.date() + pd.DateOffset(days=0)
        yesterday = today - pd.DateOffset(days=1)

        today_df = self.df[self.df['date'].isin([today])]
        yesterday_df = self.df[self.df['date'].isin([yesterday])]

        # Filter
        if isinstance(target_val, str):
            today_size = today_df[target_col].isin([target_val])
            yesterday_size = yesterday_df[target_col].isin([target_val])
        elif isinstance(target_val, list):
            today_size = today_df[target_col].isin(target_val)
            yesterday_size = yesterday_df[target_col].isin(target_val)
        elif unique:
            today_size = ~ today_df.loc[
                today_df['chat'].notna(), target_col
            ].duplicated()
            yesterday_size = ~ yesterday_df.loc[
                yesterday_df['chat'].notna(), target_col
            ].duplicated()
        else:
            today_size = today_df[target_col].notna()
            yesterday_size = yesterday_df[target_col].notna()
        today_size = today_size.sum()
        yesterday_size = yesterday_size.sum()

        # DoD
        if not yesterday_size:
            result = (today_size - yesterday_size)
        elif today_size == yesterday_size:
            result = 0
        else:
            result = (today_size - yesterday_size) / yesterday_size
        ratio = f'{result:.2%}'

        return today_size, ratio

    def death_note(
            self,
            min_date,
            max_date,
            num: int,
            date_format: str,
            sort_key: str,
            ascending: bool,
    ) -> pd.DataFrame:
        min_date = pd.to_datetime(min_date, format=date_format)
        max_date = pd.to_datetime(max_date, format=date_format)
        date_range = pd.date_range(
            start=min_date,
            end=max_date,
        )
        # Filter
        result_df = self.df[
            self.df['name'].isin(self.users)
            & self.df['event'].isna()
            & self.df['date'].isin(date_range)
            ]

        # 기준일 부터 대화 0회 인원
        chat_zero_users = self.users[~np.isin(
            self.users,
            result_df['name'].unique())
        ]
        chat_zero_users = self.df[
            self.df['name'].isin(chat_zero_users)
        ].groupby('name')[['date']].max().reset_index()
        chat_zero_users['count'] = 0
        chat_zero_users = chat_zero_users.rename(
            columns={'name': '유저', 'count': '대화 빈도', 'date': '마지막 대화'}
        )

        # 기준일 부터 대화 1회 이상 인원
        result_df = result_df.groupby(['name'])[['date']].agg(
            ['count', 'max']
        ).date.reset_index()
        result_df = result_df.rename(
            columns={'name': '유저', 'count': '대화 빈도', 'max': '마지막 대화'}
        )

        # 병합 및 결과 산출
        result_df = pd.concat([result_df, chat_zero_users])
        result_df = result_df[result_df['대화 빈도'] <= num]
        result_df = result_df.sort_values(
            by='대화 빈도',
            ignore_index=True,
            ascending=False
        )

        # 유저 입장
        death_user_in = self.df[
            self.df['name'].isin(result_df['유저'])
            & self.df['event'].isin(['들어왔습니다.'])
            ]
        death_user_in = death_user_in.drop_duplicates(
            subset='name',
            keep='last'
        )
        death_user_in = death_user_in[['name', 'date']]
        death_user_in = death_user_in.rename(
            columns={'name': '유저', 'date': '입장'}
        )
        result_df = result_df.merge(death_user_in)
        result_df = result_df[['유저', '대화 빈도', '마지막 대화']]

        # 마지막 대화 기준 정렬
        result_df = result_df.sort_values(
            sort_key,
            ignore_index=True,
            ascending=ascending
        )
        result_df['마지막 대화'] = (
                self.save_point
                - result_df['마지막 대화']
        ).dt.days.apply(lambda x: f'{x:2}일 전' if x else '오늘')

        return result_df

    def rank(
            self,
            min_date,
            max_date,
            date_format: str,
            filter: str
    ):
        min_date = pd.to_datetime(min_date, format=date_format)
        max_date = pd.to_datetime(max_date, format=date_format)
        date_range = pd.date_range(
            start=min_date,
            end=max_date,
        )
        _, filter = filter.split(' ', maxsplit=1)
        # Filter
        result_df = self.df[
            self.df['name'].isin(self.users)
            & self.df['event'].isna()
            & self.df['date'].isin(date_range)
            ]

        # 기준일 부터 대화 0회 인원
        chat_zero_users = self.users[~np.isin(
            self.users,
            result_df['name'].unique())
        ]
        chat_zero_users = self.df[
            self.df['name'].isin(chat_zero_users)
        ].groupby('name')[['date']].max().reset_index()
        chat_zero_users['count'] = 0
        chat_zero_users = chat_zero_users.rename(
            columns={'name': '유저', 'count': '대화 빈도', 'date': '마지막 대화'}
        )
        # 기준일 부터 대화 1회 이상 인원
        result_df = result_df.groupby(['name'])[['date']].agg(
            ['count', 'max']).date.reset_index()
        result_df = result_df.rename(
            columns={'name': '유저', 'count': '대화 빈도', 'max': '마지막 대화'})

        # 병합 및 결과 산출
        result_df = pd.concat([result_df, chat_zero_users])
        result_df = result_df.sort_values(by='대화 빈도', ignore_index=True,
                                          ascending=False)

        # print(result_df[result_df['유저'] == '타이거(화성/⁸⁵/갤S²⁰)'])

        # 마지막 대화 기준 정렬
        result_df = result_df.sort_values('대화 빈도', ignore_index=True,
                                          ascending=False)

        result_df['마지막 대화'] = (
                    max_date - result_df['마지막 대화']).dt.days.apply(
            lambda x: f'{x:2}일 전' if x else '오늘')

        result_df = result_df.head(20)
        result_df.index += 1
        return result_df
