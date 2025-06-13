#!/usr/bin/env python
"""Download the Mistral 7B model from Hugging Face."""

import argparse
from pathlib import Path

from huggingface_hub import snapshot_download, login
from dotenv import load_dotenv
import os

load_dotenv()
login(os.getenv("HF_TOKEN"))

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download the Mistral 7B model from Hugging Face"
    )
    parser.add_argument(
        "--repo-id",
        default="mistralai/Mistral-7B-v0.1",
        help="Hugging Face repository id for the model",
    )
    parser.add_argument(
        "-d",
        "--destination",
        default="models/mistral-7b",
        help="Directory to download the model into",
    )

    args = parser.parse_args()

    dest = Path(args.destination).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)

    snapshot_download(
        repo_id=args.repo_id,
        local_dir=str(dest),
        local_dir_use_symlinks=False,
    )


if __name__ == "__main__":
    main()
