"""
Tara PrivacyOS — Code-to-GDPR Engine
Module: CODE-102 PII & Special Category Schema Identifier
Classifies database models & ORM fields under UK GDPR (Article 6 / Article 9)
and India DPDP Act 2023 statutory obligations.
"""

import re
from typing import Dict, List, Any, Optional

class PIISchemaDetector:
    # High-Risk / Special Category (UK GDPR Article 9 & Sensitive DPDP Data)
    SPECIAL_CATEGORY_PATTERNS = {
        "HEALTH_MEDICAL": {
            "patterns": [r"health", r"medical", r"disease", r"diagnosis", r"symptom", r"prescription", r"doctor", r"treatment", r"nhs", r"blood", r"disability"],
            "category": "Health & Medical Data (UK GDPR Art 9(1))",
            "statutory_basis": "UK GDPR Article 9(2)(a) Explicit Consent / DPA 2018 Sch 1",
            "dpdp_section": "DPDPA 2023 Sec 4 & Sec 8 (Enhanced Data Protection)",
            "severity": "CRITICAL",
            "requires_explicit_consent": True,
            "recommended_encryption": "Field-Level AES-256 + KMS Envelope",
            "default_retention": "30-90 Days after consultation, then cryptographic erasure"
        },
        "RELIGIOUS_PHILOSOPHICAL": {
            "patterns": [r"religion", r"belief", r"caste", r"kundli", r"horoscope", r"astrology", r"spiritual", r"faith", r"tarot", r"ritual", r"puja"],
            "category": "Religious / Philosophical Beliefs (UK GDPR Art 9(1))",
            "statutory_basis": "UK GDPR Article 9(2)(a) Explicit Consent",
            "dpdp_section": "DPDPA 2023 Sec 4 (Personal Data Processing)",
            "severity": "CRITICAL",
            "requires_explicit_consent": True,
            "recommended_encryption": "Encrypted at rest + Practitioner Masking",
            "default_retention": "Purge raw questions 30 days post-session"
        },
        "SEXUAL_RELATIONSHIP": {
            "patterns": [r"sex_life", r"sexual_orientation", r"marital_dispute", r"affair", r"divorce_case", r"relationship_problem"],
            "category": "Sex Life / Sexual Orientation (UK GDPR Art 9(1))",
            "statutory_basis": "UK GDPR Article 9(2)(a) Explicit Consent",
            "dpdp_section": "DPDPA 2023 Sec 4 (Sensitive Personal Data)",
            "severity": "CRITICAL",
            "requires_explicit_consent": True,
            "recommended_encryption": "Field-Level AES-256",
            "default_retention": "Immediate pseudonymisation upon resolution"
        },
        "BIOMETRIC_GENETIC": {
            "patterns": [r"biometric", r"fingerprint", r"face_id", r"voice_rec", r"genetic", r"dna", r"palm_scan"],
            "category": "Biometric / Genetic Data (UK GDPR Art 9(1))",
            "statutory_basis": "UK GDPR Article 9(2)(a) Explicit Consent",
            "dpdp_section": "DPDPA 2023 Sec 3 & Sec 8",
            "severity": "CRITICAL",
            "requires_explicit_consent": True,
            "recommended_encryption": "Hardware Secure Enclave / Salted Hash",
            "default_retention": "Never retain raw biometrics"
        },
        "STATUTORY_GOV_IDENTIFIERS": {
            "patterns": [r"aadhaar", r"pan_number", r"pan_card", r"passport", r"voter_id", r"ni_number", r"national_insurance", r"ssn", r"driving_licence"],
            "category": "Government National Identifiers (UK/India Statutory IDs)",
            "statutory_basis": "UK GDPR Article 6(1)(c) Legal Obligation / DPDPA 2023 Sec 6",
            "dpdp_section": "Aadhaar Act 2016 & DPDPA Sec 8 (Strict Redaction/Masking)",
            "severity": "HIGH",
            "requires_explicit_consent": False,
            "recommended_encryption": "Masked (display only last 4 digits) + AES-256",
            "default_retention": "Statutory audit requirement (typically 6-7 years)"
        },
        "FINANCIAL_PAYMENT": {
            "patterns": [r"card_num", r"cvv", r"expiry", r"bank_acc", r"iban", r"stripe_customer", r"upi_id", r"salary", r"income"],
            "category": "Financial & Payment Credentials",
            "statutory_basis": "UK GDPR Art 6(1)(b) Contract Performance & PCI-DSS",
            "dpdp_section": "DPDPA 2023 Sec 4 & RBI Tokenisation Guidelines",
            "severity": "HIGH",
            "requires_explicit_consent": False,
            "recommended_encryption": "Tokenized via Stripe/Razorpay (Do NOT store raw CVV)",
            "default_retention": "Financial accounting 6 years"
        }
    }

    # Standard Personal Data (UK GDPR Article 6 & India DPDP Act)
    STANDARD_PII_PATTERNS = {
        "DIRECT_IDENTIFIERS": {
            "patterns": [r"first_name", r"last_name", r"full_name", r"^name$", r"username", r"display_name", r"email", r"phone", r"mobile", r"contact_no"],
            "category": "Direct Personal Identifiers (UK GDPR Art 6(1))",
            "statutory_basis": "UK GDPR Article 6(1)(b) Contract / 6(1)(a) Consent",
            "dpdp_section": "DPDPA 2023 Sec 4 & Sec 6 (Notice & Lawful Consent)",
            "severity": "HIGH",
            "requires_explicit_consent": False,
            "recommended_encryption": "TLS 1.3 in transit, AES-256 at rest",
            "default_retention": "Account lifetime + 30 days grace period"
        },
        "LOCATION_TELEMETRY": {
            "patterns": [r"ip_address", r"client_ip", r"gps", r"latitude", r"longitude", r"geo_loc", r"postal_code", r"zipcode", r"device_id", r"user_agent"],
            "category": "Online Identifiers & Telemetry (PECR / UK GDPR)",
            "statutory_basis": "PECR Reg 6 / UK GDPR Art 6(1)(f) Legitimate Interests",
            "dpdp_section": "DPDPA 2023 Sec 6",
            "severity": "MEDIUM",
            "requires_explicit_consent": False,
            "recommended_encryption": "Pseudonymised / Hashed IP strings",
            "default_retention": "Rolling 14-30 day access log rotation"
        },
        "BIRTH_DEMOGRAPHICS": {
            "patterns": [r"\bdob\b", r"date_of_birth", r"birth_date", r"birth_time", r"birth_place", r"\bgender\b", r"\bage\b"],
            "category": "Demographic & Age Information (UK GDPR Art 6(1))",
            "statutory_basis": "UK GDPR Article 6(1)(b) Contract Performance",
            "dpdp_section": "DPDPA 2023 Sec 6 & Sec 9 (Children's data guardrails if age < 18)",
            "severity": "MEDIUM",
            "requires_explicit_consent": False,
            "recommended_encryption": "Role-Based Access Control + Encryption At Rest",
            "default_retention": "Account lifetime or user deletion request"
        },
        "USER_COMMUNICATIONS": {
            "patterns": [r"\bmessage\b", r"\bquery\b", r"\bprompt\b", r"\bcontent\b", r"\bfeedback\b", r"\bchat_history\b", r"\bconversation\b"],
            "category": "User Communications & Query Prompts (UK GDPR Art 6(1))",
            "statutory_basis": "UK GDPR Article 6(1)(b) Contract Performance",
            "dpdp_section": "DPDPA 2023 Sec 4 & Sec 6 (Notice & Lawful Consent)",
            "severity": "LOW",
            "requires_explicit_consent": False,
            "recommended_encryption": "TLS 1.3 in transit, AES-256 at rest",
            "default_retention": "Account lifetime or user deletion request"
        }
    }

    def __init__(self):
        pass

    def inspect_models(self, parsed_models: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyzes all models and their fields to identify PII, Article 9 risks, and compliance duties."""
        findings = []
        special_category_count = 0
        standard_pii_count = 0
        high_risk_models = set()

        for model in parsed_models:
            model_name = model.get("model_name", "UnknownModel")
            source_file = model.get("source_file", "")
            fields = model.get("fields", [])

            detected_in_model = []

            for f in fields:
                field_name = f.get("field_name", "").lower()
                matched_classification = self._classify_field(field_name)

                if matched_classification:
                    if matched_classification["severity"] == "CRITICAL":
                        special_category_count += 1
                        high_risk_models.add(model_name)
                    else:
                        standard_pii_count += 1

                    detected_in_model.append({
                        "field_name": f.get("field_name"),
                        "line_number": f.get("line_number"),
                        **matched_classification
                    })

            if detected_in_model:
                findings.append({
                    "model_name": model_name,
                    "source_file": source_file,
                    "total_pii_fields": len(detected_in_model),
                    "contains_art9_special_category": any(f["severity"] == "CRITICAL" for f in detected_in_model),
                    "fields": detected_in_model
                })

        # Summary Metrics
        return {
            "total_models_analyzed": len(parsed_models),
            "models_with_pii": len(findings),
            "special_category_fields_detected": special_category_count,
            "standard_pii_fields_detected": standard_pii_count,
            "high_risk_art9_models": list(high_risk_models),
            "compliance_alert": (
                "CRITICAL: Special Category Data (UK GDPR Article 9) detected. "
                "Explicit consent and Data Protection Impact Assessment (DPIA) are legally mandated before launch!"
                if special_category_count > 0 else
                "Standard personal data detected. Regular UK GDPR Article 6 & DPDPA Section 6 requirements apply."
            ),
            "detailed_findings": findings
        }

    def _classify_field(self, field_name: str) -> Optional[Dict[str, Any]]:
        # Check Special Category first
        for key, config in self.SPECIAL_CATEGORY_PATTERNS.items():
            for pat in config["patterns"]:
                if re.search(pat, field_name, re.IGNORECASE):
                    return {
                        "classification_key": key,
                        "category": config["category"],
                        "statutory_basis": config["statutory_basis"],
                        "dpdp_section": config["dpdp_section"],
                        "severity": config["severity"],
                        "requires_explicit_consent": config["requires_explicit_consent"],
                        "recommended_encryption": config["recommended_encryption"],
                        "default_retention": config["default_retention"],
                        "is_art9": True
                    }

        # Check Standard PII
        for key, config in self.STANDARD_PII_PATTERNS.items():
            for pat in config["patterns"]:
                if re.search(pat, field_name, re.IGNORECASE):
                    return {
                        "classification_key": key,
                        "category": config["category"],
                        "statutory_basis": config["statutory_basis"],
                        "dpdp_section": config["dpdp_section"],
                        "severity": config["severity"],
                        "requires_explicit_consent": config["requires_explicit_consent"],
                        "recommended_encryption": config["recommended_encryption"],
                        "default_retention": config["default_retention"],
                        "is_art9": False
                    }

        return None
