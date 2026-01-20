import pandas as pd

def run_audit(parsed_data):
    # Load backend data
    shortage_df = pd.read_csv('shortage_report.csv')
    build_df = pd.read_csv('build_plan.csv')

    part_id = parsed_data['part_id']
    if part_id not in shortage_df['Part_ID'].values:
        return None

    # Retrieve supply-side details from Shortage Report
    part_info = shortage_df[shortage_df['Part_ID'] == part_id].iloc[0]
    
    # Connect to the Build Plan using Option_Code (The Join)
    # This identifies which high-level build is at risk
    impact_mask = build_df['Option_Code'] == part_info['Option_Code']
    impacted_build = build_df[impact_mask].iloc[0]
    
    # Audit Logic: High risk if inventory is 0
    is_critical = part_info['OH_Inventory'] == 0
    
    # ALL keys used in st.dataframe(ledger[[...]]) must be defined here
    return {
        "Part_ID": part_id,
        "Status": "CRITICAL" if is_critical else "WARNING",
        "Risk_Score": 10 if is_critical else 5,
        "Impacted_Option": part_info['Option_Code'], # From shortage_report
        "Build_Week": impacted_build['Build_Week'],  # From build_plan
        "System": part_info['System'],               # From shortage_report
        "Subsystem": part_info['Subsystem']          # From shortage_report
    }