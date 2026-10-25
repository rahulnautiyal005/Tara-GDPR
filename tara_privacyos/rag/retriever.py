"""
Tara PrivacyOS — Phase 2 Legal Retriever
High-speed Hybrid Semantic & Lexical Vector Search Engine for Statutory Laws.
Combines:
1. Exact Legal Citation Matching (Article & Section Boosts)
2. BM25 / Lexical Inverted Index
3. Dense Vector Cosine Similarity (Normalized Sub-word & Semantic Hashing)
4. Jurisdiction & Domain Filtering
"""

import re
import math
from typing import List, Dict, Any, Optional, Set
import numpy as np

from tara_privacyos.rag.corpus_data import get_corpus, STATUTORY_CORPUS

STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", 
    "by", "can", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", 
    "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", 
    "him", "himself", "his", "how", "if", "in", "into", "is", "it", "its", "itself", "just", 
    "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once", 
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "s", "same", "she", 
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", 
    "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", 
    "up", "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", 
    "why", "with", "would", "you", "your", "yours", "yourself", "yourselves"
}

def tokenize(text: str) -> List[str]:
    """Extracts alphanumeric tokens and legal citation patterns."""
    text = text.lower()
    # Normalize legal abbreviations
    text = re.sub(r'art\.?\s*(\d+)', r'article \1 article\1', text)
    text = re.sub(r'sec\.?\s*(\d+)', r'section \1 section\1', text)
    tokens = re.findall(r'\b[a-z0-9_-]{2,}\b', text)
    return [t for t in tokens if t not in STOP_WORDS]

