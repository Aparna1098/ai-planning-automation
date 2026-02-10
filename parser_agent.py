import google.genai as genai
import os
import json
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def parser_agent(email_text):
    """
    Extracts Part ID, ETA, and Qty from email text.
    Includes a fallback mechanism to handle API Quota (429) errors.
    """
    prompt = f"""
    Extract the following entities from this supplier email in JSON format:
    - part_id (e.g., PART-001)
    - revised_eta (YYYY-MM-DD)
    - quantity (integer)

    Email: {email_text}
    Current Date: 2026-02-09
    """

    try:
        # Primary Path: AI Inference
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        return json.loads(response.text)

    except Exception as e:
        # Fallback Path: Deterministic Regex (The "Circuit Breaker")
        # If the API is exhausted, we manually find the data to keep the demo alive.
        
        # 1. Try to find any string like PART-XXX
        part_match = re.search(r"PART-\d+", email_text.upper())
        part_id = part_match.group(0) if part_match else "PART-001"
        
        # 2. Try to find a date, otherwise default to +2 days from today
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", email_text)
        revised_eta = date_match.group(0) if date_match else (datetime(2026, 2, 9) + timedelta(days=2)).strftime('%Y-%m-%d')
        
        # 3. Try to find a quantity, otherwise default to 50
        qty_match = re.search(r"(\d+)\s*(?:pcs|units|pieces|quantity)", email_text.lower())
        quantity = int(qty_match.group(1)) if qty_match else 50

        print(f"API Throttled or Error: {e}. Switching to Regex Fallback.")
        
        return {
            "part_id": part_id,
            "revised_eta": revised_eta,
            "quantity": quantity,
            "is_fallback": True # Flag to let the UI know this is a "best guess"
        }
