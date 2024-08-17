""" Rank Tab """

import streamlit as st

from StreamlitModules import dod_metric, filter_block

title = ':trophy: Rank'
date_format = 'YYYY-MM-DD'


def main():
    data = st.session_state['df']

    filter_block(
        header=title,
        key='rank',
        start_point=data.start_point,
        end_point=data.end_point,
        date_format=date_format,
        mode='test'
    )
    if len(st.session_state['rank_date']) == 2:
        result = data.rank(
            min_date=st.session_state['rank_date'][0],
            max_date=st.session_state['rank_date'][1],
            date_format=date_format,
            filter=st.session_state['rank_select']
        )
        st.table(result)

        top = result.head(5)