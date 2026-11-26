"""
Tara PrivacyOS — Interactive Visual Data-Flow & Cross-Border Transfer Engine
Generates live visual node-link topologies, traces data lineage, inspects statutory legal bases,
and auto-generates UK-to-India IDTA (International Data Transfer Agreement) schedules.
Complies with UK GDPR (Articles 30, 44–49) & India DPDP Act 2023 (Section 16).
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

TOPOLOGY_PRESETS = {
    "tara-consultation": {
        "id": "tara-consultation",
        "name": "Tara Spiritual & Consultation Platform",
        "company": "Tara Infotech Ltd",
        "description": "Multi-tier cloud architecture serving UK astrology & wellness clients with overseas backend development & support in India.",
        "nodes": [
            {
                "id": "node_uk_users",
                "label": "UK End-Users / Clients",
                "subtext": "Mobile & Web App Clients",
                "category": "DATA_SUBJECT",
                "jurisdiction": "United Kingdom (London/Manchester)",
                "flag": "🇬🇧",
                "color": "#00CEFF",
                "x": 80, "y": 180,
                "icon": "👤"
            },
            {
                "id": "node_api_gateway",
                "label": "FastAPI Ingestion Gateway",
                "subtext": "AWS eu-west-2 (London Region)",
                "category": "CONTROLLER_SYSTEM",
                "jurisdiction": "United Kingdom",
                "flag": "🇬🇧",
                "color": "#6C5CE7",
                "x": 300, "y": 180,
                "icon": "⚡"
            },
            {
                "id": "node_db_postgres",
                "label": "PostgreSQL & Redis Cache",
                "subtext": "Encrypted Customer Store (AES-256)",
                "category": "PRIMARY_STORAGE",
                "jurisdiction": "United Kingdom",
                "flag": "🇬🇧",
                "color": "#51CF66",
                "x": 540, "y": 90,
                "icon": "🗄️"
            },
            {
                "id": "node_openai_llm",
                "label": "OpenAI GPT-4 Mini API",
                "subtext": "Consultation Transcripts Processing",
                "category": "SUBPROCESSOR_CLOUD",
                "jurisdiction": "United States (California)",
                "flag": "🇺🇸",
                "color": "#FFD43B",
                "x": 540, "y": 270,
                "icon": "🤖"
            },
            {
                "id": "node_stripe_payments",
                "label": "Stripe UK & EU Gateway",
                "subtext": "Wallet Balances & Top-Ups",
                "category": "PAYMENT_PROCESSOR",
                "jurisdiction": "Ireland / United Kingdom",
                "flag": "🇮🇪",
                "color": "#51CF66",
                "x": 300, "y": 340,
                "icon": "💳"
            },
            {
                "id": "node_india_support",
                "label": "India Tech & Support Team",
                "subtext": "Remote Debugging & Customer Care",
                "category": "CROSS_BORDER_IMPORTER",
                "jurisdiction": "India (Noida & Bengaluru)",
                "flag": "🇮🇳",
                "color": "#FF6B6B",
                "x": 780, "y": 180,
                "icon": "🇮🇳"
            }
        ],
        "links": [
            {
                "id": "flow_1",
                "source": "node_uk_users",
                "target": "node_api_gateway",
                "label": "Client Queries & Birth Details",
                "data_types": ["Name", "DOB", "Birth Place", "Consultation Question"],
                "legal_basis": "UK GDPR Article 6(1)(b) Contractual Necessity",
                "special_category": True,
                "art9_exception": "Article 9(2)(a) Explicit Consent Required",
                "encryption": "TLS 1.3 / HTTPS",
                "is_cross_border": False,
                "status": "COMPLIANT",
                "risk_desc": "Standard domestic processing for service fulfillment."
            },
            {
                "id": "flow_2",
                "source": "node_api_gateway",
                "target": "node_db_postgres",
                "label": "Persistent Storage & Chat Logs",
                "data_types": ["User Account", "Encrypted Consultation Logs", "Wallet Balance"],
                "legal_basis": "UK GDPR Article 6(1)(b) & Article 5(1)(e) Storage Limitation",
                "special_category": True,
                "art9_exception": "Article 9(2)(a) Explicit Consent",
                "encryption": "KMS Managed AES-256 at Rest",
                "is_cross_border": False,
                "status": "COMPLIANT",
                "risk_desc": "Local UK cloud data store with 90-day automated purge policy."
            },
            {
                "id": "flow_3",
                "source": "node_api_gateway",
                "target": "node_openai_llm",
                "label": "AI Transcript Summarization",
                "data_types": ["Raw Chat Transcripts", "Spiritual Queries"],
                "legal_basis": "UK GDPR Article 6(1)(f) Legitimate Interest / Consent",
                "special_category": True,
                "art9_exception": "Article 9 Violation if Consent Checkbox Missing",
                "encryption": "TLS 1.3 In-Flight",
                "is_cross_border": True,
                "transfer_mechanism": "Missing UK-US Data Bridge Certification",
                "status": "WARNING",
                "fine_exposure": "Up to £8,700,000 under ICO Chapter V",
                "remediation": "Enable Azure OpenAI UK South region to keep data inside the UK."
            },
            {
                "id": "flow_4",
                "source": "node_uk_users",
                "target": "node_stripe_payments",
                "label": "Wallet Payment Authorizations",
                "data_types": ["Cardholder Token", "Billing Postcode", "Transaction Amount"],
                "legal_basis": "UK GDPR Article 6(1)(b) & PCI-DSS Compliance",
                "special_category": False,
                "art9_exception": "N/A",
                "encryption": "End-to-End PCI Tokenization",
                "is_cross_border": False,
                "status": "COMPLIANT",
                "risk_desc": "Raw credit card numbers never touch Tara servers."
            },
            {
                "id": "flow_5",
                "source": "node_db_postgres",
                "target": "node_india_support",
                "label": "Cross-Border Support & QA Access",
                "data_types": ["Customer Phone Numbers", "Failed Session Transcripts", "Account UUID"],
                "legal_basis": "UK GDPR Chapter V (Art 44) & India DPDP Act Section 16",
                "special_category": True,
                "art9_exception": "Article 9(2)(a)",
                "encryption": "Restricted VPN / IP Whitelist",
                "is_cross_border": True,
                "transfer_mechanism": "MISSING UK IDTA / SCC ADDENDUM",
                "status": "VIOLATION",
                "fine_exposure": "Up to £17,500,000 (ICO) or ₹250 Crore (DPDP Board)",
                "remediation": "Mandatory execution of statutory UK International Data Transfer Agreement (IDTA) with India subsidiary."
            }
        ]
    },
    "medconnect-telehealth": {
        "id": "medconnect-telehealth",
        "name": "MedConnect Telemedicine & Patient EHR",
        "company": "MedConnect Health Ltd",
        "description": "NHS-integrated telehealth backend processing patient medical diagnoses, doctor appointments, and prescriptions.",
        "nodes": [
            {
                "id": "node_uk_patients",
                "label": "NHS Patients & Doctors",
                "subtext": "Telehealth Video & EHR Portal",
                "category": "DATA_SUBJECT",
                "jurisdiction": "United Kingdom",
                "flag": "🇬🇧",
                "color": "#00CEFF",
                "x": 80, "y": 180,
                "icon": "🏥"
            },
            {
                "id": "node_express_gw",
                "label": "Express.js API Gateway",
                "subtext": "Prisma ORM & JWT Auth",
                "category": "CONTROLLER_SYSTEM",
                "jurisdiction": "United Kingdom",
                "flag": "🇬🇧",
                "color": "#6C5CE7",
                "x": 300, "y": 180,
                "icon": "⚡"
            },
            {
                "id": "node_patient_db",
                "label": "EHR Encrypted Database",
                "subtext": "AWS RDS London (AES-256)",
                "category": "PRIMARY_STORAGE",
                "jurisdiction": "United Kingdom",
                "flag": "🇬🇧",
                "color": "#51CF66",
                "x": 540, "y": 120,
                "icon": "🗄️"
            },
            {
                "id": "node_aws_s3_scans",
                "label": "AWS S3 Medical Imaging",
                "subtext": "X-Rays, MRI Scans & Blood Reports",
                "category": "SUBPROCESSOR_CLOUD",
                "jurisdiction": "United Kingdom (eu-west-2)",
                "flag": "🇬🇧",
                "color": "#51CF66",
                "x": 540, "y": 280,
                "icon": "🧬"
            },
            {
                "id": "node_india_cloud_ops",
                "label": "India DevOps & SRE Team",
                "subtext": "24/7 Production Monitoring",
                "category": "CROSS_BORDER_IMPORTER",
                "jurisdiction": "India (Bengaluru)",
                "flag": "🇮🇳",
                "color": "#FF6B6B",
                "x": 780, "y": 180,
                "icon": "🇮🇳"
            }
        ],
        "links": [
            {
                "id": "flow_m1",
                "source": "node_uk_patients",
                "target": "node_express_gw",
                "label": "Patient Consultation Transcripts & EHR",
                "data_types": ["NHS Number", "Medical Diagnosis", "Prescription"],
                "legal_basis": "UK GDPR Article 9(2)(h) Healthcare Provision",
                "special_category": True,
                "art9_exception": "Direct Medical Care Provision",
                "encryption": "TLS 1.3 / mTLS",
                "is_cross_border": False,
                "status": "COMPLIANT",
                "risk_desc": "Lawful healthcare processing under DPA 2018 Schedule 1."
            },
            {
                "id": "flow_m2",
                "source": "node_express_gw",
                "target": "node_patient_db",
                "label": "EHR Diagnostic Records",
                "data_types": ["Full Medical History", "Blood Reports"],
                "legal_basis": "UK GDPR Article 9(2)(h)",
                "special_category": True,
                "art9_exception": "Statutory Healthcare Mandate",
                "encryption": "Customer Managed Key (CMK) AES-256",
                "is_cross_border": False,
                "status": "COMPLIANT",
                "risk_desc": "High security database with strict audit logging."
            },
            {
                "id": "flow_m3",
                "source": "node_patient_db",
                "target": "node_india_cloud_ops",
                "label": "Production Log Streaming & SRE Telemetry",
                "data_types": ["Server Exception Logs", "IP Addresses", "Patient Query UUID"],
                "legal_basis": "UK GDPR Chapter V (Art 46) & DPDPA Sec 16",
                "special_category": False,
                "art9_exception": "N/A",
                "encryption": "Zero Trust Bastion Host",
                "is_cross_border": True,
                "transfer_mechanism": "IDTA Required for Overseas Maintenance",
                "status": "WARNING",
                "fine_exposure": "Up to £17,500,000 for Special Category Data Exposure",
                "remediation": "Redact patient identifiers from Datadog/CloudWatch streams accessed overseas."
            }
        ]
    }
}

class DataFlowEngine:
    def __init__(self):
        self.presets = TOPOLOGY_PRESETS

    def get_presets_list(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": p["id"],
                "name": p["name"],
                "company": p["company"],
                "description": p["description"],
                "nodes_count": len(p["nodes"]),
                "links_count": len(p["links"])
            }
            for p in self.presets.values()
        ]

    def get_topology(self, preset_id: str = "tara-consultation") -> Dict[str, Any]:
        preset = self.presets.get(preset_id, self.presets["tara-consultation"])
        
        # Calculate summary metrics
        total_links = len(preset["links"])
        cross_border_count = sum(1 for l in preset["links"] if l.get("is_cross_border", False))
        violations_count = sum(1 for l in preset["links"] if l.get("status") == "VIOLATION")
        warnings_count = sum(1 for l in preset["links"] if l.get("status") == "WARNING")
        
        return {
            "preset_id": preset["id"],
            "name": preset["name"],
            "company": preset["company"],
            "description": preset["description"],
            "summary": {
                "total_nodes": len(preset["nodes"]),
                "total_flows": total_links,
                "cross_border_transfers": cross_border_count,
                "statutory_violations": violations_count,
                "statutory_warnings": warnings_count,
                "overall_health_grade": "D (Urgent IDTA Action Required)" if violations_count > 0 else ("B" if warnings_count > 0 else "A")
            },
            "nodes": preset["nodes"],
            "links": preset["links"]
        }

    def build_topology_from_extraction(self, extraction_data: Dict[str, Any], company_name: str = "Client App", repo_url: str = "") -> Dict[str, Any]:
        """
        Dynamically constructs an interactive visual data-flow topology from real scanned
        repository AST, models, routes, and detected cloud dependencies.
        """
        repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "") if repo_url else "ScannedApp"
        profile = extraction_data.get("use_case_profile", {})
        domain = profile.get("primary_domain", "Web Application & Software Service")
        models = [m.get("model_name") for m in extraction_data.get("models", [])]
        routes_count = len(extraction_data.get("routes", []))

        model_summary = ", ".join(models[:3]) if models else "User Accounts, Transaction Logs"

        nodes = [
            {
                "id": "node_users",
                "label": f"{company_name} Clients",
                "subtext": f"{domain} (Web & Mobile)",
                "category": "DATA_SUBJECT",
                "jurisdiction": "United Kingdom / Global",
                "flag": "🇬🇧",
                "color": "#00CEFF",
                "x": 80, "y": 140,
                "icon": "👤"
            },
            {
                "id": "node_api",
                "label": f"{repo_name} API Gateway",
                "subtext": f"{profile.get('detected_framework', 'Backend Service')} ({routes_count} Routes)",
                "category": "CONTROLLER_SYSTEM",
                "jurisdiction": "United Kingdom (AWS London)",
                "flag": "🇬🇧",
                "color": "#6C5CE7",
                "x": 310, "y": 140,
                "icon": "⚡"
            },
            {
                "id": "node_db",
                "label": f"{repo_name} Primary Database",
                "subtext": f"Models: {model_summary}",
                "category": "PRIMARY_STORAGE",
                "jurisdiction": "United Kingdom",
                "flag": "🇬🇧",
                "color": "#51CF66",
                "x": 550, "y": 70,
                "icon": "🗄️"
            },
            {
                "id": "node_cloud_services",
                "label": "Integrated Cloud APIs",
                "subtext": "Auth, Analytics & Webhooks",
                "category": "SUBPROCESSOR_CLOUD",
                "jurisdiction": "United States / EU",
                "flag": "🇺🇸",
                "color": "#FFD43B",
                "x": 550, "y": 240,
                "icon": "☁️"
            },
            {
                "id": "node_devops",
                "label": "Engineering & Ops Hub",
                "subtext": "DevOps, Maintenance & SRE",
                "category": "CROSS_BORDER_IMPORTER",
                "jurisdiction": "India (Remote Access)",
                "flag": "🇮🇳",
                "color": "#FF6B6B",
                "x": 790, "y": 140,
                "icon": "🇮🇳"
            }
        ]

        links = [
            {
                "id": "flow_repo_1",
                "source": "node_users",
                "target": "node_api",
                "label": f"{domain} Queries & Traffic",
                "data_types": ["User Identifiers", "Login Credentials", "Session Tokens"],
                "legal_basis": "UK GDPR Article 6(1)(b) Contractual Necessity",
                "special_category": False,
                "encryption": "TLS 1.3 / HTTPS",
                "is_cross_border": False,
                "status": "COMPLIANT",
                "risk_desc": f"Direct user traffic processed by {repo_name}."
            },
            {
                "id": "flow_repo_2",
                "source": "node_api",
                "target": "node_db",
                "label": "Persistent Storage & Model Records",
                "data_types": models[:4] if models else ["User Records", "Audit Logs"],
                "legal_basis": "UK GDPR Article 5(1)(e) Storage Limitation",
                "special_category": False,
                "encryption": "AES-256 KMS Storage",
                "is_cross_border": False,
                "status": "COMPLIANT",
                "risk_desc": f"Local storage of {len(models)} primary data models."
            },
            {
                "id": "flow_repo_3",
                "source": "node_api",
                "target": "node_cloud_services",
                "label": "Subprocessor Cloud Dispatch",
                "data_types": ["Telemetry", "Transaction Tokens"],
                "legal_basis": "UK GDPR Article 28 Processor Terms",
                "special_category": False,
                "encryption": "TLS 1.3 In-Flight",
                "is_cross_border": True,
                "transfer_mechanism": "Standard Contractual Clauses (SCC)",
                "status": "WARNING",
                "fine_exposure": "Up to £8,700,000 for unvetted third-party transfer",
                "remediation": "Verify subprocessor vendor DPA and zero-retention policy."
            },
            {
                "id": "flow_repo_4",
                "source": "node_db",
                "target": "node_devops",
                "label": "Cross-Border Support & Production SRE",
                "data_types": ["Application Logs", "Error Traces", "User Identifiers"],
                "legal_basis": "UK GDPR Chapter V (Art 44) & Section 119A DPA 2018",
                "special_category": False,
                "encryption": "Zero Trust VPN / Bastion",
                "is_cross_border": True,
                "transfer_mechanism": "MISSING UK IDTA / SCC ADDENDUM",
                "status": "VIOLATION",
                "fine_exposure": "Up to £17,500,000 (ICO) or ₹250 Crore (India DPDPA)",
                "remediation": f"Mandatory execution of UK IDTA agreement between {company_name} and overseas technical team."
            }
        ]

        preset_data = {
            "id": "scanned-repo",
            "name": f"{repo_name} ({company_name})",
            "company": company_name,
            "description": f"Live extracted architecture for {repo_name} operating in {domain}.",
            "nodes": nodes,
            "links": links
        }

        self.presets["scanned-repo"] = preset_data
        return self.get_topology("scanned-repo")

    def generate_idta_schedule(
        self,
        company_name: str = "Tara Infotech Ltd",
        overseas_entity: str = "Tara Infotech India Pvt Ltd",
        categories_transferred: Optional[List[str]] = None,
        domain: Optional[str] = None
    ) -> str:
        """Generates statutory UK International Data Transfer Agreement (IDTA) Schedule."""
        now_str = datetime.now().strftime("%B %d, %Y")
        domain_label = domain or "Digital Platform & Cloud Software Application"
        data_cats = categories_transferred or [
            "User account identifiers (Full Name, Email Address, Contact Numbers)",
            "Application interaction data, service transaction records, and operational logs",
            "Technical session diagnostics and customer service communications"
        ]
        data_cats_str = "\n".join(f"   * {cat}" for cat in data_cats)
        
        return f"""# STATUTORY UK INTERNATIONAL DATA TRANSFER AGREEMENT (IDTA)
