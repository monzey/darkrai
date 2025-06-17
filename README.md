# Darkrai

Darkrai is an experimental project aiming to create a command-line tool for generating fantasy worlds in a structured JSON format. The core feature will leverage the Mistral large language model (LLM) to autonomously produce a world's geography, environment, and points of interest. This README outlines the project goals, planned JSON schema, setup steps, and how the generator can be run once implemented.

## Project Goals

- Build a simple world generator that interacts with the Mistral LLM.
- Produce output in a standard JSON structure so that clients can easily parse or display the generated world.
- Provide a command-line interface for users to initiate world creation and save the resulting JSON to disk.

### Planned JSON Format

The generator will eventually emit a JSON object similar to the example below:

```json
{
  "world": {
    "name": "string",
    "description": "string",
    "regions": [
      {
        "name": "string",
        "biome": "string",
        "points_of_interest": ["string", "string"]
      }
    ]
  }
}
```

The format may evolve during development.

## Setup

The project is packaged using a standard `pyproject.toml`.

### Manual setup

1. Ensure Python 3.11 or higher is installed.
2. Install [Poetry](https://python-poetry.org/) if you don't already have it:

```bash
pip install --user poetry
```

3. Install the dependencies (Poetry will create a `.venv` automatically):

```bash
poetry install
```

4. Activate the environment and copy `.env.example` to `.env`:

```bash
poetry shell
cp .env.example .env
```

5. *(Optional)* Download the Mistral 7B model checkpoint for local generation:

```bash
darkrai download --destination models/mistral-7b
```

### Using Docker Compose

The `docker-compose.yml` uses the `python:3.11-slim` image and mounts your
working directory. The optional `models` directory is mounted as a volume so
checkpoints are available without being copied into the container. Dependencies
are installed automatically when the container starts.

```bash
# Start an interactive shell
docker compose run darkrai
```

### Dependencies

Planned dependencies include:

- `mistral-client` (or an equivalent library) to communicate with the Mistral LLM.
- Standard Python modules such as `json`, `argparse`, and `logging`.
- `huggingface-hub` for downloading checkpoints from Hugging Face.

A complete list will be added as implementation progresses.


### Environment Variables

Darkrai reads configuration from a local `.env` file if present. Useful variables include:

- `MISTRAL_API_KEY` – API key for the hosted Mistral service
- `HF_TOKEN` – token for downloading model checkpoints from Hugging Face


## Usage

The `MistralClient` can call the hosted Mistral API or load a local model checkpoint.

### Using the API

```python
from darkrai.mistral_client import MistralClient

client = MistralClient(api_key="YOUR_API_KEY")
world = client.generate_world("Create a fantasy world with two kingdoms")
print(world)
```

### Using a local checkpoint

```python
from darkrai.mistral_client import MistralClient

client = MistralClient(checkpoint="/path/to/checkpoint")
world = client.generate_world("Create a fantasy world with two kingdoms")
print(world)
```

The model is expected to return a JSON string which will be parsed into a Python dictionary.



## Running the Generator

You can now generate a world using the `darkrai` command:

```bash
darkrai generate "<prompt>" --output world.json
```

This will request world data from the Mistral LLM, then save the JSON output to `world.json`.

If you want to persist the generated world in a vector store managed by
LlamaIndex, provide an additional directory with `--index`:

```bash
darkrai generate "<prompt>" --output world.json --index index_dir
```

---

This project is in its early stages, and contributions are welcome as we work toward a fully functional generator.
