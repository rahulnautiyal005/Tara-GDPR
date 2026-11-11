"""
Tara PrivacyOS — Phase 4 & Phase 5 Test Suite
Tests:
1. AI & LLM Governance Engine (Shadow AI Risk Auditor, DPIA & AUP Generators)
2. Interactive Data-Flow & Cross-Border Engine (Topology, Lawful Bases, IDTA Generator)
3. FastAPI REST Endpoints Integration
"""

import unittest
from fastapi.testclient import TestClient

from tara_privacyos.legal_engines.ai_governance_engine import AIGovernanceEngine
from tara_privacyos.legal_engines.data_flow_engine import DataFlowEngine
from tara_privacyos.api.server import app

class TestPhase4And5Engines(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ai_engine = AIGovernanceEngine()
        cls.df_engine = DataFlowEngine()
        cls.client = TestClient(app)

    # -------------------------------------------------------------
    # FEATURE 1: AI & LLM GOVERNANCE ENGINE TESTS
    # -------------------------------------------------------------
    def test_ai_catalog(self):
        catalog = self.ai_engine.get_catalog()
        self.assertIn("tools", catalog)
        self.assertIn("data_types", catalog)
        self.assertGreaterEqual(len(catalog["tools"]), 6)
        self.assertGreaterEqual(len(catalog["data_types"]), 6)

    def test_ai_audit_high_risk_scenario(self):
        # Scenario: Consumer ChatGPT with sensitive consultation health notes
        audit = self.ai_engine.audit_ai_footprint(
            selected_tool_ids=["chatgpt_consumer"],
            selected_data_ids=["consultation_health"],
            company_name="Tara Infotech Ltd"
        )
        self.assertLessEqual(audit["overall_score"], 60, "Should score high risk for consumer AI with health data")
        self.assertIn("Grade", audit["health_grade"])
        self.assertGreater(len(audit["red_flags"]), 0)
        
        # Verify Article 9 breach flag
        flag_titles = [rf["title"] for rf in audit["red_flags"]]
        self.assertTrue(any("Article 9" in title for title in flag_titles))

    def test_ai_audit_enterprise_clean_scenario(self):
        # Scenario: Azure OpenAI enterprise with general marketing copy
        audit = self.ai_engine.audit_ai_footprint(
            selected_tool_ids=["azure_openai"],
            selected_data_ids=["customer_pii"],
            company_name="Tara Infotech Ltd"
        )
        self.assertGreaterEqual(audit["overall_score"], 80, "Should score high/safe for Azure enterprise tier")

    def test_ai_dpia_and_aup_generation(self):
        audit = self.ai_engine.audit_ai_footprint(
            selected_tool_ids=["chatgpt_consumer", "openai_api"],
            selected_data_ids=["consultation_health", "source_code"],
            company_name="Tara Infotech Ltd"
        )
        dpia = self.ai_engine.generate_ai_dpia(audit)
        self.assertIn("DATA PROTECTION IMPACT ASSESSMENT", dpia)
        self.assertIn("Article 35", dpia)
        self.assertIn("Tara Infotech Ltd", dpia)

        aup = self.ai_engine.generate_employee_aup(audit)
        self.assertIn("ACCEPTABLE USE POLICY", aup.upper())
        self.assertIn("3 GOLDEN RULES", aup.upper())

    # -------------------------------------------------------------
    # FEATURE 2: VISUAL DATA-FLOW & CROSS-BORDER ENGINE TESTS
    # -------------------------------------------------------------
    def test_topology_presets(self):
        presets = self.df_engine.get_presets_list()
        self.assertGreaterEqual(len(presets), 2)
        preset_ids = [p["id"] for p in presets]
        self.assertIn("tara-consultation", preset_ids)
        self.assertIn("medconnect-telehealth", preset_ids)

    def test_tara_consultation_topology(self):
        topo = self.df_engine.get_topology("tara-consultation")
        self.assertIn("nodes", topo)
        self.assertIn("links", topo)
        self.assertEqual(len(topo["nodes"]), 6)
        self.assertEqual(len(topo["links"]), 5)
        
        # Verify cross-border transfers and violations
        self.assertGreater(topo["summary"]["cross_border_transfers"], 0)
        self.assertEqual(topo["summary"]["statutory_violations"], 1, "Should identify 1 missing IDTA violation")

    def test_idta_schedule_generation(self):
        idta = self.df_engine.generate_idta_schedule("Tara Infotech Ltd", "Tara Infotech India Pvt Ltd")
        self.assertIn("INTERNATIONAL DATA TRANSFER AGREEMENT", idta)
        self.assertIn("Section 119A Data Protection Act 2018", idta)
        self.assertIn("Tara Infotech Ltd", idta)
        self.assertIn("Tara Infotech India Pvt Ltd", idta)

    # -------------------------------------------------------------
    # REST API INTEGRATION TESTS
    # -------------------------------------------------------------
    def test_api_ai_governance_endpoints(self):
        r1 = self.client.get("/api/ai-governance/tools-catalog")
        self.assertEqual(r1.status_code, 200)

        r2 = self.client.post("/api/ai-governance/audit", json={
            "selected_tools": ["chatgpt_consumer"],
            "selected_data_types": ["consultation_health"]
        })
        self.assertEqual(r2.status_code, 200)
        data = r2.json()
        self.assertIn("overall_score", data)

        r3 = self.client.post("/api/ai-governance/generate-dpia", json={"audit_result": data})
        self.assertEqual(r3.status_code, 200)
        self.assertIn("content", r3.json())

        r4 = self.client.post("/api/ai-governance/generate-aup", json={"audit_result": data})
        self.assertEqual(r4.status_code, 200)
        self.assertIn("content", r4.json())

    def test_api_data_flow_endpoints(self):
        r1 = self.client.get("/api/data-flow/presets")
        self.assertEqual(r1.status_code, 200)

        r2 = self.client.post("/api/data-flow/topology", json={"preset_id": "tara-consultation"})
        self.assertEqual(r2.status_code, 200)
        self.assertIn("nodes", r2.json())

        r3 = self.client.post("/api/data-flow/generate-idta", json={
            "company_name": "Tara Infotech Ltd",
            "overseas_entity": "Tara Infotech India Pvt Ltd"
        })
        self.assertEqual(r3.status_code, 200)
        self.assertIn("content", r3.json())

if __name__ == "__main__":
    unittest.main()
