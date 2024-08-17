import streamlit as st
from io import StringIO
from Utils import DataHandler
from StreamlitModules import dod_metric, filter_block
from StreamlitScripts import (
    tab_home,
    tab_rank,
    tab_death_note,
    tab_management,
)


def load_dataframe():
    with st.spinner():
        if st.session_state['data'] is not None:
            data = DataHandler(
                data=st.session_state['data'],
                bot_used=st.session_state['bot_used']
            )
            st.session_state['df'] = data
        else:
            del st.session_state['df']
            side_2.error('파일을 넣어주세요.')


# Side Bar Setting
side = st.sidebar
side_1 = side.container()
side_2 = side.container()
side_3 = side.container(border=True)

side_1.file_uploader(
    ' ',
    accept_multiple_files=False,
    key='data',
    label_visibility='hidden',
    # type='txt',
    on_change=load_dataframe,
)

# Settings
side_3.subheader('Settings')
side_3.toggle(
    '방장봇 사용',
    value=True,
    key='bot_used',
    on_change=load_dataframe
)

# Tab
tab = st.tabs([
    tab_home.title,
    tab_rank.title,
    tab_death_note.title,
    tab_management.title,
])
with tab[0]:
    if 'df' in st.session_state:
        tab_home.main()
with tab[1]:
    if 'df' in st.session_state:
        tab_rank.main()
with tab[2]:
    if 'df' in st.session_state:
        tab_death_note.main()

with tab[-1]:
    if 'df' in st.session_state:
        tab_management.main()
