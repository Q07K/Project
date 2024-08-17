""" Home Tab """

import streamlit as st

from StreamlitModules import dod_metric

title = ':house: HOME'


def main():
    data = st.session_state['df']

    # Title
    st.header(data.title)

    # Total
    col = st.columns([0.2, 0.3, 0.5])

    # personnel
    col[0].metric(
        '인원',
        f'{data.user_size} 명',
    )
    # Chat
    col[1].metric(
        '누적 대화',
        f'{data.chat_size} 회',
    )
    # Create
    col[2].metric(
        '데이터 추출 날짜',
        f'{data.save_point}',
    )

    # DoD
    st.write('---')
    st.subheader('전일 대비')
    st.write(f'**기준: :blue-background[{data.chat_last}]**')

    col = st.columns(4)

    # Chat
    size, ratio = data.dod_calculator(
        target_col='chat',
    )
    dod_metric(
        field=col[0],
        label='대화',
        value=f'{size} 회',
        delta=ratio,
    )
    # Activate Users
    size, ratio = data.dod_calculator(
        target_col='name',
        unique=True,
    )
    dod_metric(
        field=col[1],
        label='참여자',
        value=f'{size} 명',
        delta=ratio,
    )
    # Enter
    size, ratio = data.dod_calculator(
        target_col='event',
        target_val='들어왔습니다.',
    )
    dod_metric(
        field=col[2],
        label='유입',
        value=f'{size} 명',
        delta=ratio,
    )
    # Leave
    size, ratio = data.dod_calculator(
        target_col='event',
        target_val=['나갔습니다.', '내보냈습니다.'],
    )
    dod_metric(
        field=col[3],
        label='이탈',
        value=f'{size} 명',
        delta=ratio,
    )

    # Data
    st.write('---')
    st.subheader('최근 대화 (100)')
    st.dataframe(
        data.df,
        width=2000,
        height=350,
    )
