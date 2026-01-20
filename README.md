# NPI Agentic Control Tower

## Project Overview
The **NPI Agentic Control Tower** is an automated supply chain management system designed to monitor and mitigate risks in New Product Introduction (NPI) workflows. The system utilizes a multi-agent architecture to process supplier communication and reconcile it against core supply chain data to identify potential build disruptions.

---

## System Architecture

The architecture is built on a modular, event-driven framework that bridges the gap between unstructured communication and structured industrial planning.

```mermaid
graph TD
    A[Unstructured Supplier Email] -->|Ingestion| B(Parser Agent)
    B -->|Structured JSON| C(Auditor Agent)
    
    subgraph "Relational Data Layer"
    D[(Shortage Report CSV/GSheet)]
    E[(Build Plan CSV/GSheet)]
    end
    
    C <--> D
    C <--> E
    
    C -->|Identified Build Impact| F{Exception Queue}
    F -->|Critical Risk Selected| G(Mitigation Agent)
    
    subgraph "Knowledge Layer"
    H[.md Response Playbooks]
    I[.md Org Knowledge]
    end
    
    G <--> H
    G <--> I
    
    G -->|Automated Escalation| J[Stakeholder Alert & Recovery Plan]
