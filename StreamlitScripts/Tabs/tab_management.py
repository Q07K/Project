""" Management Tab """

import streamlit as st
import numpy as np

from StreamlitModules import dod_metric, filter_block

title = ':gear: Management'
date_format = 'YYYY-MM-DD'


def main():
    data = st.session_state['df']

    filter_block(
        header=title,
        key='test',
        start_point=data.start_point,
        end_point=data.end_point,
        date_format=date_format,
        mode='test'
    )
    if len(st.session_state['test_date']) == 2:
        result = data.rank(
            min_date=st.session_state['test_date'][0],
            max_date=st.session_state['test_date'][1],
            date_format=date_format,
            filter=st.session_state['test_select']
        )
        result.iloc[1]['유저'] = '🥇'
        medals = ['🥇', '🥈', '🥉']


        st.table(result)
