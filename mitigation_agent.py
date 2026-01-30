import pandas as pd

def run_mitigation_strategy(audit_row, knowledge_base_path="org_knowledge.csv"):
    """
    Acts as the 'Mitigation Agent'.
    Dynamically retrieves POCs and Protocols from external data (RAG-lite).
    """
    # 1. Load the organizational knowledge (the "Brain")
    # This file contains columns: Subsystem, POC, Standard_Protocol
    try:
        kb_df = pd.read_csv(knowledge_base_path)
    except FileNotFoundError:
        # Emergency Fallback if the file is missing
        return {"POC": "GSM", "Action": "Review needed", "Draft": "System Error: KB missing."}

    # 2. Extract context from the specific audit row
    subsystem = audit_row['Subsystem']
    
    # 3. Dynamic Lookup (The "Retrieval" in RAG)
    # We look for the subsystem in our knowledge base
    match = kb_df[kb_df['Subsystem'] == subsystem]

    if not match.empty:
        poc = match.iloc[0]['POC']
        protocol = match.iloc[0]['Standard_Protocol']
    else:
        # The 'Catch-All' logic for unknown subsystems
        poc = "Global Supply Manager (GSM)"
        protocol = "Initiate general vendor status and freight expedite review."

    # 4. Agentic Synthesis (Drafting the plan)
    # The agent combines 'Static Knowledge' (protocol) with 'Dynamic Data' (audit_row)
    draft = (
        f"ATTN: {poc}\n\n"
        f"Subject: CRITICAL Build Impact - Part {audit_row['Part_ID']}\n\n"
        f"The {subsystem} subsystem is currently flagging a shortage impacting "
        f"Option Code {audit_row['Impacted_Option']} for Build Week {audit_row['Build_Week']}.\n"
        f"MAPPING LOGIC: This delay creates a {audit_row['Risk_Level']} risk to production.\n\n"
        f"REQUIRED MITIGATION: {protocol}"
    )

    return {
        "POC": poc, 
        "Action": protocol, 
        "Draft": draft
    }
