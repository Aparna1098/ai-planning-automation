# NPI Agentic Control Tower

## Project Overview
The **NPI Agentic Control Tower** is an automated supply chain management system designed to monitor and mitigate risks in New Product Introduction (NPI) workflows. The system utilizes a multi-agent architecture to process supplier communication and reconcile it against core supply chain data to identify potential build disruptions.

---

## Agent Architecture
This project utilizes a specialized multi-agent system where each agent is responsible for a specific stage of the risk management lifecycle.



### 1. Parser Agent
The Parser Agent serves as the entry point for unstructured data.
* **Input**: Monitors a directory of incoming supplier communication (e.g., email text files).
* **Function**: Extracts critical data points such as Part IDs, new Estimated Time of Arrivals (ETAs), and the reason for delay.
* **Output**: Structured JSON data that can be programmatically audited.

### 2. Auditor Agent
The Auditor Agent performs the core analytical work by conducting a "Relational Audit" across multiple data sources.
* **Logic**: It joins the structured data from the Parser Agent with two primary backend datasets:
    * **Shortage Report**: Identifies current inventory levels and the technical system/subsystem for the part.
    * **Build Plan**: Maps the specific part to the vehicle "Option Code" and the specific build week it impacts.
* **Output**: A risk score and status (Critical vs. Warning) based on inventory availability and the timing of the build.

### 3. Mitigation Agent
The Mitigation Agent handles the resolution and escalation phase of the workflow.
* **Knowledge Retrieval**: References a localized knowledge base (Markdown playbooks) to identify the correct stakeholder for a specific subsystem.
* **Function**: Based on the audit results, it determines the appropriate escalation path (e.g., contacting a specific industrial engineer).
* **Output**: A drafted recovery plan and stakeholder alert tailored to the specific technical system and build impact.

---

## System Workflow
1. **Initialize**: A setup script generates the initial relational data model (Build Plan and Shortage Report) and the organizational knowledge base.
2. **Synchronize**: The user triggers an audit via the Streamlit dashboard.
3. **Analyze**: The agents work in sequence to move from an unstructured email signal to a relational risk assessment.
4. **Action**: The dashboard surfaces high-priority exceptions, allowing the user to generate and send targeted mitigation strategies.



---

## Technical Stack
* **Frontend**: Streamlit
* **Data Processing**: Python (Pandas)
* **Storage**: Local CSVs or synchronized Google Sheets
* **Knowledge Base**: Markdown (RAG-lite)

---

## Setup and Installation

### 1. Environment Configuration
To ensure all agents and the dashboard function correctly, it is recommended to use a virtual environment with Python 3.12.

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
