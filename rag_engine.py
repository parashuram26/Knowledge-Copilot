"""
RAG Engine — searches KB articles and queries Claude for answers
"""

import os
import json
import anthropic
from pathlib import Path


class RAGEngine:
    def __init__(self, kb_path: str = "data/kb_articles"):
        self.kb_path = Path(kb_path)
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.kb_content = self._load_kb()

    def _load_kb(self) -> str:
        """Load all markdown KB articles into a single context string."""
        content = ""
        for md_file in self.kb_path.glob("*.md"):
            content += f"\n\n## {md_file.stem.replace('_', ' ').title()} (file: {md_file.name})\n"
            content += md_file.read_text()
        return content

    async def search(self, question: str) -> dict:
        """Run RAG query: inject KB into prompt, get structured response."""
        system_prompt = f"""You are a helpful customer support chatbot. Answer ONLY using the KB below.

KNOWLEDGE BASE:
{self.kb_content}

Respond ONLY with this JSON structure:
{{
  "answer": "string",
  "confidence": 0.0,
  "citations": [{{"article": "string", "section": "string", "file": "string"}}],
  "topic": "account|billing|technical|general",
  "should_escalate": false
}}

Confidence: 0.85–1.0 = direct match, 0.6–0.84 = partial, 0.3–0.59 = weak, 0–0.29 = no match.
Set should_escalate=true when confidence < 0.55."""

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": question}]
        )

        raw = "".join(b.text for b in response.content if hasattr(b, "text"))
        clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
