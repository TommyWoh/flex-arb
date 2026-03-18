# Flex Arbitrage

[![CI](https://github.com/TommyWoh/flex-arbitrage/actions/workflows/ci.yml/badge.svg)](https://github.com/TommyWoh/flex-arbitrage/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/flexarb.svg)](https://badge.fury.io/py/flexarb)
[![codecov](https://codecov.io/gh/TommyWoh/flex-arbitrage/branch/main/graph/badge.svg)](https://codecov.io/gh/TommyWoh/flex-arbitrage)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/badge/type--checked-ty-blue?labelColor=orange)](https://github.com/astral-sh/ty)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-yellow.svg)](https://github.com/TommyWoh/flex-arbitrage/blob/main/LICENSE)

Calculating electricity price arbitrage across countries and times

## Features

- Fast and modern Python toolchain using Astral's tools (uv, ruff, ty)
- Type-safe with full type annotations
- Command-line interface built with Typer
- Comprehensive documentation with MkDocs — [View Docs](https://TommyWoh.github.io/flex-arbitrage/)

## Installation

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

### CLI Usage

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

```bash
git clone https://github.com/TommyWoh/flex-arbitrage.git
cd flex-arbitrage
make install
```

### Running Tests

```bash
make test

# With coverage
make test-cov

# Across all Python versions
make test-matrix
```

### Code Quality

```bash
# Run all checks (lint, format, type-check)
make verify

# Auto-fix lint and format issues
make fix
```

### Prek

```bash
prek install
prek run --all-files
```

### Documentation

```bash
make docs-serve
```

## License

This project is licensed under the Proprietary License - see the [LICENSE](LICENSE) file for details.
