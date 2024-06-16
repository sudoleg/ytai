from os import getenv

import streamlit as st

from modules.helpers import get_default_config_value

GENERAL_ERROR_MESSAGE = "An unexpected error occurred. If you are a developer and run the app locally, you can view the logs to see details about the error."


def is_api_key_set() -> bool:
    """Checks whether the OpenAI API key is set as environment variable and in streamlit's session state."""
    if (not getenv("OPENAI_API_KEY")) and st.session_state.openai_api_key == "":
        return False
    return True


def display_missing_api_key_warning():
    """Checks whether an API key is provided and displays warning if not."""
    if not is_api_key_set():
        st.warning(
            """:warning: It seems you haven't provided an API-Key yet. Make sure to do so by providing it in the settings (sidebar) 
            or as an environment variable according to the [instructions](https://github.com/sudoleg/ytai?tab=readme-ov-file#installation--usage).
            Also, make sure that you have **active credit grants** and that they are not expired! You can check it [here](https://platform.openai.com/usage),
            it should be on the right side. 
            """
        )


def set_api_key_in_session_state():
    """If the env-var OPENAI_API_KEY is set, it's value is assigned to openai_api_key property in streamlit's session state.
    Otherwise an input field for the API key is diplayed.
    """
    OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        st.text_input("OpenAI API Key", key="openai_api_key", type="password")
    else:
        st.session_state.openai_api_key = OPENAI_API_KEY


def is_temperature_and_top_p_altered() -> bool:
    if st.session_state.temperature != get_default_config_value(
        "temperature"
    ) and st.session_state.top_p != get_default_config_value("top_p"):
        return True
    return False


def set_initial_session_state():
    # it's recommended to explicitly set session_state vars initially
    if "model" not in st.session_state:
        st.session_state.model = get_default_config_value("default_model")
    if "temperature" not in st.session_state:
        st.session_state.temperature = get_default_config_value("temperature")
    if "top_p" not in st.session_state:
        st.session_state.top_p = get_default_config_value("top_p")


def display_model_settings():
    """Function for displaying the sidebar and adjusting settings.

    Every widget with a key is added to streamlits session state and can be accessed in the application.
    Here, the selectbox for model has the key 'model'.
    Thus the selected model can be accessed via st.session_state.model.
    """
    set_initial_session_state()
    with st.sidebar:
        st.header("Model settings")
        model = st.selectbox(
            "Select a model",
            tuple(get_default_config_value("available_models")),
            key="model",
            help=get_default_config_value("help_texts.model"),
        )
        st.slider(
            label="Adjust temperature",
            min_value=0.0,
            max_value=2.0,
            step=0.1,
            key="temperature",
            help=get_default_config_value("help_texts.temperature"),
        )
        st.sidebar.slider(
            label="Adjust Top P",
            min_value=0.0,
            max_value=1.0,
            step=0.1,
            key="top_p",
            help=get_default_config_value("help_texts.top_p"),
        )
        if is_temperature_and_top_p_altered():
            st.warning(
                "OpenAI generally recommends altering temperature or top_p but not both. See their [API reference](https://platform.openai.com/docs/api-reference/chat/create#chat-create-temperature)"
            )
        if model != get_default_config_value("default_model"):
            st.warning(
                """:warning: Make sure that you have at least Tier 1, as GPT-4 (turbo, 4o) is not available in the free tier.
                See OpenAI's documentation about [usage tiers](https://platform.openai.com/docs/guides/rate-limits/usage-tiers).  
                Also, beware of the potentially higher costs of other models.
                """
            )
        st.write(
            f"[View the source code]({get_default_config_value('github_repo_link')})"
        )
