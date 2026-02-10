import pandas as pd

def mitigation_agent(audit_results, email_text):
    # Load Organizational Matrix
    try:
        kb_df = pd.read_csv("org_knowledge.csv")
    except FileNotFoundError:
        return {"POC": "Data Missing", "Target_Role": "N/A", "Protocol": "Verify CSV files."}

    # 1. Clean Subsystem Extraction
    # Ensures "Energy - Battery" becomes "Battery" without extra spaces
    description = audit_results.get("Description", "")
    subsystem = description.split("-")[-1].strip() if "-" in description else description
    
    # 2. Enhanced Keyword Detection
    email_content = email_text.lower()
    
    if any(k in email_content for k in ["quality", "defect", "rework", "failed", "inspection"]):
        target_role = "Quality"
    elif any(k in email_content for k in ["cost", "price", "material", "commercial", "shortage"]):
        target_role = "GSM"
    else:
        # Default for timing/logistics delays
        target_role = "NPI TPM"

    # 3. Precise Lookup (Subsystem + Role)
    match = kb_df[(kb_df['Subsystem'] == subsystem) & (kb_df['Role'] == target_role)]
    
    if not match.empty:
        poc_name = match.iloc[0]['Name']
        protocol = match.iloc[0]['Standard_Protocol']
    else:
        # Final fallback if the specific role isn't mapped for that subsystem
        poc_name = "Global Planning Lead"
        target_role = "General Planning"
        protocol = "Initiate manual escalation protocol."

    return {
        "Target_Role": target_role,
        "POC": poc_name,
        "Protocol": protocol
    }
