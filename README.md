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

The repository currently contains only this documentation, but it is intended to be a Python package. To prepare a development environment:

1. Ensure Python 3.11 or higher is installed.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies once they are defined in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Dependencies

Planned dependencies include:

- `mistral-client` (or an equivalent library) to communicate with the Mistral LLM.
- Standard Python modules such as `json`, `argparse`, and `logging`.

A complete list will be added as implementation progresses.


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

You can now generate a world using `scripts/generate_world.py`:

```bash
python scripts/generate_world.py "<prompt>" --output world.json
```

This will request world data from the Mistral LLM, then save the JSON output to `world.json`.

---

This project is in its early stages, and contributions are welcome as we work toward a fully functional generator.
