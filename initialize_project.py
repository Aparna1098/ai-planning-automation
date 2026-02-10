import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def initialize_system():
    # 1. Shortage Report & 2. Build Plan remain standard...
    shortage_data = {
        "Part_ID": ["PART-001", "PART-002", "PART-003"],
        "System": ["Energy", "Sensing", "Computing"],
        "Subsystem": ["Battery", "Front Axle", "Cooling Loop"],
        "OH_Inventory": [45, 0, 120],  
        "Option_Code": ["P1", "C2", "T1"]
    }
    
    # 3. Expanded Org Knowledge (Matrix Organization)
    # We now map multiple roles to each Subsystem
    kb_data = {
        "Subsystem": ["Battery", "Battery", "Battery", "Front Axle", "Front Axle", "Front Axle"],
        "Role": ["NPI TPM", "GSM", "Quality", "NPI TPM", "GSM", "Quality"],
        "Name": ["Sarah Miller", "David Smith", "Alice Wong", "James Chen", "Robert Glass", "Lee Zhang"],
        "Standard_Protocol": [
            "Manage build schedule impact and line trials.",
            "Negotiate expedite fees and commercial recovery.",
            "Review supplier quality deviation requests.",
            "Verify alternative part numbers in PLM.",
            "Execute spot-buy for raw material shortages.",
            "Perform incoming inspection for reworked units."
        ]
    }

    pd.DataFrame(shortage_data).to_csv(os.path.join(BASE_DIR, "shortage_report.csv"), index=False)
    pd.DataFrame(kb_data).to_csv(os.path.join(BASE_DIR, "org_knowledge.csv"), index=False)
    
    print(f"✅ Matrix Organization Initialized at: {BASE_DIR}")

if __name__ == "__main__":
    initialize_system()
