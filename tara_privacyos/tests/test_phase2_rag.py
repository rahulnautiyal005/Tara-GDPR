"""
Tara PrivacyOS — Phase 2 RAG Engine Test Suite
Tests:
1. Statutory Corpus Loading & Schema Integrity
2. Hybrid Semantic & Lexical Vector Retrieval
3. Exact Citation Boosting (Art 9, Sec 8, IDTA, PECR, RoPA)
4. RAG Query Grounding & Statutory Citation Badges
5. RAG Document Audit & Redline Replacement
"""

import unittest
from tara_privacyos.rag.corpus_data import get_corpus, get_corpus_stats
from tara_privacyos.rag.retriever import LegalRetriever
from tara_privacyos.rag.rag_engine import TaraRAGEngine

class TestPhase2RAG(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = get_corpus()
        cls.retriever = LegalRetriever()
        cls.rag_engine = TaraRAGEngine()

    def test_corpus_integrity(self):
        self.assertGreater(len(self.corpus), 10, "Corpus should contain at least 10 statutory chunks")
        stats = get_corpus_stats()
        self.assertIn("UK_GDPR", stats["jurisdictions"])
        self.assertIn("INDIA_DPDPA", stats["jurisdictions"])
        self.assertIn("PECR", stats["jurisdictions"])

    def test_article_9_retrieval(self):
        query = "Do I need explicit consent for processing spiritual, health and astrology data under UK GDPR?"
        results = self.retriever.search(query, top_k=3)
        self.assertGreater(len(results), 0)
        citations = [r["id"] for r in results]
        self.assertIn("UK-GDPR-ART-09", citations, "Article 9 should be top retrieved for sensitive data query")
        self.assertGreater(results[0]["similarity_score"], 0.3)

    def test_data_retention_and_erasure_retrieval(self):
        query = "Can we keep user chat history forever or do we need to delete it under GDPR?"
        results = self.retriever.search(query, top_k=3)
        citations = [r["id"] for r in results]
        self.assertTrue(
            "UK-GDPR-ART-05" in citations or "UK-GDPR-ART-17" in citations or "MODEL-CLAUSE-RETENTION" in citations,
            "Storage limitation or erasure should be retrieved"
        )

    def test_india_dpdpa_penalties_retrieval(self):
        query = "What is the maximum penalty for data breach under India DPDPA 2023?"
        results = self.retriever.search(query, jurisdiction="INDIA_DPDPA", top_k=2)
        self.assertGreater(len(results), 0)
        self.assertIn(results[0]["id"], ["IN-DPDPA-SEC-08", "IN-DPDPA-SCHEDULE-PENALTIES"])
        self.assertTrue(any("250" in r["penalties"] and ("crore" in r["penalties"].lower()) for r in results))

    def test_pecr_cookie_retrieval(self):
        query = "Do mobile app SDK tracking and cookies require opt-in consent?"
        results = self.retriever.search(query, top_k=3)
        citations = [r["id"] for r in results]
        self.assertIn("ICO-PECR-REG-06", citations)

    def test_rag_end_to_end_query(self):
        res = self.rag_engine.query("What are the international transfer rules if my UK app uses developers in India?")
        self.assertTrue(res["success"])
        self.assertIn("retrieved_citations", res)
        self.assertGreater(len(res["retrieved_citations"]), 0)
        cit_titles = [c["id"] for c in res["retrieved_citations"]]
        self.assertTrue("UK-GDPR-CHAP-V" in cit_titles or "MODEL-CLAUSE-IDTA-CROSSBORDER" in cit_titles)

    def test_rag_document_audit(self):
        draft_policy = """
        We collect user full names, consultation notes, and health or spiritual concerns.
        We retain your personal data for as long as necessary for our business operations.
        Your data may be shared with our overseas team and practitioners in India to deliver consultations.
        """
        audit_res = self.rag_engine.audit_document(draft_policy)
        self.assertIn("issues", audit_res)
        self.assertGreater(len(audit_res["issues"]), 2)
        issue_titles = [i["title"] for i in audit_res["issues"]]
        issue_laws = [i.get("law", "") for i in audit_res["issues"]]
        # Accepts either Article 9 / Special Category / Lawful Basis issues
        self.assertTrue(any("Article 9" in t or "Article 9" in l or "Special Category" in t or "lawful basis" in t.lower() or "legal basis" in t.lower() for t, l in zip(issue_titles, issue_laws)))
        self.assertTrue(any("Retention" in t or "retention" in t.lower() for t in issue_titles))
        self.assertTrue(any("International" in t or "transfer" in t.lower() or "sharing" in t.lower() or "overseas" in t.lower() for t in issue_titles))

if __name__ == "__main__":
    unittest.main()
