import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from darkrai.index import store_world_in_index


def test_store_world_requires_llama_index(tmp_path):
    index_dir = tmp_path / "index"
    with pytest.raises(RuntimeError):
        store_world_in_index({"name": "test"}, str(index_dir))
