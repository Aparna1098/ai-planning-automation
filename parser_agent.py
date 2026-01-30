import json

def parse_email(email_text):
    """
    Acts as the 'Parser Agent'. 
    Uses instructions and schema enforcement instead of hard-coded string matching.
    """
    
    # In a real app, you would use: response = client.chat.completions.create(...)
    # Below is the logic you would send to the LLM:
    
    system_prompt = """
    You are a Supply Chain Data Extractor. 
    Your job is to read an email and return ONLY a structured JSON object.
    
    FIELDS TO EXTRACT:
    1. part_id: Look for any alphanumeric ID (e.g., PART-123). If not found, return 'UNKNOWN'.
    2. new_eta: Find the specific date mentioned. Format it as YYYY-MM-DD.
    3. status: If the email mentions delays, shortages, or lateness, set to 'delayed'. Otherwise 'on-time'.
    
    STRICT RULE: Return only the JSON. No conversational text.
    """

    # --- SIMULATION OF LLM OUTPUT ---
    # In your project, the LLM would see the 'system_prompt' + 'email_text' 
    # and return something like the string below:
    
    # This represents what the AI would generate dynamically:
    simulated_ai_response = '{"part_id": "PART-012", "new_eta": "2026-03-10", "status": "delayed"}'
    
    # 1. Convert the AI's "string" response into a Python Dictionary (JSON)
    try:
        parsed_data = json.loads(simulated_ai_response)
    except json.JSONDecodeError:
        # Fallback if the AI gives a messy response
        parsed_data = {"part_id": "UNKNOWN", "new_eta": None, "status": "error"}

    # 2. Add the raw text for auditability
    parsed_data["raw_text"] = email_text
    
    return parsed_data