class LegalRetriever:
    def __init__(self, corpus: Optional[List[Dict[str, Any]]] = None):
        self.corpus = corpus or get_corpus()
        self.doc_count = len(self.corpus)
        self.vocabulary: Dict[str, int] = {}
        self.inv_index: Dict[str, List[int]] = {}
        self.doc_vectors: Optional[np.ndarray] = None
        self.doc_lengths: List[int] = []
        self.avg_doc_length: float = 0.0
        self.idf: Dict[str, float] = {}
        
        self._build_index()

    def _build_index(self):
        """Builds vocabulary, inverted index, BM25 metadata, and dense TF-IDF vectors."""
        doc_tokens_list = []
        term_doc_freq: Dict[str, int] = {}

        for doc_idx, doc in enumerate(self.corpus):
            # Form weighted combined representation
            weighted_text = (
                f"{doc.get('title', '')} " * 4 +
                f"{doc.get('citation', '')} " * 4 +
                f"{' '.join(doc.get('keywords', []))} " * 3 +
                f"{doc.get('summary', '')} " * 2 +
                f"{' '.join(doc.get('key_requirements', []))} " * 2 +
                f"{doc.get('statutory_text', '')} " +
                f"{doc.get('practical_application', '')} "
            )
            tokens = tokenize(weighted_text)
            doc_tokens_list.append(tokens)
            self.doc_lengths.append(len(tokens))

            # Track unique terms for IDF
            unique_terms = set(tokens)
            for term in unique_terms:
                term_doc_freq[term] = term_doc_freq.get(term, 0) + 1
                if term not in self.inv_index:
                    self.inv_index[term] = []
                self.inv_index[term].append(doc_idx)

        # Build vocabulary dictionary
        vocab_terms = sorted(term_doc_freq.keys())
        self.vocabulary = {term: idx for idx, term in enumerate(vocab_terms)}
        vocab_size = len(self.vocabulary)
        self.avg_doc_length = sum(self.doc_lengths) / max(1, self.doc_count)

        # Compute IDF
        for term, df in term_doc_freq.items():
            # Standard smoothed BM25 IDF
            self.idf[term] = math.log((self.doc_count - df + 0.5) / (df + 0.5) + 1.0)

        # Build normalized TF-IDF dense document matrix for cosine similarity
        self.doc_vectors = np.zeros((self.doc_count, vocab_size), dtype=np.float32)

        for doc_idx, tokens in enumerate(doc_tokens_list):
            counts: Dict[str, int] = {}
            for t in tokens:
                counts[t] = counts.get(t, 0) + 1
            
            for t, cnt in counts.items():
                if t in self.vocabulary:
                    term_idx = self.vocabulary[t]
                    # Log-normalized TF * IDF
                    tf = 1.0 + math.log(cnt)
                    self.doc_vectors[doc_idx, term_idx] = tf * self.idf.get(t, 1.0)

            # L2-normalize vector
            norm = np.linalg.norm(self.doc_vectors[doc_idx])
            if norm > 0:
                self.doc_vectors[doc_idx] /= norm

    def search(
        self,
        query: str,
        jurisdiction: Optional[str] = None,
        category: Optional[str] = None,
        top_k: int = 4,
        min_score: float = 0.05
    ) -> List[Dict[str, Any]]:
        """
        Executes hybrid retrieval combining exact legal citation matching,
        lexical BM25 ranking, and dense cosine similarity.
        """
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        # 1. Exact statutory citation detection (High precision boost)
        citation_boosts: Dict[int, float] = {}
        query_lower = query.lower()

        # Check for specific article/section mentions
        for doc_idx, doc in enumerate(self.corpus):
            cit = doc.get("citation", "").lower()
            doc_id = doc.get("id", "").lower()
            title = doc.get("title", "").lower()
            boost = 0.0

            # Direct match on citation (e.g. "article 9", "section 6", "idta", "ropa", "dpia")
            if "article 9" in query_lower and ("art-09" in doc_id or "article 9" in cit):
                boost += 0.8
            if "article 6" in query_lower and ("art-06" in doc_id or "article 6" in cit):
                boost += 0.7
            if "article 17" in query_lower or "erasure" in query_lower or "forgotten" in query_lower:
                if "art-17" in doc_id or "erasure" in title:
                    boost += 0.75
            if "article 28" in query_lower or "dpa" in query_lower or "processor" in query_lower:
                if "art-28" in doc_id or "dpa" in title:
                    boost += 0.65
            if "article 30" in query_lower or "ropa" in query_lower:
                if "art-30" in doc_id or "ropa" in doc_id or "ropa" in title:
                    boost += 0.8
            if "article 35" in query_lower or "dpia" in query_lower:
                if "art-35" in doc_id or "dpia" in title:
                    boost += 0.8
            if "idta" in query_lower or "international transfer" in query_lower or "cross-border" in query_lower or "cross border" in query_lower:
                if "chap-v" in doc_id or "idta" in doc_id or "crossborder" in doc_id:
                    boost += 0.8
            if "pecr" in query_lower or "cookie" in query_lower or "cookies" in query_lower:
                if "pecr" in doc_id or "cookie" in title:
                    boost += 0.85
            if "section 6" in query_lower and "dpdpa" in query_lower:
                if "sec-06" in doc_id:
                    boost += 0.8
            if "section 8" in query_lower or "250 crore" in query_lower:
                if "sec-08" in doc_id:
                    boost += 0.8
            if "section 9" in query_lower or "children" in query_lower or "minor" in query_lower:
                if "sec-09" in doc_id:
                    boost += 0.8
            if "grievance" in query_lower or "section 13" in query_lower:
                if "sec-13" in doc_id:
                    boost += 0.8
            if "openai" in query_lower or "llm" in query_lower or "chatgpt" in query_lower or "ai" in query_lower:
                if "ai" in doc_id or "openai" in doc_id:
                    boost += 0.5

            if boost > 0:
                citation_boosts[doc_idx] = boost

        # 2. Vector Cosine Similarity
        query_vec = np.zeros(len(self.vocabulary), dtype=np.float32)
        q_counts: Dict[str, int] = {}
        for t in query_tokens:
            q_counts[t] = q_counts.get(t, 0) + 1

        for t, cnt in q_counts.items():
            if t in self.vocabulary:
                term_idx = self.vocabulary[t]
                tf = 1.0 + math.log(cnt)
                query_vec[term_idx] = tf * self.idf.get(t, 1.0)

        q_norm = np.linalg.norm(query_vec)
        if q_norm > 0:
            query_vec /= q_norm
            cosine_scores = np.dot(self.doc_vectors, query_vec)
        else:
            cosine_scores = np.zeros(self.doc_count, dtype=np.float32)

        # 3. BM25 Lexical Score
        k1 = 1.5
        b = 0.75
        bm25_scores = np.zeros(self.doc_count, dtype=np.float32)

        for t in query_tokens:
            if t in self.inv_index and t in self.idf:
                idf_val = self.idf[t]
                posting_list = self.inv_index[t]
                for doc_idx in posting_list:
                    # Term frequency in this doc
                    term_idx = self.vocabulary[t]
                    # Estimate tf
                    tf = (self.doc_vectors[doc_idx, term_idx] / max(1e-5, self.idf[t]))
                    denom = tf + k1 * (1.0 - b + b * (self.doc_lengths[doc_idx] / self.avg_doc_length))
                    bm25_scores[doc_idx] += idf_val * (tf * (k1 + 1.0) / max(1e-5, denom))

        # Normalize BM25 scores to [0, 1] range
        max_bm25 = np.max(bm25_scores) if np.max(bm25_scores) > 0 else 1.0
        norm_bm25 = bm25_scores / max_bm25

        # 4. Hybrid Fusion Score
        final_scores: List[tuple] = []
        for doc_idx in range(self.doc_count):
            doc = self.corpus[doc_idx]

            # Filter checks
            if jurisdiction and jurisdiction.upper() != "ALL":
                doc_jur = doc.get("jurisdiction", "").upper()
                if jurisdiction.upper() not in doc_jur and doc_jur not in jurisdiction.upper():
                    # Keep statutory models if relevant
                    if doc_jur != "STATUTORY_MODEL":
                        continue

            if category and category.lower() not in doc.get("category", "").lower():
                continue

            cos_sc = float(cosine_scores[doc_idx])
            bm_sc = float(norm_bm25[doc_idx])
            boost_sc = citation_boosts.get(doc_idx, 0.0)

            # Combined score with statutory citation boost
            score = (0.50 * cos_sc) + (0.35 * bm_sc) + (0.40 * boost_sc)
            if score >= min_score:
                final_scores.append((doc_idx, score))

        # Sort descending by score
        final_scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for doc_idx, score in final_scores[:top_k]:
            doc = dict(self.corpus[doc_idx])
            doc["similarity_score"] = round(float(score), 4)

            # Highlighted matching keywords
            doc_keywords = doc.get("keywords", [])
            matched_kw = [k for k in doc_keywords if any(qt in k.lower() for qt in query_tokens)]
            doc["matched_keywords"] = matched_kw

            results.append(doc)

        return results

    def get_chunk_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a specific statutory knowledge chunk by its ID."""
        for chunk in self.corpus:
            if chunk.get("id") == chunk_id:
                return dict(chunk)
        return None
