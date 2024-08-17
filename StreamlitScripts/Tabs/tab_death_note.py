""" Death Note Tab """

import streamlit as st

from StreamlitModules import dod_metric, filter_block

title = ':skull: Death Note'
date_format = 'YYYY-MM-DD'


def main():
    data = st.session_state['df']
    filter_block(
        header=':skull: Death Note',
        key='death',
        start_point=data.start_point,
        end_point=data.end_point,
        date_format=date_format,
    )

    st.write('정렬 기준')
    col = st.columns([0.5, 0.5])
    sort_key = col[0].radio(
        '정렬 기준',
        ['유저', '대화 빈도', '마지막 대화'],
        index=1,
        horizontal=True,
        label_visibility='collapsed',
    )
    ascending = col[1].toggle(
        ':red[정렬 변경]',
        value=True,
        # label_visibility='collapsed',
    )

    if len(st.session_state['death_date']) == 2:
        result = data.death_note(
            min_date=st.session_state['death_date'][0],
            max_date=st.session_state['death_date'][1],
            num=st.session_state['death_num'],
            date_format=date_format,
            sort_key=sort_key,
            ascending=ascending,
        )
        st.table(result)
