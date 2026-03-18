# Flex Arbitrage

Calculating electricity price arbitrage across countries and times

## Installation

Install using pip:

```bash
pip install flexarb
```

Or using uv (recommended):

```bash
uv add flexarb
```

## Quick Start

```python
import flexarb

print(flexarb.__version__)
```

### Command Line Interface

Flex Arbitrage provides a command-line interface:

```bash
# Show version
flexarb --version

# Say hello
flexarb hello World
```

## Development

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for package management

### Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/TommyWoh/flex-arbitrage.git
cd flex-arbitrage
uv sync --group dev
```

### Running Tests

```bash
uv run pytest
```

### Code Quality

```bash
# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type check
uv run ty check
```

### Prek Hooks

Install prek hooks:

```bash
prek install
```

## License

This project is licensed under the Proprietary License - see the [LICENSE](https://github.com/TommyWoh/flex-arbitrage/blob/main/LICENSE) file for details.
