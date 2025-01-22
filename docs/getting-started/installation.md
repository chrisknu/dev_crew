# Installation Guide

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- git
- OpenAI API key
- Serper API key

## Installation Methods

### 1. Direct Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dev-crew.git
cd dev-crew
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

### 2. Docker Installation

1. Build the Docker image:
```bash
docker build -t dev-crew .
```

2. Run with Docker:
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e SERPER_API_KEY=your_key \
  dev-crew
```

### 3. Docker Compose Installation

1. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

2. Start services:
```bash
docker-compose up -d
```

## Configuration

### Environment Variables

Create a `.env` file with:
```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
MODEL_NAME=gpt-4
LOG_LEVEL=INFO
```

### Package Configuration

The package is configured in `pyproject.toml`:
```toml
[project]
name = "dev_crew"
version = "0.1.0"
requires-python = ">=3.10,<3.13"

[project.scripts]
dev_crew = "dev_crew.main:run"
run_crew = "dev_crew.main:run"
train = "dev_crew.main:train"
replay = "dev_crew.main:replay"
test = "dev_crew.main:test"
```

## Verification

Verify installation by running:
```bash
dev_crew --version
```

## Common Issues

### 1. Python Version
Error: "Python version not supported"
Solution: Ensure Python 3.10 or higher is installed

### 2. API Keys
Error: "API key not found"
Solution: Check .env file configuration

### 3. Dependencies
Error: "Module not found"
Solution: Verify installation with `pip list`

## Updates

To update the package:
```bash
git pull
pip install -e .
```