"""
Tara PrivacyOS — Code-to-GDPR Engine
Module: CODE-104 Third-Party SDK & Subprocessor Detector
Detects third-party APIs, SDKs, and cloud dependencies, mapping them to
statutory Article 28 DPA obligations and international transfer mechanisms.
"""

from typing import Dict, List, Any

class SubprocessorDetector:
    # Known third-party subprocessors database
    SUBPROCESSOR_DATABASE = {
        "openai": {
            "name": "OpenAI LLC",
            "category": "AI / Large Language Model API",
            "jurisdiction": "United States (Third Country)",
            "data_types_processed": ["User Consultation Prompts", "Question Transcripts", "Context Summaries"],
            "transfer_mechanism_required": "UK IDTA / EU SCCs + Enterprise Zero-Data Retention Agreement",
            "article_28_dpa_status": "Mandatory DPA (Ensure API opt-out of model training is active)",
            "risk_level": "CRITICAL",
            "recommendation": "Verify OpenAI API Data Processing Addendum is executed. Ensure organization account disables training on API inputs."
        },
        "anthropic": {
            "name": "Anthropic PBC",
            "category": "AI / LLM API",
            "jurisdiction": "United States (Third Country)",
            "data_types_processed": ["Consultation Queries", "Conversation Context"],
            "transfer_mechanism_required": "UK IDTA / Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory DPA Required",
            "risk_level": "CRITICAL",
            "recommendation": "Execute Anthropic Commercial DPA. Confirm data retention schedule."
        },
        "google": {
            "name": "Google LLC / Google Cloud Platform",
            "category": "Cloud Hosting & AI APIs",
            "jurisdiction": "United States / EU / Global",
            "data_types_processed": ["Application Hosting", "Database Backups", "AI Inference"],
            "transfer_mechanism_required": "Google Cloud Data Processing Addendum (CDPA) + UK Addendum",
            "article_28_dpa_status": "Mandatory Cloud DPA",
            "risk_level": "HIGH",
            "recommendation": "Ensure GCP region is pinned to Europe (e.g. europe-west2 London) to minimize international transfer liabilities."
        },
        "boto3": {
            "name": "Amazon Web Services (AWS)",
            "category": "Cloud Infrastructure & Database",
            "jurisdiction": "United States / Ireland / UK",
            "data_types_processed": ["Primary Database", "User Files", "App Compute"],
            "transfer_mechanism_required": "AWS GDPR Data Processing Addendum",
            "article_28_dpa_status": "Mandatory Cloud DPA",
            "risk_level": "HIGH",
            "recommendation": "Pin primary S3 and RDS storage to AWS London (eu-west-2) to ensure UK local residency."
        },
        "stripe": {
            "name": "Stripe Payments UK, Ltd.",
            "category": "Payment Processing (PCI-DSS)",
            "jurisdiction": "United Kingdom / United States",
            "data_types_processed": ["Payment Card Tokens", "Customer Billing Address", "Transaction History"],
            "transfer_mechanism_required": "Stripe Data Processing Agreement",
            "article_28_dpa_status": "Independent Controller / Joint Controller in card data handling",
            "risk_level": "HIGH",
            "recommendation": "Use Stripe Elements to prevent raw payment card numbers from touching Tara backend servers."
        },
        "razorpay": {
            "name": "Razorpay Software Pvt. Ltd.",
            "category": "Payment Processing (India UPI & Cards)",
            "jurisdiction": "India",
            "data_types_processed": ["UPI ID", "Indian Bank Credentials", "Billing Details"],
            "transfer_mechanism_required": "DPDPA 2023 Compliant Merchant Agreement & RBI Tokenisation",
            "article_28_dpa_status": "Payment Processor Agreement",
            "risk_level": "HIGH",
            "recommendation": "Execute Merchant Service Agreement complying with RBI storage guidelines and DPDP Act 2023."
        },
        "firebase": {
            "name": "Google Firebase",
            "category": "Authentication & Mobile Telemetry",
            "jurisdiction": "United States",
            "data_types_processed": ["Device IDs", "Push Tokens", "Authentication Metadata"],
            "transfer_mechanism_required": "Google Cloud DPA + UK International Transfer Safeguards",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "HIGH",
            "recommendation": "Audit Firebase Analytics tracking to ensure non-essential SDK telemetry requires PECR opt-in consent."
        },
        "posthog": {
            "name": "PostHog Inc.",
            "category": "Product Analytics & Session Recording",
            "jurisdiction": "EU Cloud / US Cloud",
            "data_types_processed": ["User Clickstreams", "Session Replays", "IP Addresses"],
            "transfer_mechanism_required": "PostHog DPA + PECR Cookie Banner Consent",
            "article_28_dpa_status": "Mandatory Processor DPA",
            "risk_level": "HIGH",
            "recommendation": "Configure PostHog EU cloud instance; enable strict input masking on session recording to mask client consultation queries."
        },
        "twilio": {
            "name": "Twilio Inc.",
            "category": "SMS & Video Communication Gateway",
            "jurisdiction": "United States",
            "data_types_processed": ["Customer Phone Numbers", "SMS Logs", "Call Audio"],
            "transfer_mechanism_required": "Twilio Binding Corporate Rules (BCR) / DPA",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "HIGH",
            "recommendation": "Sign Twilio Data Protection Addendum utilizing Twilio's approved BCRs for UK transfers."
        },
        "sendgrid": {
            "name": "Twilio SendGrid",
            "category": "Transactional Email",
            "jurisdiction": "United States",
            "data_types_processed": ["Customer Email Addresses", "Email Delivery Logs"],
            "transfer_mechanism_required": "Twilio BCR / DPA",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Ensure marketing unsubscription headers and transactional-only filters are enforced."
        },
        "cloudinary": {
            "name": "Cloudinary Ltd.",
            "category": "Media Storage & Image CDN",
            "jurisdiction": "United States / Israel (Adequacy Decision)",
            "data_types_processed": ["Property Photos", "Listing Media", "User Uploads"],
            "transfer_mechanism_required": "UK Addendum / EU Standard Contractual Clauses (SCCs)",
            "article_28_dpa_status": "Mandatory Media DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Execute Cloudinary Data Processing Addendum and enforce secure signed upload URLs."
        },
        "mapbox": {
            "name": "Mapbox Inc.",
            "category": "Interactive Maps & Geolocation Telemetry",
            "jurisdiction": "United States",
            "data_types_processed": ["User IP Addresses", "Geocoordinates", "Map Telemetry"],
            "transfer_mechanism_required": "UK-US Data Bridge / EU Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Geolocation DPA",
            "risk_level": "HIGH",
            "recommendation": "Execute Mapbox Data Processing Addendum and configure privacy-preserving coordinate fuzzing."
        },
        "mongo": {
            "name": "MongoDB Inc. (MongoDB Atlas)",
            "category": "Cloud Database Infrastructure",
            "jurisdiction": "United States / Ireland / AWS Cloud",
            "data_types_processed": ["User Profiles", "Listing Records", "Authentication Credentials"],
            "transfer_mechanism_required": "MongoDB Atlas GDPR Data Processing Agreement",
            "article_28_dpa_status": "Mandatory Cloud Database DPA",
            "risk_level": "HIGH",
            "recommendation": "Pin MongoDB Atlas cluster to AWS London (eu-west-2) or Mumbai (ap-south-1) for statutory data residency."
        },
        "render": {
            "name": "Render Services Inc.",
            "category": "Cloud Compute & Web Hosting",
            "jurisdiction": "United States / Germany (Frankfurt)",
            "data_types_processed": ["Application Compute Logs", "HTTP Headers", "IP Telemetry"],
            "transfer_mechanism_required": "Render DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Hosting DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Execute Render Data Processing Agreement and configure encrypted environment secrets."
        }
    }

    def __init__(self):
        pass

    def detect_subprocessors(self, imports_and_sdks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Scans all imported packages and dependencies to build subprocessor register."""
        detected_vendors = {}

        for item in imports_and_sdks:
            pkg_name = item.get("package", "").lower()
            source_file = item.get("source_file", "")

            for db_key, vendor_info in self.SUBPROCESSOR_DATABASE.items():
                if db_key in pkg_name:
                    if db_key not in detected_vendors:
                        detected_vendors[db_key] = {
                            **vendor_info,
                            "detected_packages": [pkg_name],
                            "referencing_files": [source_file]
                        }
                    else:
                        if pkg_name not in detected_vendors[db_key]["detected_packages"]:
                            detected_vendors[db_key]["detected_packages"].append(pkg_name)
                        if source_file not in detected_vendors[db_key]["referencing_files"]:
                            detected_vendors[db_key]["referencing_files"].append(source_file)

        # International Transfer & Risk Summary
        us_transfers = [v["name"] for v in detected_vendors.values() if "United States" in v["jurisdiction"]]
        critical_vendors = [v["name"] for v in detected_vendors.values() if v["risk_level"] == "CRITICAL"]

        return {
            "total_subprocessors_detected": len(detected_vendors),
            "critical_risk_subprocessors": len(critical_vendors),
            "international_transfers_count": len(us_transfers),
            "us_transfers_detected": us_transfers,
            "subprocessor_register": list(detected_vendors.values())
        }
