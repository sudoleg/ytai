import logging

import streamlit as st

from modules.helpers import read_file
from modules.ui import (
    display_missing_api_key_warning,
    set_api_key_in_session_state,
)


def main():
    st.set_page_config(
        page_title="YouTube AI", layout="wide", initial_sidebar_state="auto"
    )

    # display sidebar with page links
    st.sidebar.page_link(page="pages/summary.py", label="Summary")
    st.sidebar.page_link(page="pages/chat.py", label="Chat")

    set_api_key_in_session_state()
    display_missing_api_key_warning()

    st.markdown(body=read_file(".assets/description.md"))


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level=logging.INFO,
    )
    main()
