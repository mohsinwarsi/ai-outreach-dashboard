import streamlit as st

st.set_page_config(page_title="AI Outreach Dashboard", layout="centered")

st.markdown("<h1 style='text-align: center; color: neongreen;'>AI Outreach System</h1>", unsafe_allow_html=True)

st.markdown("""
### 🚀 Welcome to your AI Outreach Assistant

This prototype allows you to:
- Upload your lead list (CSV)
- Generate personalized outreach emails
- Send emails via Gmail (Google API connected)
- Track replies

*Note: Demo mode uses dummy data.*

---
""")

uploaded_file = st.file_uploader("📤 Upload your leads (CSV)", type=["csv"])
if uploaded_file:
    st.success("✅ File uploaded successfully!")
    st.dataframe(uploaded_file)

st.text_input("✏️ Your Email Subject", value="Give Me 10 Minutes—Your POS Will Pay for Itself 💡")

body = st.text_area("📨 Email Body", value="""
Hi [First Name],

What if you could save 1¢ on every transaction and let your POS system pay for itself?

Our all-in-one POS helps businesses like yours:
✅ Boost sales with faster checkouts
✅ Track inventory & sales in real time
✅ Accept all payment types securely

Give me just 10 minutes to show you how it works—and how most of our clients see the system cover its own cost within months.

When’s a good time for a quick call?

Best,  
Mohsin K.  
""")

st.button("📧 Generate & Send Emails")

st.markdown("---")
st.markdown("<footer style='text-align: center; color: gray;'>Made by Mohsin K | Connect on <a href='https://www.linkedin.com/in/mohsinwarsi' target='_blank'>LinkedIn</a></footer>", unsafe_allow_html=True)
