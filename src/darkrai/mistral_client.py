import os
import json
from typing import Any, Dict, Optional

from urllib import request as urlrequest
from urllib.error import HTTPError
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
            if AutoTokenizer is None or AutoModelForCausalLM is None:
                raise ImportError("transformers is required for using local checkpoints")
            self.tokenizer = AutoTokenizer.from_pretrained(checkpoint, use_fast=True)
            self.local_model = AutoModelForCausalLM.from_pretrained(checkpoint)
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
        inputs = self.tokenizer(prompt, return_tensors="pt")
        output_ids = self.local_model.generate(**inputs, **kwargs)
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

    def generate_world(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """Generate world data from a prompt.

        The model is expected to return a JSON string describing the world.
        This method parses the string into a Python dictionary.
        """
        text = self._call_local(prompt, **kwargs) if self.checkpoint else self._call_api(prompt, **kwargs)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Model output is not valid JSON: {text}") from exc

