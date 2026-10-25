"""
Tara PrivacyOS — Phase 2 Statutory RAG Package
Exports:
- TaraRAGEngine: Master RAG orchestrator for grounded legal Q&A and document audits
- LegalRetriever: Fast hybrid vector & lexical search engine
- STATUTORY_CORPUS: Comprehensive UK GDPR and India DPDPA statutory database
"""

from tara_privacyos.rag.corpus_data import STATUTORY_CORPUS, get_corpus, get_corpus_stats
from tara_privacyos.rag.retriever import LegalRetriever
from tara_privacyos.rag.rag_engine import TaraRAGEngine

__all__ = [
    "TaraRAGEngine",
    "LegalRetriever",
    "STATUTORY_CORPUS",
    "get_corpus",
    "get_corpus_stats"
]
