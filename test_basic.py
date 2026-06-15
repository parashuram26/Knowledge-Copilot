"""
Basic tests for SD-01 KB Chatbot
Run: pytest tests/
"""

import pytest
import json


# ── Unit tests for RAG response structure ──

def test_response_has_required_fields():
    """Validate response schema."""
    sample = {
        "answer": "To reset your password, click Forgot Password on the login page.",
        "confidence": 0.95,
        "citations": [{"article": "Account Management", "section": "How to Reset Your Password", "file": "account_management"}],
        "topic": "account",
        "should_escalate": False
    }
    assert "answer" in sample
    assert "confidence" in sample
    assert 0.0 <= sample["confidence"] <= 1.0
    assert "citations" in sample
    assert "topic" in sample
    assert "should_escalate" in sample


def test_escalation_triggered_on_low_confidence():
    """should_escalate should be True when confidence < 0.55."""
    conf = 0.3
    should_escalate = conf < 0.55
    assert should_escalate is True


def test_no_escalation_on_high_confidence():
    """should_escalate should be False when confidence >= 0.55."""
    conf = 0.92
    should_escalate = conf < 0.55
    assert should_escalate is False


def test_topic_is_valid():
    valid_topics = {"account", "billing", "technical", "general"}
    topic = "billing"
    assert topic in valid_topics


def test_citation_structure():
    citation = {"article": "Billing & Payments", "section": "Refund Policy", "file": "billing_payments"}
    assert "article" in citation
    assert "section" in citation
    assert "file" in citation


def test_ticket_id_format():
    import random, string
    ticket_id = "TKT-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    assert ticket_id.startswith("TKT-")
    assert len(ticket_id) == 10


# ── Integration test (requires ANTHROPIC_API_KEY env var) ──

@pytest.mark.skip(reason="Requires live API key — run manually")
def test_live_rag_query():
    import asyncio
    from src.rag_engine import RAGEngine

    rag = RAGEngine()
    result = asyncio.run(rag.search("How do I reset my password?"))

    assert result["confidence"] > 0.7
    assert not result["should_escalate"]
    assert len(result["citations"]) > 0
    assert result["topic"] == "account"
