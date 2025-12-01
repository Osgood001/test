"""Simple Python SDK to talk to the Life Coach backend."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class LifeCoachClient:
    base_url: str = "http://localhost:8000"
    session: Optional[requests.Session] = None

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        sess = self.session or requests.Session()
        response = sess.post(f"{self.base_url}{path}", json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def generate_intervention(
        self, state: str, mood: str, blocker: str, tone: str
    ) -> Dict[str, Any]:
        """Call the intervention endpoint and return structured hints."""
        return self._post(
            "/api/intervention",
            {
                "state": state,
                "mood": mood,
                "blocker": blocker,
                "tone": tone,
            },
        )

    def generate_reflection(
        self, day_quality: str, highlight: str, block: str, experiment: str
    ) -> Dict[str, Any]:
        """Call the reflection endpoint and return a reflection summary."""
        return self._post(
            "/api/reflection",
            {
                "dayQuality": day_quality,
                "highlight": highlight,
                "block": block,
                "experiment": experiment,
            },
        )
