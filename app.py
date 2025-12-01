import streamlit as st
import pandas as pd
import requests
import datetime

st.set_page_config(page_title="AI Supplier Follow-Up Tool", layout="centered")

st.title("📦 AI Supplier Follow-Up Tool")
st.write("Upload your PO / Shortage Report CSV and automatically generate supplier follow-up emails.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Data Preview")
    st.dataframe(df)

    # Risk Logic
    st.subheader("🚨 Risk Detection")

    def classify_risk(row):
        if pd.isna(row["ETA"]):
            return "Missing ETA — High Risk"
        try:
            eta = pd.to_datetime(row["ETA"])
            if eta < datetime.datetime.today():
                return "ETA Passed — Critical"
        except:
            return "Invalid ETA — High Risk"

        return "On Track"

    df["Risk"] = df.apply(classify_risk, axis=1)
    st.dataframe(df)

    high_risk = df[df["Risk"] != "On Track"]

    st.subheader("✉️ AI-Generated Supplier Emails")

    if st.button("Generate Emails"):
        emails = []
        for _, row in high_risk.iterrows():
            supplier = row.get("Supplier", "Supplier")
            part = row.get("Part", "Part")
            po = row.get("PO", "PO")
            eta = row.get("ETA", "N/A")
            issue = row.get("Risk", "Risk Identified")

            prompt = f"""
Draft a concise supplier follow-up email.

Context:
- Supplier: {supplier}
- Part: {part}
- PO: {po}
- ETA: {eta}
- Issue: {issue}

Requirements:
- Professional but firm
- Ask for shipping confirmation
- Ask for recovery plan if delayed
- <120 words
"""

            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"},
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": prompt}],
                }
            )

            email_text = resp.json()["choices"][0]["message"]["content"]
            emails.append(email_text)

            st.write("---")
            st.write(email_text)

        # Download All
        st.download_button(
            "Download All Emails",
            "\n\n---\n\n".join(emails),
            "supplier_emails.txt",
            "text/plain",
        )
