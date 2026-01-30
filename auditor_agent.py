import pandas as pd
from constants import SHORTAGE_REPORT_PATH, BUILD_PLAN_PATH, CRITICAL_DELAY_DAYS

def run_audit(parsed_data):
    """
    Performs a relational audit by joining supply signals with master build plans.
    Calculates impact severity using multi-source data points.
    """
    # 1. Load backend data using centralized constants
    shortage_df = pd.read_csv(SHORTAGE_REPORT_PATH)
    build_df = pd.read_csv(BUILD_PLAN_PATH)

    part_id = parsed_data.get('part_id')
    
    # Validation: Ensure the Part ID exists in our system of record
    if part_id not in shortage_df['Part_ID'].values:
        print(f"Audit Warning: Part {part_id} not found in master records.")
        return None

    # 2. Supply-Side Retrieval (Shortage Report)
    part_info = shortage_df[shortage_df['Part_ID'] == part_id].iloc[0]
    
    # 3. Relational Join (Build Plan)
    # Mapping the part-level signal to the high-level vehicle production impact
    impact_mask = build_df['Option_Code'] == part_info['Option_Code']
    
    if not impact_mask.any():
        return None
        
    impacted_build = build_df[impact_mask].iloc[0]
    
    # 4. Analytics Logic: Dynamic Risk Calculation
    # Instead of hard-coding 10 or 5, we calculate based on inventory coverage.
    inventory = part_info['OH_Inventory']
    demand = impacted_build['Target_Qty']
    
    # Logic: Risk increases as (Demand / Inventory) increases
    coverage_ratio = inventory / demand if demand > 0 else 1.0
    
    # Final Risk Assignment
    # A delay is critical if inventory is zero OR if it impacts a near-term Build Week
    is_critical = (inventory == 0) or (parsed_data['status'] == 'delayed' and coverage_ratio < 0.2)
    
    return {
        "Part_ID": part_id,
        "Status": "CRITICAL" if is_critical else "WARNING",
        "Risk_Score": round(1.0 - coverage_ratio, 2) if not is_critical else 1.0,
        "Impacted_Option": part_info['Option_Code'],
        "Build_Week": impacted_build['Build_Week'],
        "System": part_info['System'],
        "Subsystem": part_info['Subsystem'],
        "Inventory_Coverage": f"{round(coverage_ratio * 100)}%"
    }
