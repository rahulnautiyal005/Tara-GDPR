"""
Tara PrivacyOS — Code-to-GDPR Engine
Module: CODE-105 UK GDPR Statutory Mandates Generator
Synthesizes AST scan, PII findings, route flows, and subprocessors into
legally binding UK GDPR compliance mandates, Article 30 RoPA, and developer action checklists.
"""

from typing import Dict, List, Any

class UKGDPRMandatesGenerator:
    def __init__(self):
        pass

    def generate_mandates(self, pii_summary: Dict[str, Any], route_summary: Dict[str, Any], subproc_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Produces full UK GDPR statutory compliance package tailored to scanned code."""
        has_art9 = pii_summary.get("special_category_fields_detected", 0) > 0
        art9_models = pii_summary.get("high_risk_art9_models", [])

        # 1. Statutory Mandates
        mandates = []

        # Lawful Basis
        mandates.append({
            "article": "UK GDPR Article 6(1)(b) & 6(1)(a)",
            "title": "Lawful Basis for Standard Processing",
            "statutory_requirement": (
                "Personal data (Name, Email, Phone, Billing) must be processed under Article 6(1)(b) (Performance of Contract) "
                "for delivering services, or Article 6(1)(a) (Consent) for optional marketing and cookies."
            ),
            "status": "APPLICABLE",
            "risk_if_unaddressed": "Unlawful processing under ICO regulations. Statutory fine up to £17.5M or 4% of annual turnover."
        })

        # Special Category Article 9
        if has_art9:
            mandates.append({
                "article": "UK GDPR Article 9(1) & Article 9(2)(a)",
                "title": "Explicit Consent for Special Category Consultation Data",
                "statutory_requirement": (
                    f"Codebase stores sensitive data (health/religious/spiritual/astrological context) in models: {', '.join(art9_models)}. "
                    "Processing is strictly prohibited under Article 9(1) unless an Article 9(2) exception applies. "
                    "Action Required: Implement separate, unbundled EXPLICIT CONSENT checkbox at booking: "
                    "'I explicitly consent to the processing of my personal health/spiritual consultation data in accordance with the Privacy Notice.'"
                ),
                "status": "CRITICAL_VIOLATION_IF_MISSING",
                "risk_if_unaddressed": "Severe enforcement priority for UK ICO. Fines up to £17.5M and mandatory processing suspension orders."
            })

        # Article 28 Processor Contracts
        subprocs = subproc_summary.get("subprocessor_register", [])
        if subprocs:
            vendor_names = [s["name"] for s in subprocs]
            mandates.append({
                "article": "UK GDPR Article 28(3)",
                "title": "Mandatory Data Processing Agreements (DPAs)",
                "statutory_requirement": (
                    f"Third-party subprocessors detected in code ({', '.join(vendor_names)}). "
                    "Under Article 28, Tara must maintain written, legally binding DPAs binding each processor to process "
                    "data only on documented instructions, ensure confidentiality, and delete data on termination."
                ),
                "status": "MANDATORY_CONTRACTUAL_AUDIT",
                "risk_if_unaddressed": "Direct violation of Article 28. Fines up to £8.7M."
            })

        # Chapter V International Transfers (UK to India & US)
        mandates.append({
            "article": "UK GDPR Chapter V (Articles 44–46)",
            "title": "UK International Data Transfer Agreement (IDTA) / SCCs",
            "statutory_requirement": (
                "UK customer consultation and profile data accessed by development, support, or practitioner teams in India, "
                "or US cloud subprocessors (OpenAI, AWS, Twilio), constitutes a restricted international transfer. "
                "Statutory Mandate: Execute the UK ICO International Data Transfer Agreement (IDTA) or the UK Addendum to EU SCCs "
                "along with a Transfer Risk Assessment (TRA)."
            ),
            "status": "CRITICAL_GOVERNANCE_REQUIREMENT",
            "risk_if_unaddressed": "Unlawful international data export. Immediate ICO regulatory stop order on overseas data access."
        })

        # Article 32 Security & Access Controls
        mandates.append({
            "article": "UK GDPR Article 32 & Article 5(1)(c)",
            "title": "Practitioner Data Minimisation & At-Rest Encryption",
            "statutory_requirement": (
                "Ensure database fields storing special category and consultation transcripts use AES-256 encryption. "
                "Furthermore, practitioners must NEVER have access to customer personal contact phone numbers or raw email addresses. "
                "Implement in-app calling / masked messaging to prevent practitioner client poaching and off-platform data leakage."
            ),
            "status": "TECHNICAL_CONTROL_MANDATE",
            "risk_if_unaddressed": "Major data breach vulnerability; unauthorized external data leak requiring 72-hour ICO notification."
        })

        # 2. Automated Article 30 RoPA Table
        ropa_entries = self._build_ropa_table(pii_summary, subproc_summary)

        # 3. Developer Remediation Checklist
        dev_checklist = self._build_dev_checklist(pii_summary, route_summary, subproc_summary)

        return {
            "regulator": "Information Commissioner's Office (ICO) — United Kingdom",
            "regulations": "UK General Data Protection Regulation (UK GDPR) & Data Protection Act 2018",
            "dpia_required": has_art9,
            "dpia_justification": (
                "A formal Data Protection Impact Assessment (DPIA) is statutory mandatory because the application involves "
                "large-scale processing of special category data (Article 9) and automated AI/LLM consultation workflows."
                if has_art9 else "DPIA recommended as best practice."
            ),
            "mandates": mandates,
            "article_30_ropa": ropa_entries,
            "developer_remediation_checklist": dev_checklist
        }

    def _build_ropa_table(self, pii_summary: Dict[str, Any], subproc_summary: Dict[str, Any]) -> List[Dict[str, Any]]:
        ropa = [
            {
                "activity_id": "ROPA-01",
                "processing_purpose": "User Account Registration & Identity Authentication",
                "data_subjects": "Platform Customers & Consultation Seekers",
                "data_categories": "Full Name, Email Address, Password Hash, IP Address",
                "lawful_basis": "UK GDPR Article 6(1)(b) (Performance of Contract)",
                "recipients_processors": "AWS (Hosting), Twilio (SMS Auth)",
                "transfer_safeguards": "UK IDTA / UK Addendum to EU SCCs",
                "retention_period": "Duration of user account + 30 days after deletion request",
                "security_measures": "TLS 1.3 in transit, Bcrypt/Argon2 password hashing, RBAC"
            },
            {
                "activity_id": "ROPA-02",
                "processing_purpose": "Consultation Booking, Horoscope/Kundli & Spiritual Sessions",
                "data_subjects": "Consultation Clients",
                "data_categories": "Date of Birth, Birth Time, Birth Location, Consultation Queries, Relationship/Health Context",
                "lawful_basis": "UK GDPR Art 6(1)(b) (Contract) + Art 9(2)(a) (Explicit Consent)",
                "recipients_processors": "Assigned Vetted Practitioner (India/UK), AWS RDS",
                "transfer_safeguards": "UK IDTA Agreement between Tara UK and Tara India / Practitioners",
                "retention_period": "Consultation query purged after 60 days; birth demographics kept until account closed",
                "security_measures": "Field-level AES-256 encryption, Practitioner phone/email masking"
            },
            {
                "activity_id": "ROPA-03",
                "processing_purpose": "AI/LLM Consultation Insights & Summarization",
                "data_subjects": "Consultation Clients",
                "data_categories": "De-identified Consultation Transcripts & Question Prompts",
                "lawful_basis": "UK GDPR Article 6(1)(b) + Explicit Consent Art 9(2)(a)",
                "recipients_processors": "OpenAI LLC (API Processor)",
                "transfer_safeguards": "Standard Contractual Clauses + Zero-Data Retention Commercial Agreement",
                "retention_period": "Zero retention on processor side; local ephemeral cache for session duration",
                "security_measures": "PII scrubbing before API egress, TLS 1.3"
            },
            {
                "activity_id": "ROPA-04",
                "processing_purpose": "Payment Processing & Financial Invoicing",
                "data_subjects": "Paying Customers & Practitioners",
                "data_categories": "Billing Address, Payment Token, Transaction Amount, Payout Account",
                "lawful_basis": "UK GDPR Article 6(1)(b) & Article 6(1)(c) (Statutory Tax Accounting)",
                "recipients_processors": "Stripe Payments UK Ltd. / Razorpay",
                "transfer_safeguards": "Stripe Global DPA",
                "retention_period": "Statutory 6 years for UK HMRC and financial compliance",
                "security_measures": "PCI-DSS Level 1 tokenisation (No card CVVs on Tara servers)"
            }
        ]
        return ropa

    def _build_dev_checklist(self, pii_summary: Dict[str, Any], route_summary: Dict[str, Any], subproc_summary: Dict[str, Any]) -> List[Dict[str, Any]]:
        checklist = [
            {
                "task_id": "DEV-UK-01",
                "priority": "CRITICAL",
                "component": "Frontend Registration & Booking UI",
                "requirement": "Add unbundled explicit consent checkbox for Article 9 consultation data before booking.",
                "code_action": "Ensure consent checkbox is unticked by default and logs consent_timestamp, policy_version, user_id."
            },
            {
                "task_id": "DEV-UK-02",
                "priority": "CRITICAL",
                "component": "Practitioner Portal / API Layer",
                "requirement": "Implement data masking on practitioner API views to prevent customer contact theft.",
                "code_action": "Strip customer phone number and email from practitioner response payloads. Route communications via in-app relay."
            },
            {
                "task_id": "DEV-UK-03",
                "priority": "CRITICAL",
                "component": "User Account API",
                "requirement": "Implement DELETE /api/user/account statutory right to erasure (Article 17).",
                "code_action": "Create soft-delete workflow that scrubs PII across database tables and informs subprocessors within 30 days."
            },
            {
                "task_id": "DEV-UK-04",
                "priority": "HIGH",
                "component": "AI / OpenAI API Integration",
                "requirement": "Configure OpenAI zero-data retention headers and sanitize prompt payloads.",
                "code_action": "Scrub direct names, phone numbers, and addresses from prompt text before dispatching to external LLMs."
            },
            {
                "task_id": "DEV-UK-05",
                "priority": "HIGH",
                "component": "Database / ORM Models",
                "requirement": "Implement field-level encryption for sensitive consultation notes.",
                "code_action": "Use SQLAlchemy TypeDecorator or database pgcrypto / KMS envelope for sensitive columns."
            }
        ]
        return checklist
