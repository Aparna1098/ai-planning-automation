import pandas as pd
from datetime import datetime, timedelta

def auditor_agent(parsed_data):
    try:
        shortage_df = pd.read_csv("shortage_report.csv")
        build_df = pd.read_csv("build_plan.csv")
    except FileNotFoundError:
        return {"error": "Master CSV files not found."}
    
    part_id = str(parsed_data.get('part_id', '')).strip().upper()
    if part_id not in shortage_df['Part_ID'].values:
        return None
    
    part_info = shortage_df[shortage_df['Part_ID'] == part_id].iloc[0]
    impacted_build = build_df[build_df['Option_Code'] == part_info['Option_Code']].iloc[0]
    
    # 1. Calculate Burn Rate and Runout
    inventory = part_info['OH_Inventory']
    demand = impacted_build['Target_Qty']
    daily_burn = (demand / 5) if demand > 0 else 0
    doh = round(inventory / daily_burn) if daily_burn > 0 else 0
    
    today = datetime(2026, 2, 9) # Hardcoded for your current demo date
    runout_dt = today + timedelta(days=doh)
    
    # 2. Parse Supplier ETA
    eta_str = parsed_data.get('revised_eta', '2026-02-09')
    try:
        eta_dt = datetime.strptime(eta_str, "%Y-%m-%d")
    except:
        eta_dt = today

    # 3. Calculate TRUE Buffer (Runout Date - ETA)
    # This tells you exactly how many days of "safety" you have left.
    true_buffer = (runout_dt - eta_dt).days
    
    # 4. New Logic Trigger
    if true_buffer <= 0:
        status = "CRITICAL" # Parts arrive too late
    elif true_buffer <= 2:
        status = "WARNING"  # Parts arrive, but with < 2 days of safety
    else:
        status = "HEALTHY"  # Sufficient safety margin
    
    return {
        "Part_ID": part_id,
        "Description": f"{part_info['System']} - {part_info['Subsystem']}",
        "Status": status,
        "Days_on_Hand": f"{doh} Days",
        "OH_Inventory": inventory,
        "Build_Week": impacted_build['Build_Week'],
        "Arrival_Buffer": f"{true_buffer} Days", # Now reflects safety margin
        "Runout_Date": runout_dt.strftime('%Y-%m-%d')
    }
