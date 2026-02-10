import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# Import your custom agents
from parser_agent import parser_agent
from auditor_agent import auditor_agent
from mitigation_agent import mitigation_agent
from drafting_agent import drafting_agent

# --- PAGE CONFIG & BALANCED CSS ---
st.set_page_config(page_title="NPI Agentic Control Tower", layout="wide")

st.markdown("""
    <style>
    /* Increased padding to prevent clipping of the date and title */
    .block-container {padding-top: 2.5rem; padding-bottom: 0rem;}
    
    /* Header styling with specific margin to drop the date down */
    .stMarkdown div p { margin-top: 5px; }
    
    /* Title spacing */
    .main-title {font-size: 26px; font-weight: bold; margin-bottom: 10px;}
    
    /* Compact input area remains the same */
    .stTextArea textarea {height: 90px !important;}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_t, col_date = st.columns([3.5, 1.5])
with col_t:
    # Using a div with a class for custom margin control
    st.markdown('<div class="main-title">Material Planning Assistant</div>', unsafe_allow_html=True)
with col_date:
    st.write(f"**System Date:**\nMonday, Feb 09, 2026")

# --- INPUT SECTION ---
email_input = st.text_area("Paste Supplier Email:", label_visibility="collapsed")
exec_btn = st.button("Execute Audit Pipeline", use_container_width=True)

if exec_btn and email_input:
    with st.spinner("Analyzing..."):
        # Agent Pipeline execution
        extracted = parser_agent(email_input)
        audit = auditor_agent(extracted)
        
        if audit:
            mitigation = mitigation_agent(audit, email_input)
            
            # --- PRIMARY RESULTS GRID ---
            c1, c2, c3 = st.columns([1.5, 2.5, 2])
            
            with c1:
                # Dynamic Status Badge
                colors = {"CRITICAL": "#ff4b4b", "WARNING": "#ffa500", "ON TRACK": "#28a745"}
                bg = colors.get(audit["Status"], "#808080")
                st.markdown(f'<div style="background:{bg}; color:white; padding:12px; border-radius:8px; text-align:center; font-weight:bold; font-size:18px;">{audit["Status"]}</div>', unsafe_allow_html=True)
            
            with c2:
                # Core risk metrics display
                st.markdown(f"**Part:** {audit['Part_ID']} | **Runout:** `{audit['Runout_Date']}`")
                st.markdown(f"**Buffer:** `{audit['Arrival_Buffer']}`")
            
            with c3:
                # Stakeholder assignment
                st.markdown(f"👤 **{mitigation['POC']}**")
                st.caption(f"{mitigation['Target_Role']}")

            st.divider()

            # --- DRAWERS ---
            with st.expander("Relational Audit Summary", expanded=True):
                st.table(pd.DataFrame([audit]))
            
            with st.expander("AI Communication Draft"):
                with st.spinner("Generating..."):
                    draft = drafting_agent(audit, mitigation)
                st.code(draft, language="text")

            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                with st.expander("📉 Shortage Report"):
                    st.dataframe(pd.read_csv("shortage_report.csv"), hide_index=True)
            with col_sub2:
                with st.expander("📅 Build Plan"):
                    st.dataframe(pd.read_csv("build_plan.csv"), hide_index=True)
        else:
            st.error("Technical Error: Part ID not recognized.")

# Footer
st.caption("v2.5.1 Balanced Layout for 13\" Display")
