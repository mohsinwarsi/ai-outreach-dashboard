import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import pickle
import os
import base64
import openai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build

# === CONFIGURATION ===
st.set_page_config(page_title="AI Outreach Dashboard", layout="wide")

REDIRECT_URI = "https://ai-outreach-dashboard-e34h2sugpctnjdskipqkck.streamlit.app/"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Load Gmail API credentials
CLIENT_ID = st.secrets["gmail"]["client_id"]
CLIENT_SECRET = st.secrets["gmail"]["client_secret"]

# === FUNCTIONS ===

def get_credentials():
    if os.path.exists("token.pkl"):
        with open("token.pkl", "rb") as token:
            creds = pickle.load(token)
        if creds and creds.valid:
            return creds
    return None

def save_credentials(creds):
    with open("token.pkl", "wb") as token:
        pickle.dump(creds, token)

def authorize_gmail():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = REDIRECT_URI

    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    st.markdown(f"[🔐 Authorize Gmail Access]({auth_url})")
    code = st.text_input("Paste the authorization code here")

    if code:
        try:
            flow.fetch_token(code=code)
            creds = flow.credentials
            save_credentials(creds)
            st.success("✅ Gmail connected successfully!")
        except Exception as e:
            st.error(f"Error fetching token: {e}")

def create_message(sender, to, subject, message_text):
    message = MIMEMultipart()
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    message.attach(MIMEText(message_text, "plain"))
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw_message}

def send_email(creds, to, subject, body):
    try:
        service = build("gmail", "v1", credentials=creds)
        sender = "me"
        message = create_message(sender, to, subject, body)
        send_message = service.users().messages().send(userId=sender, body=message).execute()
        return send_message
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")

# === MAIN APP ===

st.title("📧 AI Outreach Dashboard")

creds = get_credentials()
if not creds:
    st.warning("Gmail not connected.")
    authorize_gmail()
else:
    st.success("✅ Gmail connected.")

    st.subheader("Compose Email")
    to_email = st.text_input("Recipient Email")
    subject = st.text_input("Subject", "Let's talk about AI solutions")
    body = st.text_area("Email Body", "Hi there,\n\nWe’d love to show you how AI can improve your outreach. Let’s talk!")

    if st.button("🚀 Send Email"):
        if to_email and subject and body:
            result = send_email(creds, to_email, subject, body)
            st.success("✅ Email sent successfully!")
            st.json(result)
        else:
            st.warning("Please fill out all fields before sending.")

