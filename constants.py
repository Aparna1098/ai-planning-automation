# constants.py

# --- File Paths ---
SHORTAGE_REPORT_PATH = "data/shortage_report.csv"
BUILD_PLAN_PATH = "data/build_plan.csv"
KNOWLEDGE_BASE_PATH = "data/org_knowledge.csv"
RISK_LEDGER_PATH = "outputs/risk_ledger.csv"

# --- Risk Logic Thresholds ---
# How many days of inventory buffer trigger a warning?
LOW_INVENTORY_THRESHOLD = 2 
# How many days of delay trigger a critical status?
CRITICAL_DELAY_DAYS = 5

# --- Agent Personas (Prompts) ---
PARSER_SYSTEM_PROMPT = """
You are a Supply Chain Data Extractor. 
Extract Part_ID, New_ETA, and Status into JSON format.
"""

MITIGATION_TONE = "Professional, firm, and technical."
