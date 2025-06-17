"""Command line interface for Darkrai."""

import argparse
import json
import os
import sys
from pathlib import Path

from .config import load_env
from .mistral_client import MistralClient


def _cmd_generate(args: argparse.Namespace) -> None:
    """Handle the ``generate`` subcommand."""

    client = MistralClient(
        api_key=args.api_key,
        model=args.model,
        checkpoint=args.checkpoint,
    )
    world = client.generate_world(args.prompt)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(world, f, indent=2)
    else:
        json.dump(world, sys.stdout, indent=2)
        sys.stdout.write("\n")

    if args.index:
        from .index import store_world_in_index
        store_world_in_index(world, args.index)


def _cmd_download(args: argparse.Namespace) -> None:
    from huggingface_hub import snapshot_download, login

    token = os.getenv("HF_TOKEN")
    if token:
        login(token)

    dest = Path(args.destination).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=args.repo_id,
        local_dir=str(dest),
        local_dir_use_symlinks=False,
    )


def main(argv: list[str] | None = None) -> None:
    load_env()

    parser = argparse.ArgumentParser(description="Darkrai CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser("generate", help="Generate a fantasy world")
    gen.add_argument("prompt", help="Prompt describing the world to generate")
    gen.add_argument("-o", "--output", help="File to write JSON output")
    gen.add_argument("--api-key", help="Mistral API key")
    gen.add_argument("--model", default="mistral-7b", help="Model name")
    gen.add_argument("--checkpoint", help="Path to local checkpoint")
    gen.add_argument("--index", help="Directory to store a LlamaIndex vector store")
    gen.set_defaults(func=_cmd_generate)

    dl = subparsers.add_parser("download", help="Download model from Hugging Face")
    dl.add_argument("--repo-id", default="mistralai/Mistral-7B-v0.1", help="Repository id")
    dl.add_argument("-d", "--destination", default="models/mistral-7b", help="Download directory")
    dl.set_defaults(func=_cmd_download)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
