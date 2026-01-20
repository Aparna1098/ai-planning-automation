def run_mitigation_strategy(audit_row):
    """
    RAG-Lite Logic: Uses backend data to draft a precise recovery plan.
    """
    part_id = audit_row['Part_ID']
    system = audit_row['System']
    subsystem = audit_row['Subsystem']
    option = audit_row['Impacted_Option']
    week = audit_row['Build_Week']

    # Professional Routing Logic based on Subsystem
    if subsystem == "Battery":
        poc = "SIE-B (Power Systems)"
        action = "Request thermal safety clearance and secondary cell source ETA."
    elif subsystem == "Structure":
        poc = "SIE-A (Chassis)"
        action = "Confirm casting machine uptime and weld-cell capacity."
    else:
        poc = "GSM (Global Supply Manager)"
        action = "General vendor status and freight expedite review."
    
    draft = (f"Hi {poc},\n\nWe have a CRITICAL shortage for {part_id} in the {subsystem} subsystem. "
             f"This delay impacts {option} for the {week} build. "
             f"Required: {action}")

    return {"POC": poc, "Action": action, "Draft": draft}