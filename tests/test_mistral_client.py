import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from darkrai.mistral_client import MistralClient


def test_api_key_required():
    with pytest.raises(ValueError):
        MistralClient()


def test_generate_world_parses_json(monkeypatch):
    client = MistralClient(api_key="dummy")
    monkeypatch.setattr(client, "_call_api", lambda prompt, **kw: '{"name": "test"}')
    result = client.generate_world("prompt")
    assert result == {"name": "test"}
