import pandas as pd
from constants import SHORTAGE_REPORT_PATH, BUILD_PLAN_PATH, KNOWLEDGE_BASE_PATH

def init_data():
    # 1. Master Supply Data (Shortage Report)
    shortage_data = {
        "Part_ID": [f"PART-{i:03}" for i in range(1, 11)],
        "System": ["Powertrain", "Chassis", "Battery", "Body", "Interior"] * 2,
        "Subsystem": ["Inverter", "Suspension", "Cells", "Stamping", "Seats"] * 2,
        "Option_Code": ["P85", "C1", "B_LR", "S1", "I_PREM"] * 2,
        "OH_Inventory": [10, 0, 5, 100, 20, 50, 0, 15, 0, 5]
    }
    pd.DataFrame(shortage_data).to_csv(SHORTAGE_REPORT_PATH, index=False)

    # 2. Master Demand Data (Build Plan)
    build_data = {
        "Option_Code": ["P85", "C1", "B_LR", "S1", "I_PREM"],
        "Build_Week": ["2026-W05", "2026-W05", "2026-W06", "2026-W07", "2026-W05"],
        "Target_Qty": [50, 20, 100, 40, 60]
    }
    pd.DataFrame(build_data).to_csv(BUILD_PLAN_PATH, index=False)

    # 3. Org Knowledge Base (for Mitigation Agent)
    kb_data = {
        "Subsystem": ["Inverter", "Suspension", "Cells", "Stamping", "Seats"],
        "POC": ["Alice (Power)", "Bob (Chassis)", "Charlie (Battery)", "Dana (Body)", "Eve (Interior)"],
        "Standard_Protocol": [
            "Request secondary component source.",
            "Verify casting machine uptime.",
            "Review thermal safety clearance.",
            "Confirm stamping tool availability.",
            "Expedite freight for fabric materials."
        ]
    }
    pd.DataFrame(kb_data).to_csv(KNOWLEDGE_BASE_PATH, index=False)
    print("System Data Initialized Successfully.")

if __name__ == "__main__":
    init_data()
