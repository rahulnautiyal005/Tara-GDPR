"""
Tara PrivacyOS & Legal AI — Family Law & Matrimonial Finance Engine
Phase 2 MVP: Form E Financial Discovery, 12-Month Bank Forensic Audit,
and Section 25 Matrimonial Causes Act 1973 Settlement Modeling.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

FAMILY_LAW_PRESETS: Dict[str, Any] = {
    "harrison-matrimonial": {
        "id": "harrison-matrimonial",
        "case_name": "Harrison v. Harrison",
        "court_ref": "FD26F00892",
        "jurisdiction": "England & Wales (Family Division / Central Family Court, London)",
        "hearing_type": "First Directions Appointment (FDA) / Financial Dispute Resolution (FDR)",
        "applicant": {
            "name": "Eleanor Harrison",
            "role": "Applicant (Wife)",
            "age": 44,
            "occupation": "Former Interior Architect (Primary Carer)",
            "gross_income": 18000,
            "net_monthly": 1500,
            "earning_capacity": "Part-time capacity restricted by childcare obligations",
            "housing_need": 1400000
        },
        "respondent": {
            "name": "Marcus Harrison",
            "role": "Respondent (Husband)",
            "age": 47,
            "occupation": "Managing Director, Mayfair Private Capital Partners",
            "gross_income": 340000,
            "net_monthly": 16800,
            "earning_capacity": "High trajectory with discretionary bonus pool",
            "housing_need": 1400000
        },
        "marriage_details": {
            "marriage_date": "2010-06-12",
            "separation_date": "2026-02-18",
            "duration_years": 16,
            "children": [
                {"name": "Oliver Harrison", "age": 14, "schooling": "Independent Day School (£24k/yr)"},
                {"name": "Amelia Harrison", "age": 11, "schooling": "Independent Day School (£21k/yr)"}
            ]
        },
        "assets_schedule": {
            "matrimonial_home": {
                "address": "42 Victoria Road, Kensington, London W8 5RH",
                "ownership": "Joint Tenancy (50/50)",
                "gross_valuation": 2400000,
                "mortgage_outstanding": 620000,
                "mortgage_lender": "Barclays Premier Home Loans",
                "notional_sale_costs_pct": 3.0,
                "net_equity": 1708000
            },
            "bank_accounts": [
                {"holder": "Joint", "institution": "Barclays Premier Current", "balance": 42500, "disclosed": True},
                {"holder": "Respondent", "institution": "Coutts & Co Current", "balance": 185000, "disclosed": True},
                {"holder": "Respondent", "institution": "Julius Baer Offshore GBP (Guernsey)", "balance": 310000, "disclosed": False, "audit_source": "Bank Audit Flagger"},
                {"holder": "Applicant", "institution": "HSBC Advance Current", "balance": 18400, "disclosed": True}
            ],
            "investments_and_business": [
                {"name": "Mayfair Private Capital Partnership Equity (15%)", "declared_value": 450000, "forensic_adjusted_value": 850000, "holder": "Respondent"},
                {"name": "Vanguard FTSE Global All-Cap ISA", "declared_value": 145000, "forensic_adjusted_value": 145000, "holder": "Respondent"},
                {"name": "Kraken Crypto Wallet (BTC & ETH)", "declared_value": 0, "forensic_adjusted_value": 38400, "holder": "Respondent", "disclosed": False}
            ],
            "pensions": [
                {"scheme": "Aviva Executive SIPP Scheme", "cev": 620000, "holder": "Respondent"},
                {"scheme": "Prudential Personal Pension", "cev": 85000, "holder": "Applicant"}
            ],
            "liabilities": [
                {"creditor": "American Express Centurion", "amount": 28000, "holder": "Respondent"},
                {"creditor": "Capital Gains Tax Reserve (2025/26)", "amount": 65000, "holder": "Respondent"}
            ]
        },
        "bank_audit_discrepancies": [
            {
                "id": "FLAG-01",
                "severity": "CRITICAL",
                "type": "Undisclosed Offshore Transfer",
                "date": "2026-01-14",
                "amount": 95000,
                "currency": "GBP",
                "source_account": "Coutts & Co (Acct ending 4912)",
                "beneficiary": "Apex Horizon FZE (Emirates NBD, Dubai, UAE)",
                "finding": "Wire transfer dispatched 5 weeks before petition filing. Form E Section 2.14 fails to declare any UAE corporate or bank holdings.",
                "legal_implication": "Breach of full and frank financial disclosure under Livesey v Jenkins [1985] AC 424. Potential Section 37 MCA 1973 avoidance of disposition.",
                "questionnaire_item": "Provide all bank statements, incorporation certificates, and audited accounts for Apex Horizon FZE from 1 Jan 2025 to date."
            },
            {
                "id": "FLAG-02",
                "severity": "CRITICAL",
                "type": "Unexplained Cash Liquidations",
                "date": "2026-02-01 to 2026-02-03",
                "amount": 45000,
                "currency": "GBP",
                "source_account": "Coutts Mayfair Branch Over-The-Counter",
                "beneficiary": "Self (Cash Withdrawals in 3 x £15k tranches)",
                "finding": "Unprecedented cash withdrawals spanning 72 hours immediately preceding physical separation of the parties.",
                "legal_implication": "Asset dissipation or concealment. Presumption of available liquidity to be added back (add-back doctrine: Norris v Norris [2003] 2 FLR 1124).",
                "questionnaire_item": "State the precise location, retention, or destination of the £45,000 withdrawn in cash between 1-3 Feb 2026, with documentary receipts."
            },
            {
                "id": "FLAG-03",
                "severity": "HIGH",
                "type": "Disguised Third-Party Management Fee",
                "date": "Monthly (2025–2026)",
                "amount": 28500,
                "currency": "GBP",
                "source_account": "Mayfair Capital Account",
                "beneficiary": "Kingswood Advisory Ltd (Director: Brother-in-Law)",
                "finding": "Regular round-sum transfers without contractual deliverables or commercial correspondence.",
                "legal_implication": "Artificial deflation of net disposable drawings to minimise spousal and child maintenance liability under Section 25(2)(a).",
                "questionnaire_item": "Produce copies of all consultancy contracts, invoices, and deliverables supporting payments of £28,500 to Kingswood Advisory Ltd."
            },
            {
                "id": "FLAG-04",
                "severity": "MEDIUM",
                "type": "Undisclosed Cryptocurrency Egress",
                "date": "2025-11-20",
                "amount": 18200,
                "currency": "GBP",
                "source_account": "Barclays Premier to Revolut Pay",
                "beneficiary": "Payward Ltd (Kraken Crypto Exchange)",
                "finding": "Form E Box 2.8 (Investments) states 'None' for digital/virtual currencies despite debit card transaction records.",
                "legal_implication": "Omission of capital assets. Under court rules, digital assets must be disclosed with public wallet addresses.",
                "questionnaire_item": "Confirm all public wallet addresses and provide exchange ledger reports for all cryptocurrency accounts held by the Respondent."
            }
        ]
    },
    "davies-matrimonial": {
        "id": "davies-matrimonial",
        "case_name": "Davies v. Davies",
        "court_ref": "BS26D00412",
        "jurisdiction": "Bristol Family Court",
        "hearing_type": "First Directions Appointment (FDA)",
        "applicant": {
            "name": "Sarah Davies",
            "role": "Applicant (Wife)",
            "age": 52,
            "occupation": "Senior Specialist NHS Nurse",
            "gross_income": 46000,
            "net_monthly": 2850,
            "earning_capacity": "Near ceiling; defined contribution NHS pension",
            "housing_need": 380000
        },
        "respondent": {
            "name": "Robert Davies",
            "role": "Respondent (Husband)",
            "age": 54,
            "occupation": "Principal Civil Engineering Project Director",
            "gross_income": 88000,
            "net_monthly": 4900,
            "earning_capacity": "High stable professional earnings",
            "housing_need": 380000
        },
        "marriage_details": {
            "marriage_date": "2002-09-14",
            "separation_date": "2025-11-05",
            "duration_years": 23,
            "children": []
        },
        "assets_schedule": {
            "matrimonial_home": {
                "address": "18 Clifton Green, Bristol BS8 4JW",
                "ownership": "Joint (50/50)",
                "gross_valuation": 560000,
                "mortgage_outstanding": 115000,
                "mortgage_lender": "Nationwide Building Society",
                "notional_sale_costs_pct": 3.0,
                "net_equity": 428200
            },
            "bank_accounts": [
                {"holder": "Joint", "institution": "Nationwide FlexPlus", "balance": 18200, "disclosed": True},
                {"holder": "Respondent", "institution": "Lloyds Club Account", "balance": 38500, "disclosed": True},
                {"holder": "Applicant", "institution": "Santander 123", "balance": 14200, "disclosed": True}
            ],
            "investments_and_business": [
                {"name": "Nutmeg Stocks & Shares ISA", "declared_value": 52000, "forensic_adjusted_value": 52000, "holder": "Respondent"}
            ],
            "pensions": [
                {"scheme": "Civil Service Alpha Pension Scheme", "cev": 540000, "holder": "Respondent"},
                {"scheme": "NHS 2015 Pension Scheme", "cev": 118000, "holder": "Applicant"}
            ],
            "liabilities": [
                {"creditor": "Barclaycard Platinum", "amount": 8400, "holder": "Respondent"}
            ]
        },
        "bank_audit_discrepancies": [
            {
                "id": "FLAG-D1",
                "severity": "HIGH",
                "type": "Suppressed Annual Performance Bonus",
                "date": "2026-03-28",
                "amount": 22000,
                "currency": "GBP",
                "source_account": "Atkins Infrastructure Payroll",
                "beneficiary": "Lloyds Account (ending 8821)",
                "finding": "Form E Part 2.1 declared standard salary only, omitting the recurring guaranteed £22,000 performance bonus.",
                "legal_implication": "Misstatement of gross income under Section 25(2)(a).",
                "questionnaire_item": "Provide P60 and last 3 March payslips showing bonus remuneration history."
            }
        ]
    }
}

class FamilyLawEngine:
    """Core algorithmic engine for UK Family Court Matrimonial Finance Analysis."""

    def __init__(self):
        self.presets = FAMILY_LAW_PRESETS

    def list_presets(self) -> List[Dict[str, Any]]:
        """Returns summarized presets for UI selection."""
        return [
            {
                "id": v["id"],
                "case_name": v["case_name"],
                "court_ref": v["court_ref"],
                "jurisdiction": v["jurisdiction"],
                "parties": f"{v['applicant']['name']} vs {v['respondent']['name']}",
                "duration": f"{v['marriage_details']['duration_years']} years",
                "total_declared": sum([
                    v["assets_schedule"]["matrimonial_home"]["net_equity"],
                    sum(a["balance"] for a in v["assets_schedule"]["bank_accounts"]),
                    sum(p["cev"] for p in v["assets_schedule"]["pensions"])
                ]),
                "flags_count": len(v.get("bank_audit_discrepancies", []))
            }
            for v in self.presets.values()
        ]

    def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves complete case record."""
        return self.presets.get(case_id, self.presets["harrison-matrimonial"])

    def run_full_audit(self, case_id: str) -> Dict[str, Any]:
        """
        Executes complete Phase 2 Family Law analysis:
        1. Form E balance sheet computation
        2. Forensic bank statement anomaly extraction
        3. Section 25 MCA 1973 multi-scenario settlement modeling
        4. ES1 Composite Asset Schedule & Questionnaire generation
        """
        case = self.get_case(case_id)
        if not case:
            case = self.presets["harrison-matrimonial"]

        assets = case["assets_schedule"]
        home = assets["matrimonial_home"]

        # Calculate Capital Sub-Totals
        net_home_equity = home["net_equity"]
        liquid_cash = sum(a["balance"] for a in assets["bank_accounts"])
        investments_val = sum(i["forensic_adjusted_value"] for i in assets["investments_and_business"])
        pensions_total = sum(p["cev"] for p in assets["pensions"])
        liabilities_total = sum(l["amount"] for l in assets["liabilities"])

        # Undisclosed / Hidden Assets Uncovered by AI
        hidden_assets = [
            a for a in assets["bank_accounts"] if not a.get("disclosed", True)
        ] + [
            i for i in assets["investments_and_business"] if not i.get("disclosed", True)
        ]
        hidden_total = sum(h.get("balance", h.get("forensic_adjusted_value", 0)) for h in hidden_assets)

        # Net Real Capital (excluding pensions)
        net_capital = net_home_equity + liquid_cash + investments_val - liabilities_total
        total_wealth_pool = net_capital + pensions_total

        # Section 25 MCA 1973 Statutory Calculations
        models = self._compute_settlement_models(case, net_capital, pensions_total)

        return {
            "metadata": {
                "case_name": case["case_name"],
                "court_ref": case["court_ref"],
                "jurisdiction": case["jurisdiction"],
                "hearing_type": case["hearing_type"],
                "audit_timestamp": datetime.now().isoformat(),
                "duration_years": case["marriage_details"]["duration_years"],
                "children_count": len(case["marriage_details"]["children"])
            },
            "balance_sheet": {
                "matrimonial_home_equity": net_home_equity,
                "liquid_cash": liquid_cash,
                "investments_and_business": investments_val,
                "liabilities": liabilities_total,
                "net_capital_assets": net_capital,
                "pension_assets_cev": pensions_total,
                "total_matrimonial_wealth": total_wealth_pool,
                "ai_uncovered_hidden_assets": hidden_total
            },
            "bank_discrepancies": case.get("bank_audit_discrepancies", []),
            "section_25_models": models,
            "questionnaires": [d["questionnaire_item"] for d in case.get("bank_audit_discrepancies", [])]
        }

    def _compute_settlement_models(self, case: Dict[str, Any], net_capital: float, pensions_total: float) -> Dict[str, Any]:
        """Calculates standard UK Family Court Section 25 settlement scenarios."""
        # 1. White v White (50/50 Equal Division Starting Point)
        equal_capital_each = net_capital / 2.0
        equal_pension_each = pensions_total / 2.0

        # Pension Sharing Order (PSO) to equalize CEVs
        p_applicant = next((p["cev"] for p in case["assets_schedule"]["pensions"] if p["holder"] == "Applicant"), 0)
        p_respondent = next((p["cev"] for p in case["assets_schedule"]["pensions"] if p["holder"] == "Respondent"), 0)
        pension_transfer_needed = max(0, (p_respondent - p_applicant) / 2.0)
        pso_pct = round((pension_transfer_needed / p_respondent * 100), 1) if p_respondent > 0 else 0

        # 2. Needs-Based Carer Settlement (Radmacher / Charman)
        # Prioritizes applicant retaining the matrimonial home mortgage-free for minor children
        app_housing_need = case["applicant"]["housing_need"]
        needs_applicant_capital = min(net_capital * 0.70, max(app_housing_need, net_capital * 0.60))
        needs_respondent_capital = net_capital - needs_applicant_capital

        return {
            "scenario_a_equality": {
                "title": "Model A: Pure Equal Sharing (White v White)",
                "statutory_basis": "Section 25(2) MCA 1973 Equality Benchmark",
                "applicant_capital": equal_capital_each,
                "respondent_capital": equal_capital_each,
                "applicant_capital_pct": 50.0,
                "respondent_capital_pct": 50.0,
                "pso_percentage": pso_pct,
                "summary": "Equal 50/50 split of all capital and pension assets. Requires sale of matrimonial home or substantial re-mortgage buyout."
            },
            "scenario_b_needs": {
                "title": "Model B: Needs-Based Housing Priority (Charman / Radmacher)",
                "statutory_basis": "Section 25(2)(b) First Consideration to Welfare of Minor Children",
                "applicant_capital": needs_applicant_capital,
                "respondent_capital": needs_respondent_capital,
                "applicant_capital_pct": round((needs_applicant_capital / net_capital * 100), 1),
                "respondent_capital_pct": round((needs_respondent_capital / net_capital * 100), 1),
                "pso_percentage": pso_pct,
                "summary": "Transfers sufficient net capital to the Applicant to preserve mortgage-free family home for children until majority."
            },
            "scenario_c_clean_break": {
                "title": "Model C: Full Clean Break with Pension Offsetting",
                "statutory_basis": "Section 25A MCA 1973 Clean Break Direction",
                "applicant_capital": net_capital * 0.65,
                "respondent_capital": net_capital * 0.35,
                "applicant_capital_pct": 65.0,
                "respondent_capital_pct": 35.0,
                "pso_percentage": 0.0,
                "summary": "Applicant receives higher capital share in exchange for waiving pension sharing order and spousal periodical payments."
            }
        }
