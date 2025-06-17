"""Utility to store generated worlds in a LlamaIndex vector store."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def store_world_in_index(world: Dict[str, Any], index_dir: str) -> None:
    """Persist the given ``world`` into a LlamaIndex vector store.

    Parameters
    ----------
    world:
        Dictionary describing the world.
    index_dir:
        Directory where the vector index will be persisted.

    The ``llama-index`` package must be installed. If it is not available,
    a ``RuntimeError`` is raised.
    """

    try:
        from llama_index import (
            VectorStoreIndex,
            StorageContext,
            load_index_from_storage,
            Document,
        )
    except ImportError as exc:  # pragma: no cover - dependency missing
        raise RuntimeError("llama-index is required to store worlds") from exc

    path = Path(index_dir)
    path.mkdir(parents=True, exist_ok=True)

    text = json.dumps(world, ensure_ascii=False)
    doc = Document(text=text)

    if any(path.iterdir()):
        storage = StorageContext.from_defaults(persist_dir=str(path))
        index = load_index_from_storage(storage)
        index.insert(doc)
    else:
        index = VectorStoreIndex.from_documents([doc])

    index.storage_context.persist(persist_dir=str(path))
