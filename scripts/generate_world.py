#!/usr/bin/env python
"""Command-line interface for generating a world using Mistral."""

import argparse
import json
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a fantasy world using the Mistral model")
    parser.add_argument("prompt", help="Prompt describing the world to generate")
    parser.add_argument("-o", "--output", help="Output file path. If omitted, prints to stdout")
    parser.add_argument("--api-key", help="API key for Mistral. Defaults to MISTRAL_API_KEY env var")
    parser.add_argument("--model", default="mistral-7b", help="Model name to use (default: mistral-7b)")
    parser.add_argument("--checkpoint", help="Path to local checkpoint instead of using API")

    args = parser.parse_args()

    # Allow running the script without installing the package
    src_path = Path(__file__).resolve().parents[1] / "src"
    sys.path.insert(0, str(src_path))

    from darkrai import MistralClient
    client = MistralClient(api_key=args.api_key, model=args.model, checkpoint=args.checkpoint)
    world = client.generate_world(args.prompt)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(world, f, indent=2)
    else:
        json.dump(world, sys.stdout, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
