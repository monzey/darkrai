import os
import json
from typing import Any, Dict, Optional

from urllib import request as urlrequest
from urllib.error import HTTPError
from llama_cpp import Llama
import requests

from transformers import AutoTokenizer, AutoModelForCausalLM,LlamaTokenizerFast,LlamaTokenizer

class MistralClient:
    """Client for interacting with the Mistral model via API or local checkpoint."""

    def __init__(self, api_key: Optional[str] = None, model: str = "mistral-7b", checkpoint: Optional[str] = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.model = model
        self.checkpoint = checkpoint
        self.session = requests.Session() if requests else None

        if checkpoint:
            self.local_model = Llama(
                model_path=checkpoint,
                n_ctx=2048,
                n_threads=os.cpu_count() or 4,
            )
        else:
            if not self.api_key:
                raise ValueError("API key must be provided via argument or MISTRAL_API_KEY environment variable")
            self.local_model = None

    def _call_api(self, prompt: str, **kwargs: Any) -> str:
        url = "https://api.mistral.ai/v1/chat/completions"
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        payload.update(kwargs)
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        if self.session is not None:
            response = self.session.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        else:  # fallback without requests
            req = urlrequest.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            try:
                with urlrequest.urlopen(req) as resp:
                    data = json.load(resp)
            except HTTPError as exc:  # pragma: no cover - network errors
                raise RuntimeError(f"HTTP error {exc.code}") from exc

        return data["choices"][0]["message"]["content"]

    def _call_local(self, prompt: str, **kwargs: Any) -> str:
        if not self.local_model:
            raise RuntimeError("Local model not configured")
        result = self.local_model(
            prompt,
            max_tokens=2000,
            stop=["###"],
            temperature=0.7,
            top_p=0.95,
            **kwargs
        )
        return result["choices"][0]["text"]

    def generate_world(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """Generate world data from a prompt.

        The model is expected to return a JSON string describing the world.
        This method parses the string into a Python dictionary.
        """
        prePrompt = """ Tu es un moteur de génération de mondes pour jeu de rôle.

        Ton objectif est de générer un monde riche, cohérent et immersif pour une partie de jeu de rôle. Tu dois répondre uniquement avec un objet JSON valide et structuré comme suit :

        ```json
        {
            "name": "Nom du monde",
            "description": "Brève description du monde et de son ambiance",
            "factions": [
                {
                    "name": "Nom de la faction",
                    "ideology": "Ce en quoi ils croient",
                    "influence": "Zone ou sphère d'influence",
                    "relationships": {
                        "Nom d'une autre faction": "relation (allié, ennemi, neutre)"
                    }
                }
            ],
            "locations": [
                {
                    "name": "Nom de l'endroit",
                    "type": "ville, ruine, forêt, etc.",
                    "description": "Brève description",
                    "faction_presence": ["Nom de faction", "autre faction"]
                }
            ],
            "notable_figures": [
                {
                    "name": "Nom du personnage",
                    "role": "fonction ou statut (roi, mage, chef rebelle...)",
                    "traits": ["brave", "rusé", "sanguinaire"]
                }
            ],
            "starting_situation": {
                "conflict": "Problème ou crise majeure actuelle",
                "mystery": "Élément étrange ou inconnu qui intrigue les habitants",
                "opportunities": ["quête 1", "quête 2", "quête 3"]
            }
        }
        ```
        Réponds strictement avec un JSON valide, sans explication, sans balises Markdown ni texte additionnel.
        """
        text = self._call_local(prePrompt + " " + prompt, **kwargs) if self.checkpoint else self._call_api(prompt, **kwargs)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Model output is not valid JSON: {text}") from exc

