"""
Tara PrivacyOS — Code-to-GDPR Engine
Module: CODE-106 India DPDP Act 2023 Statutory Mandates Generator
Synthesizes codebase architecture into actionable statutory obligations
under India's Digital Personal Data Protection Act 2023.
"""

from typing import Dict, List, Any

class IndiaDPDPAMandatesGenerator:
    def __init__(self):
        pass

    def generate_mandates(self, pii_summary: Dict[str, Any], route_summary: Dict[str, Any], subproc_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Produces India DPDP Act 2023 statutory compliance requirements and developer guidance."""
        mandates = []

        # Section 6 Notice & Consent
        mandates.append({
            "section": "DPDP Act 2023 Section 6(1) & 6(2)",
            "title": "Itemised Bilingual Notice & Unconditional Consent",
            "statutory_requirement": (
                "Before or at the time of collecting personal data, Tara (Data Fiduciary) must present an itemised notice "
                "specifying the personal data to be collected, purpose of processing, how to exercise rights, and grievance officer contacts. "
                "Notice must be accessible in clear language with option for English and 22 Indian scheduled languages."
            ),
            "status": "MANDATORY_STATUTORY_NOTICE",
            "statutory_penalty": "Penalties up to ₹50 Crore for failure to issue compliant statutory notice."
        })

        # Section 8 Reasonable Security Safeguards
        mandates.append({
            "section": "DPDP Act 2023 Section 8(5) & 8(6)",
            "title": "Reasonable Security Safeguards & Immediate Breach Reporting",
            "statutory_requirement": (
                "The Data Fiduciary must implement reasonable security safeguards (encryption, role-based access, access logging) "
                "to prevent personal data breaches. In case of ANY breach, immediate notification to the Data Protection Board of India (DPBI) "
                "and affected individuals is mandatory."
            ),
            "status": "CRITICAL_DEFENSE_OBLIGATION",
            "statutory_penalty": "Maximum statutory fine of ₹250 CRORE (~£25 Million) for failure to implement reasonable security safeguards!"
        })

        # Section 8(7) Erasure upon Purpose Fulfillment
        mandates.append({
            "section": "DPDP Act 2023 Section 8(7)",
            "title": "Mandatory Erasure upon Purpose Fulfillment or Consent Withdrawal",
            "statutory_requirement": (
                "Personal data must be erased as soon as the user withdraws consent or as soon as the purpose for which it was collected "
                "is no longer being served. The codebase must not retain consultation transcripts indefinitely."
            ),
            "status": "AUTOMATED_RETENTION_MANDATE",
            "statutory_penalty": "Penalties up to ₹100 Crore for non-compliance with data erasure duties."
        })

        # Section 9 Children's Data Guardrails
        mandates.append({
            "section": "DPDP Act 2023 Section 9",
            "title": "Children's Data Verification & Prohibition of Behavioural Tracking",
            "statutory_requirement": (
                "If the platform serves individuals under 18 years, Tara must obtain verifiable parental consent. "
                "Strict statutory prohibition against behavioural monitoring, tracking, or targeted advertising directed at children."
            ),
            "status": "AGE_GATING_CHECK",
            "statutory_penalty": "Penalties up to ₹200 Crore for breach of obligations in relation to children."
        })

        # Section 10 Significant Data Fiduciary (SDF) Assessment
        is_large_scale = pii_summary.get("total_models_analyzed", 0) > 5 or pii_summary.get("special_category_fields_detected", 0) > 0
        mandates.append({
            "section": "DPDP Act 2023 Section 10",
            "title": "Significant Data Fiduciary (SDF) Readiness Check",
            "statutory_requirement": (
                "Given the sensitive nature of consultation & astrological profiling data, the Central Government may notify Tara "
                "as a Significant Data Fiduciary (SDF). SDF obligations require: (1) Appointing a resident India Data Protection Officer (DPO), "
                "(2) Appointing an Independent Data Auditor, and (3) Conducting periodic DPIAs."
            ),
            "status": "ASSESSMENT_RECOMMENDED" if is_large_scale else "MONITOR",
            "statutory_penalty": "Penalties up to ₹150 Crore for SDF non-compliance."
        })

        # Section 16 Cross-Border Data Transfers
        mandates.append({
            "section": "DPDP Act 2023 Section 16 & RBI Guidelines",
            "title": "Cross-Border Data Transfer & Payment Localisation",
            "statutory_requirement": (
                "Personal data can be transferred outside India unless sent to blacklisted jurisdictions notified by the Indian Government. "
                "Payment transaction data processed via Razorpay or UPI must adhere to RBI mandate ensuring full end-to-end transaction data "
                "remains stored exclusively in servers located in India."
            ),
            "status": "INFRASTRUCTURE_CONFIGURATION_MANDATE",
            "statutory_penalty": "Penalties up to ₹100 Crore."
        })

        # Developer Action Points under DPDPA
        dev_action_points = [
            {
                "task_id": "DEV-IN-01",
                "priority": "CRITICAL",
                "area": "Grievance Redressal Mechanism",
                "action": "Expose an in-app Grievance Redressal Officer contact and ticket submission workflow (Section 13)."
            },
            {
                "task_id": "DEV-IN-02",
                "priority": "HIGH",
                "area": "Consent Withdrawal Hook",
                "action": "Ensure withdrawing consent (e.g. user toggles off data use in settings) triggers background job to cease processing."
            },
            {
                "task_id": "DEV-IN-03",
                "priority": "HIGH",
                "area": "Data Localisation for Indian Financials",
                "action": "Verify Indian banking/UPI payment logs are maintained within AWS India (ap-south-1) or Razorpay native storage."
            }
        ]

        return {
            "regulator": "Data Protection Board of India (DPBI)",
            "act": "Digital Personal Data Protection Act, 2023 (DPDPA 2023)",
            "jurisdiction": "Republic of India",
            "max_statutory_penalty": "₹250 Crore (~£25 Million) per violation",
            "mandates": mandates,
            "developer_action_points": dev_action_points
        }
