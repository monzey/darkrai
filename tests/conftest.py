import sys
import types

# Provide a minimal stub for the llama_cpp module so that imports succeed
module = types.ModuleType("llama_cpp")
class DummyLlama:
    def __init__(self, *args, **kwargs):
        pass
    def __call__(self, prompt: str, **kwargs):
        return {"choices": [{"text": ""}]}
module.Llama = DummyLlama
sys.modules.setdefault("llama_cpp", module)

# Minimal requests stub
requests_module = types.ModuleType("requests")
class DummyResponse:
    def __init__(self, json_data=None):
        self._json = json_data or {}
    def raise_for_status(self):
        pass
    def json(self):
        return self._json
class DummySession:
    def post(self, *args, **kwargs):
        return DummyResponse({"choices": [{"message": {"content": ""}}]})
requests_module.Session = DummySession
sys.modules.setdefault("requests", requests_module)

# Minimal transformers stub
transformers_module = types.ModuleType("transformers")
class Dummy:
    pass
transformers_module.AutoTokenizer = Dummy
transformers_module.AutoModelForCausalLM = Dummy
transformers_module.LlamaTokenizerFast = Dummy
transformers_module.LlamaTokenizer = Dummy
sys.modules.setdefault("transformers", transformers_module)
