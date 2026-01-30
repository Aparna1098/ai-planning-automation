import streamlit as st
import pandas as pd
import json
from constants import RISK_LEDGER_PATH

# --- AGENT 1: PARSER ---
def parser_agent(email_text):
    # Simulated LLM logic: Extracting data into JSON
    # In reality, this would be: response = openai_client.chat(...)
    simulated_json = '{"part_id": "PART-002", "new_eta": "2026-02-28", "status": "delayed"}'
    data = json.loads(simulated_json)
    data["raw_text"] = email_text
    return data

# --- AGENT 2: AUDITOR ---
def auditor_agent(parsed_data):
    shortage_df = pd.read_csv("shortage_report.csv")
    build_df = pd.read_csv("build_plan.csv")
    
    part_id = parsed_data['part_id']
    if part_id not in shortage_df['Part_ID'].values: return None
    
    part_info = shortage_df[shortage_df['Part_ID'] == part_id].iloc[0]
    impact_mask = build_df['Option_Code'] == part_info['Option_Code']
    impacted_build = build_df[impact_mask].iloc[0]
    
    inventory = part_info['OH_Inventory']
    demand = impacted_build['Target_Qty']
    coverage = inventory / demand if demand > 0 else 1.0
    
    return {
        "Part_ID": part_id,
        "Status": "CRITICAL" if inventory == 0 else "WARNING",
        "Risk_Score": round(1.0 - coverage, 2),
        "Impacted_Option": part_info['Option_Code'],
        "Build_Week": impacted_build['Build_Week'],
        "System": part_info['System'],
        "Subsystem": part_info['Subsystem'],
        "Inventory_Coverage": f"{round(coverage * 100)}%"
    }

# --- AGENT 3: MITIGATION ---
def mitigation_agent(audit_row):
    kb_df = pd.read_csv("org_knowledge.csv")
    match = kb_df[kb_df['Subsystem'] == audit_row['Subsystem']]
    
    poc = match.iloc[0]['POC'] if not match.empty else "GSM"
    action = match.iloc[0]['Standard_Protocol'] if not match.empty else "Review vendor status."
    
    draft = f"Hi {poc},\n\nDelay detected for {audit_row['Part_ID']}. Impacts {audit_row['Build_Week']}. Protocol: {action}"
    return {"POC": poc, "Action": action, "Draft": draft}

# --- STREAMLIT UI ---
st.set_page_config(page_title="NPI Control Tower", layout="wide")
st.title("🚢 NPI Agentic Control Tower")

email_input = st.text_area("Paste Supplier Email Here:", "Part PART-002 is delayed due to weather.")

if st.button("Run Agentic Audit"):
    # Step 1: Parse
    signal = parser_agent(email_input)
    # Step 2: Audit
    result = auditor_agent(signal)
    
    if result:
        st.subheader("Relational Audit Result")
        st.write(pd.DataFrame([result]))
        
        # Step 3: Mitigate
        plan = mitigation_agent(result)
        st.subheader("Recommended Mitigation Plan")
        st.success(f"**Assigned POC:** {plan['POC']}")
        st.info(f"**Action:** {plan['Action']}")
        st.text_area("Communication Draft:", plan['Draft'], height=150)
    else:
        st.error("Part ID not found in Master Data.")
