def parse_email(email_text):
    """
    Acts as the 'Email Translator' Agent.
    In a production environment, this would call an LLM (like GPT-4o) 
    to extract structured data from unstructured text.
    """
    
    # 1. Identify the Part ID mentioned in the email
    # We look for 'PART-XXX' patterns to match your 50-part MRP list.
    found_part = "UNKNOWN"
    for i in range(1, 51):
        part_str = f"PART-{i:03}"
        if part_str in email_text:
            found_part = part_str
            break
            
    # 2. Extract the New ETA
    # Simple keyword-based extraction to simulate AI logic
    new_eta = "2026-02-15" # Default to our standard build deadline
    if "Feb 22" in email_text: 
        new_eta = "2026-02-22"
    elif "Feb 18" in email_text: 
        new_eta = "2026-02-18"
    
    # 3. Determine the Status
    # We flag it as 'delayed' if keywords suggest a production snag.
    status = "delayed" if any(x in email_text.lower() for x in ["delay", "late", "down", "short"]) else "on-time"
    
    return {
        "part_id": found_part,
        "new_eta": new_eta,
        "status": status,
        "raw_text": email_text
    }