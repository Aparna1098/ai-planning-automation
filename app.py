import streamlit as st
import pandas as pd
import os
from parser_agent import parse_email
from auditor_agent import run_audit
from mitigation_agent import run_mitigation_strategy

st.set_page_config(page_title="NPI Command Center", layout="wide")
st.title("🛡️ NPI Action Control Tower")

# --- TRIGGER AUDIT ---
if st.button("🔄 Audit Supply Chain Exceptions"):
    results = []
    if os.path.exists('supplier_emails'):
        for file in os.listdir('supplier_emails'):
            if file.endswith('.txt'):
                with open(os.path.join('supplier_emails', file), 'r') as f:
                    content = f.read()
                    parsed = parse_email(content)
                    audit = run_audit(parsed)
                    if audit:
                        audit['email_body'] = content
                        results.append(audit)
        pd.DataFrame(results).to_csv('risk_ledger.csv', index=False)
        st.success("Audit complete. Exceptions identified.")

# --- ACTION QUEUE & DROPDOWN ---
if os.path.exists('risk_ledger.csv'):
    ledger = pd.read_csv('risk_ledger.csv').sort_values(by="Risk_Score", ascending=False)
    st.header("🚨 Priority Action Queue")
    st.dataframe(ledger[['Part_ID', 'Status', 'Impacted_Option', 'Build_Week', 'Subsystem']], use_container_width=True)

    st.divider()
    # RESTORED: Select specific risk to generate action
    selected_part = st.selectbox("Select Impacted Part for Mitigation Strategy:", ledger['Part_ID'])
    
    if st.button("🤖 Run RAG Mitigation"):
        # Retrieve the full data row for the selected part
        row = ledger[ledger['Part_ID'] == selected_part].iloc[0]
        
        with st.spinner(f"Consulting Knowledge Base for {selected_part}..."):
            strategy = run_mitigation_strategy(row)
        
        st.subheader(f"Strategy for {selected_part}")
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**Assigned Owner:** {strategy['POC']}")
            st.info(f"**Recommended Action:** {strategy['Action']}")
        with col2:
            st.warning("**Draft Stakeholder Alert:**")
            st.text_area("Copy to Clipboard:", strategy['Draft'], height=150)