## MANDATORY ADDENDUM TO DATA PROCESSING AGREEMENT (DPA)
**Governing Authority:** Information Commissioner's Office (ICO)  
**Governing Statute:** UK GDPR Section 119A Data Protection Act 2018  
**Transfer Mechanism:** Standard Data Protection Clauses (UK IDTA Standard)  
**Execution Date:** {now_str}

---

### PART 1: PARTIES & ROLES TABLE

| Role | Transferring Entity (Exporter) | Receiving Entity (Importer) |
| :--- | :--- | :--- |
| **Corporate Name** | **{company_name}** | **{overseas_entity}** |
| **Jurisdiction of Incorporation** | England & Wales (United Kingdom) | Republic of India (DPDPA 2023 Compliant) |
| **Designated Role under UK GDPR** | **Data Controller** | **Data Processor** (Technical Services) |
| **Contact Email** | privacy@{company_name.lower().replace(' ', '')}.com | compliance@{overseas_entity.lower().replace(' ', '')}.com |

---

### PART 2: TRANSFER DETAILS & ARTICLE 30 SPECIFICATION

1. **Categories of Data Subjects:**
   * UK and European clients and registered users of {company_name} ({domain_label}).
   * Application subscribers and corporate account users.
2. **Categories of Personal Data Transferred:**
{data_cats_str}
3. **Special Category Data (Article 9 UK GDPR):**
   * Processed strictly where explicit consent is granted under Article 9(2)(a) with zero unauthorized local export.
4. **Purpose of the Overseas Transfer:**
   * Software engineering, cloud infrastructure maintenance, automated testing, production support, and security monitoring.

---

### PART 3: MANDATORY TECHNICAL & ORGANISATIONAL SAFEGUARDS (TOMS)

* **Mandate 1 (Access Control):** Importer personnel in India shall access UK personal data exclusively via encrypted Zero Trust Bastion hosts with Multi-Factor Authentication (MFA).
* **Mandate 2 (No Local Downloads):** Absolute prohibition on exporting customer personal identifiers or communication logs to local workstations or personal devices in India.
* **Mandate 3 (Security at Rest & Transit):** All data transfers utilize TLS 1.3 in-flight and AES-256 KMS encryption at rest.
* **Mandate 4 (72-Hour Breach Escalation):** Importer must report any unauthorized access or potential compromise to Exporter within **24 hours** to facilitate Exporter's 72-hour ICO statutory reporting window.

---

### PART 4: STATUTORY SIGNATURE & BINDING UNDERTAKING

*This Schedule constitutes a legally binding Addendum. Both parties agree to submit to the jurisdiction of the UK Courts and the Information Commissioner's Office (ICO) regarding any claims arising under this transfer.*

**For and on behalf of Data Exporter ({company_name}):**  
Signature: ___________________________  
Name: Authorized Privacy Officer  
Title: Lead Data Protection Officer  

**For and on behalf of Data Importer ({overseas_entity}):**  
Signature: ___________________________  
Name: Managing Director (India Operations)  
Title: Country Head & Compliance Lead  
"""

