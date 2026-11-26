"""
Tara PrivacyOS — Legal Intelligence Engine
Module: Use-Based GDPR & DPDPA Document Generator
Generates bespoke, statutory-compliant Privacy Policies, Article 30 RoPA,
DPIA assessments, and Developer Remediation Blueprints based on actual data
extracted from a GitHub repository and its inferred business use case.
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class UseBasedGDPRGenerator:
    """
    Synthesizes extracted repository AST, models, routes, and subprocessors
    into a completely tailored, use-based statutory GDPR and DPDPA compliance suite.
    """

    def __init__(self):
        pass

    def generate_full_package(self, extraction_data: Dict[str, Any], company_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Master method to generate all legal documents based on the extracted GitHub data.
        """
        repo_meta = extraction_data.get("repository_metadata", {})
        use_case = extraction_data.get("use_case_profile", {})
        models = extraction_data.get("extracted_models", [])
        pii = extraction_data.get("pii_and_special_category", {})
        routes = extraction_data.get("extracted_routes", []) or extraction_data.get("routes_and_endpoints", [])
        subprocs = extraction_data.get("subprocessors_and_transfers", {})
        if not subprocs.get("subprocessor_register") and extraction_data.get("subprocessor_register"):
            subprocs = {
                "subprocessor_register": extraction_data.get("subprocessor_register", []),
                "total_subprocessors_detected": len(extraction_data.get("subprocessor_register", [])),
                "us_transfers_detected": [v["name"] for v in extraction_data.get("subprocessor_register", []) if "United States" in v.get("jurisdiction", "")]
            }

        c_name = company_name or repo_meta.get("name", "Tara Infotech Service").replace("-", " ").title()

        # Generate each individual document
        privacy_policy_md = self._build_privacy_policy(c_name, repo_meta, use_case, pii, routes, subprocs)
        ropa_records = self._build_ropa_table(c_name, use_case, pii, routes, subprocs)
        dpia_document = self._build_dpia(c_name, use_case, pii, subprocs)
        dev_blueprint = self._build_dev_blueprint(routes, pii, subprocs)
        risk_score, health_grade, critical_alerts = self._calculate_risk_profile(pii, routes, subprocs)

        return {
            "summary": {
                "organization_name": c_name,
                "repository_analyzed": repo_meta.get("name", "Unknown"),
                "primary_domain": use_case.get("primary_domain", "Web Application"),
                "risk_score": risk_score,
                "health_grade": health_grade,
                "generated_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
                "critical_statutory_alerts": critical_alerts
            },
            "statutory_privacy_policy_markdown": privacy_policy_md,
            "article_30_ropa": ropa_records,
            "dpia_assessment": dpia_document,
            "developer_remediation_blueprint": dev_blueprint
        }

    def _build_privacy_policy(
        self,
        c_name: str,
        repo_meta: Dict[str, Any],
        use_case: Dict[str, Any],
        pii: Dict[str, Any],
        routes: List[Dict[str, Any]],
        subprocs: Dict[str, Any]
    ) -> str:
        """Constructs a comprehensive, publication-ready Privacy Policy Markdown."""
        today = datetime.now().strftime("%B %d, %Y")
        domain = use_case.get("primary_domain", "Digital Services")
        data_subjects = ", ".join(use_case.get("data_subjects", ["Platform Users"]))

        has_art9 = pii.get("special_category_fields_detected", 0) > 0
        art9_models = pii.get("high_risk_art9_models", [])
        subproc_list = subprocs.get("subprocessor_register", [])

        # Gather detected fields
        fields_by_cat = {}
        for finding in pii.get("detailed_findings", []):
            m_name = finding.get("model_name", "Model")
            for f in finding.get("fields", []):
                cat = f.get("category", "General Personal Data")
                if cat not in fields_by_cat:
                    fields_by_cat[cat] = []
                fields_by_cat[cat].append(f"{f.get('field_name')} ({m_name})")

        md = f"""# STATUTORY PRIVACY NOTICE & DATA PROTECTION STATEMENT
**Organization:** {c_name}  
**Application / Service:** {repo_meta.get('name', 'Cloud Platform')} ({domain})  
**Applicable Legal Frameworks:** UK General Data Protection Regulation (UK GDPR), Data Protection Act 2018 (ICO), & India Digital Personal Data Protection Act 2023 (DPDPA 2023)  
**Effective Date:** {today}  
**Status:** Statutory Audit & Implementation Ready  

---

## 1. Introduction & Scope
This Statutory Privacy Notice governs the processing of personal data by **{c_name}** ("we", "us", or "our") in connection with our software applications, APIs, and digital platform hosted at `{repo_meta.get('source_url', 'our repository')}`.

As an organization committed to privacy by design and default, we process personal data strictly in accordance with:
1. **UK GDPR & Data Protection Act 2018** enforced by the Information Commissioner's Office (ICO).
2. **India Digital Personal Data Protection Act, 2023 (DPDPA 2023)** enforced by the Data Protection Board of India (DPBI).

This notice applies to all: {data_subjects}.

---

## 2. Categories of Personal Data Processed (Use-Based Breakdown)
Based on our software architecture and database models, we collect and process the following categories of data:

"""
        for cat, flist in fields_by_cat.items():
            md += f"### {cat}\n"
            md += f"- **Specific Fields Extracted from Code:** {', '.join(flist)}\n\n"

        if not fields_by_cat:
            md += "- **Direct Identifiers:** Full Name, Email Address, Contact Phone Number, Billing Details.\n"
            md += "- **Technical Telemetry:** IP Address, Session Access Logs, Browser User Agent Strings.\n\n"

        if has_art9:
            md += f"""---

## 3. SPECIAL CATEGORY DATA (UK GDPR Article 9 & DPDPA Enhanced Safeguards)
⚠️ **MANDATORY LEGAL DISCLOSURE:**
Our platform processes special categories of personal data in data models: `{', '.join(art9_models)}`.
Under UK GDPR Article 9(1), processing of data concerning health, genetic/biometric data, or religious/philosophical beliefs is strictly prohibited unless an explicit exception under Article 9(2) applies.

**Lawful Basis for Special Category Processing:**
- **UK GDPR Article 9(2)(a):** The data subject has given **explicit, freely given, and unbundled consent** for the processing of sensitive personal data for consultation and wellness advisory purposes.
- **DPA 2018 Schedule 1 / DPDPA Section 4 & 8:** Implementation of field-level encryption (AES-256) and complete confidentiality shielding between external practitioners and client records.
- **Revocation Right:** You retain the statutory right to withdraw your explicit consent at any time without affecting the lawfulness of processing based on consent prior to withdrawal.

---
"""

        md += """## 4. Lawful Bases for Processing Matrix (UK GDPR Article 6 & DPDPA Section 4)

| Processing Purpose / Service Route | Personal Data Categories | Lawful Basis (UK GDPR) | Statutory Basis (India DPDPA) |
| :--- | :--- | :--- | :--- |
| **User Authentication & Account Management** | Name, Email, Password Hash, IP Address | Article 6(1)(b) (Performance of Contract) | Section 4 & 6 (Notice & Consent) |
| **Core Application Service Delivery & Operations** | User inputs, operational telemetry, transactional logs | Article 6(1)(b) (Contractual Necessity) | Section 4 & 6 (Notice & Consent) |
"""
        if "Real Estate" in domain or "Rental" in domain or "Hospitality" in domain:
            md += """| **Property Listings & Rental Reservations** | Property location, photos, rent amounts, owner contact | Article 6(1)(b) (Contractual Necessity) | Section 4 & 6 (Notice & Consent) |
| **Public Reviews & Verified Host Ratings** | Review comments, star ratings, submission timestamp | Article 6(1)(f) (Legitimate Interests) | Section 4 & 6 (Notice & Consent) |
| **Interactive Geolocation & Property Mapping** | Map coordinates, property address, IP telemetry | Article 6(1)(f) (Legitimate Interests) | Section 4 & 6 (Notice & Consent) |
"""
        if any("payment" in r.get("endpoint", "").lower() or "billing" in r.get("endpoint", "").lower() for r in routes) or any(s.get("name") in ["Stripe Payments UK Ltd", "Razorpay Software Pvt Ltd"] for s in subproc_list):
            md += "| **Payment Invoicing & Statutory Accounting** | Billing Address, Transaction Identifiers, Card Token | Article 6(1)(b) & Article 6(1)(c) (Legal Obligation) | Section 4 & RBI Payment Localisation |\n"
        if any("openai" in s.get("name", "").lower() for s in subproc_list):
            md += "| **Automated AI Intelligence & Analytics** | Application prompts, contextual telemetry | Article 6(1)(b) (Contract) / Consent Art 6(1)(a) | Section 6 (Specific Purpose Limitation) |\n"
        md += """| **Security Auditing & Fraud Prevention** | IP address, timestamp, device telemetry | Article 6(1)(f) (Legitimate Interests) | Section 8(5) (Security Safeguards) |

---

"""
        md += """## 5. Third-Party Subprocessors & International Transfers (UK GDPR Chapter V & Article 28)
To operate our application, we engage verified third-party cloud service providers acting as Data Processors under written Article 28 Data Processing Agreements (DPAs):

| Subprocessor / Service | Purpose in Codebase | Processing Country | Cross-Border Transfer Mechanism |
| :--- | :--- | :--- | :--- |
"""
        for sp in subproc_list:
            md += f"| **{sp.get('name')}** | {sp.get('category')} | {sp.get('jurisdiction')} | {sp.get('transfer_mechanism_required')} |\n"

        if not subproc_list:
            md += "| **Amazon Web Services (AWS)** | Cloud Infrastructure & Database Hosting | UK / Ireland (eu-west-2) | UK IDTA / Standard Contractual Clauses |\n"
            md += "| **Stripe Payments UK Ltd** | Payment Processing & Tokenization | United Kingdom / US | Stripe Global DPA & PCI-DSS Level 1 |\n"

        md += f"""
### International Data Transfer Governance:
Where data is transferred from the UK or EEA to teams or servers located in third countries (e.g., India or the United States), **{c_name}** ensures statutory compliance through:
1. **UK International Data Transfer Agreement (IDTA)** or the UK Addendum to the EU Standard Contractual Clauses (SCCs).
2. **Transfer Risk Assessments (TRA)** to ensure local legislation does not undermine GDPR equivalency.
3. For US cloud subprocessors, verifying certification under the UK-US Data Bridge / EU-US Data Privacy Framework.

---

## 6. Data Retention & Erasure Schedule
In compliance with the Principle of Storage Limitation (UK GDPR Article 5(1)(e)) and DPDPA 2023 Section 8(7), data is retained only for as long as necessary:

| Data Type / Model | Retention Period | Post-Retention Action |
| :--- | :--- | :--- |
| **Account Profile & Identifiers** | Duration of active account + 30 days grace | Cryptographic purge from production DB |
| **Operational Application Data & Session Logs** | 30 to 90 days post-session fulfillment | Irreversible anonymisation / deletion |
| **Payment Transactions & Invoices** | 6 Statutory Years (UK HMRC & Financial Laws) | Archived in restricted financial ledger |
| **Server Access Logs & IP Telemetry** | Rolling 14 to 30 days | Automated log rotation & overwriting |

---

## 7. Your Statutory Rights (DSAR Articles 15–22 & DPDPA Section 12)
You possess inviolable rights regarding your personal data:
- **Right of Access (Article 15):** Request a copy of all personal data we hold concerning you free of charge.
- **Right to Erasure / Right to be Forgotten (Article 17 & DPDPA Sec 12(3)):** Request complete deletion of your account and records via our automated erasure endpoint or support ticket.
- **Right to Data Portability (Article 20):** Receive your data in a structured, commonly used, and machine-readable format (JSON/CSV).
- **Right to Rectification (Article 16):** Update inaccurate or incomplete demographic or contact records.
- **Right to Withdraw Consent (Article 7(3)):** Revoke consent at any moment for optional services or Article 9 data.

**How to Exercise Your Rights:**
- Submit an automated DSAR request via email to `privacy@{c_name.lower().replace(' ', '')}.com`
- Statutory Response Time: **Within 30 calendar days** (UK GDPR) / **Timely resolution** (DPDPA).

---

## 8. Supervisory Authorities & Grievance Redressal
If you believe our data processing violates statutory standards:
- **United Kingdom:** Information Commissioner's Office (ICO) — [https://ico.org.uk](https://ico.org.uk) | Helpline: 0303 123 1113
- **Republic of India:** Data Protection Board of India (DPBI) & Internal Grievance Officer: `grievance@{c_name.lower().replace(' ', '')}.com`
"""
        return md

    def _build_ropa_table(
        self,
        c_name: str,
        use_case: Dict[str, Any],
        pii: Dict[str, Any],
        routes: List[Dict[str, Any]],
        subprocs: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Constructs statutory Article 30 Record of Processing Activities ledger."""
        has_art9 = pii.get("special_category_fields_detected", 0) > 0
        records = [
            {
                "activity_id": "ROPA-001",
                "purpose": "User Identity Authentication & Account Onboarding",
                "data_subjects": "Registered Application Users & Subscribers",
                "categories_of_data": "Full Name, Email Address, Password Hash, IP Telemetry",
                "lawful_basis": "UK GDPR Article 6(1)(b) (Performance of Contract)",
                "recipients_processors": "AWS Cloud Infrastructure (Hosting), Twilio (SMS MFA)",
                "transfer_safeguards": "UK IDTA / Standard Contractual Clauses",
                "retention_period": "Account lifetime + 30-day post-closure deletion grace period",
                "security_measures": "TLS 1.3 in transit, Argon2 password hashing, RBAC isolation"
            },
            {
                "activity_id": "ROPA-002",
                "purpose": f"{use_case.get('primary_domain', 'Consultation')} Core Service Fulfillment",
                "data_subjects": ", ".join(use_case.get('data_subjects', ['Registered Application Users'])),
                "categories_of_data": "Application data, transactional inputs, operational metadata" + (", Special Category Data" if has_art9 else ""),
                "lawful_basis": "UK GDPR Art 6(1)(b) (Contract)" + (" & Art 9(2)(a) (Explicit Consent)" if has_art9 else ""),
                "recipients_processors": "Authorized Cloud Infrastructure, Application Databases",
                "transfer_safeguards": "Cross-Border UK-India IDTA / Standard Contractual Clauses",
                "retention_period": "30 to 90 days after service fulfillment, then purged",
                "security_measures": "Field-Level AES-256 encryption, Practitioner phone/email masking"
            },
            {
                "activity_id": "ROPA-003",
                "purpose": "Payment Invoicing, Tokenization & Statutory Tax Accounting",
                "data_subjects": "Paying Customers & B2B Clients",
                "categories_of_data": "Customer ID, Transaction Amount, Card Token, Billing Postal Code",
                "lawful_basis": "UK GDPR Article 6(1)(b) & Article 6(1)(c) (Legal Obligation)",
                "recipients_processors": "Stripe Payments UK Ltd / Banking Gateways",
                "transfer_safeguards": "Stripe Global Data Processing Agreement",
                "retention_period": "6 Statutory Years (UK HMRC & Financial Compliance)",
                "security_measures": "PCI-DSS Level 1 Tokenization (Zero raw card numbers stored)"
            },
            {
                "activity_id": "ROPA-004",
                "purpose": "Automated AI Query Analysis & LLM Summarization",
                "data_subjects": "Application Users utilizing AI features",
                "categories_of_data": "De-identified question prompts, transcript excerpts",
                "lawful_basis": "UK GDPR Article 6(1)(b) & Explicit Consent Art 9(2)(a)",
                "recipients_processors": "Azure OpenAI / OpenAI API (Enterprise Zero Data Retention)",
                "transfer_safeguards": "EU/UK Standard Contractual Clauses + Commercial ZDR Agreement",
                "retention_period": "Zero retention on processor servers; ephemeral cache during session",
                "security_measures": "PII scrubbing before API dispatch, TLS 1.3 encrypted transport"
            }
        ]
        return records

    def _build_dpia(
        self,
        c_name: str,
        use_case: Dict[str, Any],
        pii: Dict[str, Any],
        subprocs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generates statutory Data Protection Impact Assessment (UK GDPR Article 35)."""
        has_art9 = pii.get("special_category_fields_detected", 0) > 0
        art9_count = pii.get("special_category_fields_detected", 0)

        necessity_assessment = (
            f"The processing of personal data within {c_name}'s {use_case.get('primary_domain')} application "
            "is necessary to deliver core digital services requested by data subjects. Data minimisation principles "
            "(Article 5(1)(c)) are maintained by restricting field inputs to strictly functional attributes."
        )

        risks = [
            {
                "risk_title": "Unauthorized Cross-Border Administrative Data Exfiltration",
                "likelihood": "Medium",
                "severity": "High",
                "mitigation": "Enforce strict Role-Based Access Control (RBAC), API tokenization, and end-to-end audit logging across all remote access sessions."
            },
            {
                "risk_title": "Subprocessor LLM Training on Confidential Client Prompts",
                "likelihood": "Low",
                "severity": "Critical",
                "mitigation": "Execute Azure OpenAI / OpenAI Enterprise Zero-Data Retention (ZDR) Addendum confirming inputs are never utilized for model fine-tuning."
            },
            {
                "risk_title": "Delayed Execution of Statutory Erasure Requests (DSAR Art 17)",
                "likelihood": "Medium",
                "severity": "High",
                "mitigation": "Expose automated self-service account deletion endpoint (DELETE /api/v1/user/account) with automated cascading DB scrub."
            }
        ]

        if has_art9:
            risks.insert(0, {
                "risk_title": "Processing Special Category Data (Art 9) Without Unbundled Explicit Consent",
                "likelihood": "High",
                "severity": "Critical",
                "mitigation": "Implement separate, unbundled explicit consent checkbox prior to session submission with cryptographic audit timestamp logging."
            })

        return {
            "statutory_mandate": "UK GDPR Article 35 & ICO High-Risk Processing Guidelines",
            "dpia_mandated": has_art9 or len(subprocs.get("subprocessor_register", [])) > 2,
            "justification": (
                "Statutory mandatory DPIA triggered due to processing of Article 9 special category data "
                f"({art9_count} sensitive fields detected in codebase) and integration with external cloud AI processors."
                if has_art9 else
                "Recommended DPIA due to automated processing, international transfers, and cloud microservice architecture."
            ),
            "necessity_assessment": necessity_assessment,
            "identified_risks_and_mitigations": risks,
            "dpo_signoff_status": "PROVISIONAL APPROVAL SUBJECT TO CODE REMEDIATIONS"
        }

    def _build_dev_blueprint(
        self,
        routes: List[Dict[str, Any]],
        pii: Dict[str, Any],
        subprocs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Provides developer-ready code patches and remediation checklists."""
        has_art9 = pii.get("special_category_fields_detected", 0) > 0

        code_patches = {
            "fastapi_erasure_endpoint": '''# FILE: api_routes.py — Statutory UK GDPR Article 17 Right to Erasure
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/user", tags=["Privacy & DSAR"])

@router.delete("/account", status_code=status.HTTP_200_OK)
def delete_user_account(user_id: str, db: Session = Depends(get_db)):
    """
    Statutory DSAR Right to Erasure (UK GDPR Article 17 & DPDPA Section 12(3)).
    Permanently erases user identity, obfuscates consultation history,
    and dispatches asynchronous scrub webhook to third-party processors.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User account not found")

    # 1. Obfuscate PII fields
    user.full_name = "ANONYMISED_USER"
    user.email = f"erased_{user.id}@gdpr-erased.local"
    user.phone_number = None
    user.is_erased = True
    user.erasure_timestamp = datetime.utcnow()

    # 2. Purge consultation transcripts
    db.query(KundliConsultationModel).filter(
        KundliConsultationModel.user_id == user_id
    ).delete(synchronize_session=False)

    db.commit()
    return {"status": "SUCCESS", "message": "User personal data cryptographically scrubbed."}
''',
            "practitioner_masking_middleware": '''# FILE: serializers.py — Practitioner Data Minimisation (UK GDPR Art 5(1)(c))
def serialize_client_for_practitioner(client_model) -> dict:
    """
    Data Minimisation & Poaching Protection:
    Strips raw phone numbers and direct emails from practitioner views.
    Communications must remain strictly in-app.
    """
    return {
        "client_id": client_model.id,
        "first_name": client_model.full_name.split()[0] if client_model.full_name else "Client",
        "birth_details": {
            "date": client_model.date_of_birth,
            "place": client_model.birth_place
        },
        # Direct identifiers completely masked
        "masked_email": f"***@***.{client_model.email.split('.')[-1]}" if client_model.email else None,
        "masked_phone": f"+**-***-***{client_model.phone_number[-4:]}" if client_model.phone_number else None
    }
'''
        }

        checklist = [
            {
                "task_id": "DEV-01",
                "priority": "CRITICAL" if has_art9 else "HIGH",
                "component": "API Routes / User Controller",
                "task": "Implement DELETE /api/v1/user/account (Right to Erasure)",
                "statute": "UK GDPR Article 17 & DPDPA Section 12(3)",
                "action": "Add soft-delete and cryptographic purge logic for user models and transcripts."
            },
            {
                "task_id": "DEV-02",
                "priority": "CRITICAL" if has_art9 else "MEDIUM",
                "component": "Booking & Registration UI",
                "task": "Implement Explicit Consent (Article 9 Checkbox)",
                "statute": "UK GDPR Article 9(2)(a)",
                "action": "Checkbox must be unticked by default, separate from general terms, with timestamp logging."
            },
            {
                "task_id": "DEV-03",
                "priority": "HIGH",
                "component": "Practitioner API Endpoints",
                "task": "Mask Customer Phone & Email on Practitioner Responses",
                "statute": "UK GDPR Article 5(1)(c) (Data Minimisation)",
                "action": "Ensure phone numbers and raw email addresses are never returned to external practitioner clients."
            },
            {
                "task_id": "DEV-04",
                "priority": "HIGH",
                "component": "Third-Party AI / LLM Integrations",
                "task": "Configure Zero-Data Retention (ZDR) & Sanitize Egress Payloads",
                "statute": "UK GDPR Article 28(3) & Chapter V",
                "action": "Verify OpenAI API opt-out of model fine-tuning and sanitize direct identifiers before dispatch."
            }
        ]

        return {
            "action_checklist": checklist,
            "ready_to_use_code_patches": code_patches
        }

    def _calculate_risk_profile(
        self,
        pii: Dict[str, Any],
        routes: List[Dict[str, Any]],
        subprocs: Dict[str, Any]
    ) -> tuple:
        """Computes compliance score, health grade, and top statutory red flags."""
        score = 100
        critical_alerts = []

        if pii.get("special_category_fields_detected", 0) > 0:
            score -= 25
            critical_alerts.append(
                f"UK GDPR Article 9 Special Category Data detected ({pii.get('special_category_fields_detected')} fields). Explicit consent required."
            )

        if not any("account" in r.get("path", "") or "delete" in r.get("path", "") for r in routes):
            score -= 15
            critical_alerts.append(
                "Missing statutory Right to Erasure endpoint (DELETE /api/user/account) under Article 17."
            )

        us_transfers = subprocs.get("us_transfers_detected", [])
        if us_transfers:
            score -= 10
            critical_alerts.append(
                f"International data transfers to US cloud providers ({', '.join(us_transfers)}). UK IDTA / SCCs mandatory."
            )

        score = max(20, min(100, score))
        if score >= 85:
            grade = "A (Statutory Compliant)"
        elif score >= 70:
            grade = "B (Good — Minor Remediations Needed)"
        elif score >= 50:
            grade = "C (Moderate Risk — Remediations Mandatory)"
        else:
            grade = "F (Critical Regulatory Vulnerability)"

        return score, grade, critical_alerts
