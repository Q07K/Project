import streamlit as st
from streamlit.delta_generator import DeltaGenerator


def dod_metric(
        field: DeltaGenerator,
        label: str,
        value: int,
        delta: str
) -> None:
    '''

    Parameters
    ----------
    field : DeltaGenerator
    label : str
    value : int
    delta : str

    Returns
    -------
    None

    '''
    if '0.00%' == delta:
        delta_color = 'off'
    else:
        delta_color = 'normal'

    field.metric(
        label=label,
        value=value,
        delta=delta,
        delta_color=delta_color,
    )


def filter_block(
        header: str,
        key: str,
        start_point,
        end_point,
        date_format: str,
        mode: str = 'frequency'

) -> None:
    st.header(header)
    col = st.columns([0.5, 0.5])
    col[0].date_input(
        '조회 기간',
        format=date_format,
        key=f'{key}_date',
        value=[],
        min_value=start_point,
        max_value=end_point,
    )
    if mode == 'frequency':
        col[1].number_input(
            '대화 빈도',
            value=0,
            min_value=0,
            key=f'{key}_num'
        )
    elif mode == 'test':
        col[1].selectbox(
            '조회 대상',
            ('📑 전체', '📸 사진', '🎬 동영상', '😆 이모티콘'),
            key=f'{key}_select',
            index=0,
            disabled=True
        )
