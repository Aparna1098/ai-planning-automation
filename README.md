# ai-planning-automation
A collection of AI-powered micro-tools for supply chain and material planning automation including email agents, risk detection, and workflow optimization.


# AI Supplier Follow-Up Tool (MVP)

This AI tool:
- Reads PO / Shortage Report CSV files
- Detects missing or late ETAs
- Automatically drafts supplier follow-up emails using LLMs
- Allows downloading all emails

## How to Use
1. Go to the Streamlit app URL (after deployment)
2. Upload your CSV
3. Review risk classification
4. Generate supplier emails

## Deployment
This tool is deployed using Streamlit Cloud.
To deploy:
- Push repository to GitHub
- Go to https://share.streamlit.io
- Select this repo and deploy `app.py`

## API Key Setup
Add the following to Streamlit Secrets:

