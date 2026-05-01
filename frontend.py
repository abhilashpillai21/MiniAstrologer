import streamlit as st
import vectordb
import auth
from dashboard import show_dashboard


# def get_usage_logs():
#     response = supabase.table("usage_logs").select("user_email, question, created_at").execute
#     return response.data

def getuploadfile(uploaded_file):
    if uploaded_file is not None:
        uploaded_file.seek(0)
        return uploaded_file.read().decode("utf-8")
    return None


# def login_user(email, password):
#     response = supabase.auth.sign_in_with_password({
#         "email": email,
#         "password": password
#     })
#     return response


def signup_user(email, password):
    response = auth.auth.sign_up({
        "email": email,
        "password": password
    })
    return response


# -----------------------------
# Session state setup
# -----------------------------

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask your question"}
    ]

if "last_file" not in st.session_state:
    st.session_state.last_file = None


# -----------------------------
# Page title
# -----------------------------

st.title(":rainbow[Mini Astrology App]")


# -----------------------------
# Auth UI
# -----------------------------

if st.session_state.user is None:
    st.subheader("Login or create an account")

    mode = st.radio("Choose", ["Login", "Sign Up"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button(mode):
        if not email or not password:
            st.error("Please enter both email and password.")
        else:
            try:
                if mode == "Sign Up":
                    signup_user(email, password)
                    st.success("Account created. Please check your email to confirm your account.")
                    st.info("After confirming your email, come back and log in.")

                else:
                    response = auth.login_user(email, password)

                    if response.user:
                        st.session_state.user = response.user
                        st.success("Logged in successfully.")
                        st.rerun()
                    else:
                        st.error("Login failed.")

            except Exception as e:
                st.error(f"Auth error: {str(e)}")

    st.warning("Please log in to use the app.")
    st.stop()


# -----------------------------
# Logged-in user area
# -----------------------------

st.sidebar.write(f"Logged in as: {st.session_state.user.email}")

if st.sidebar.button("Log out"):
    st.session_state.user = None
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask your question"}
    ]
    st.session_state.last_file = None
    st.rerun()


# -----------------------------
# File upload
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload your birth chart in txt format",
    type="txt",
    key="main_file_uploader"
)

if uploaded_file is not None:
    if st.session_state.last_file != uploaded_file.name:
        st.session_state.last_file = uploaded_file.name
        st.session_state.messages = [
            {"role": "assistant", "content": "File uploaded. Ask your question."}
        ]


# -----------------------------
# Chat history display
# -----------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Chat input
# -----------------------------

if prompt := st.chat_input("Ask your question"):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        file_text = getuploadfile(uploaded_file)

        if file_text is None:
            full_response = "Please upload a birth chart text file first."
            sources = []
        else:
            full_response, sources = vectordb.findanswers(file_text, prompt)

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })

        message_placeholder.markdown(full_response)

        try:
            auth.insert_data(st.session_state.user.email, prompt, full_response)

        except Exception as e:
            st.write(f'Could not save usagelogs : {e}')

        if sources:
            with st.sidebar:
                with st.expander("Sources used"):
                    for i, (distance, text) in enumerate(sources):
                        st.markdown(f"**Source {i + 1} | Score: {distance:.4f}**")
                        st.code(text)