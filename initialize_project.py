import os
import pandas as pd

def initialize_project():
    os.makedirs('supplier_emails', exist_ok=True)
    
    # 1. Build Plan (The Demand anchor)
    build_plan = {
        'Option_Code': ['OPT-A', 'OPT-B', 'OPT-C'],
        'Build_Week': ['2026-W05', '2026-W05', '2026-W06'],
        'Target_Qty': [200, 150, 300]
    }
    pd.DataFrame(build_plan).to_csv('build_plan.csv', index=False)

    # 2. Shortage Report (The Supply detail)
    shortage_report = {
        'Part_ID': ['PART-001', 'PART-002', 'PART-003'],
        'Option_Code': ['OPT-A', 'OPT-A', 'OPT-B'], 
        'System': ['Chassis', 'Power', 'Thermal'],
        'Subsystem': ['Structure', 'Battery', 'Cooling'],
        'OH_Inventory': [50, 0, 1200],
        'Must_Arrive_By': ['2026-02-10', '2026-02-12', '2026-02-15']
    }
    pd.DataFrame(shortage_report).to_csv('shortage_report.csv', index=False)
    
    print("✅ Backend files synchronized with relational columns.")

if __name__ == "__main__":
    initialize_project()