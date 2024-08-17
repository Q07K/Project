import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

file: UploadedFile = st.file_uploader(
    "test"
)
if file is not None:
    print(isinstance(file, UploadedFile))
    print(type(file))
    print(file.name)
    print(file.read())
