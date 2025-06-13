# darkrai

Utilities for generating world data using Mistral models.

## Installation

```
pip install -r requirements.txt
```

The package depends on `requests` and optionally `transformers` if you want to use a local checkpoint.

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

