import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def drafting_agent(audit_results, mitigation_details):
    prompt = f"Write a professional email for {audit_results['Part_ID']}..." # Your full prompt here
    
    try:
        # Attempt to get the dynamic AI response
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text
    except Exception as e:
        # GRACEFUL FALLBACK: If API is down or quota is hit, use a smart template
        return (
            f"Subject: URGENT - {audit_results['Status']} Risk for {audit_results['Part_ID']}\n\n"
            f"Dear {mitigation_details['POC']},\n\n"
            f"This is an automated escalation regarding {audit_results['Description']}. "
            f"Current tracking indicates a {audit_results['Status']} risk with a Runout Date of {audit_results['Runout_Date']}. "
            f"Supplier ETA is currently {audit_results['Arrival_Buffer']} relative to runout. "
            f"Please proceed with the following SOP: {mitigation_details['Protocol']}.\n\n"
            f"Best regards,\nNPI Planning Bot (Fallback Mode)"
        )
