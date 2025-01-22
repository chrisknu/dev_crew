# Quick Start Guide

## Prerequisites

- Python >=3.10 and <3.13
- pip (Python package installer)

## Installation

1. Install CrewAI with tools:
```bash
pip install 'crewai[tools]'
# or alternatively:
pip install crewai crewai-tools
```

2. Create a new project using CrewAI CLI:
```bash
crewai create crew dev_crew
```

3. Clone our extensions repository:
```bash
git clone https://github.com/yourusername/dev-crew.git
cd dev-crew
```

4. Install the package in development mode:
```bash
pip install -e .
```

## Environment Setup

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
MODEL_NAME=gpt-4
LOG_LEVEL=INFO
```

## Usage

You can use DevCrew in several ways:

### Basic Usage
```bash
python -m dev_crew "Create a modern Next.js application with TypeScript and TailwindCSS"
```

### With Custom Project Name
```bash
python -m dev_crew --project-name my-app "Create a FastAPI backend with SQLAlchemy"
```

### With Custom Timeout
```bash
python -m dev_crew --timeout 3600 "Create a full-stack application"
```

## Project Structure

After creation, your project will have this structure:
```
dev_crew/
├── .gitignore
├── pyproject.toml
├── README.md
├── .env
└── src/
    └── dev_crew/
        ├── __init__.py
        ├── main.py
        ├── crew.py
        ├── tools/
        │   ├── custom_tool.py
        │   └── __init__.py
        └── config/
            ├── agents.yaml
            └── tasks.yaml
```

## Next Steps

1. Check out the [User Guide](../user-guide/cli.md) for more detailed usage
2. Review [Best Practices](../user-guide/best-practices.md) for optimal results
3. See [Configuration](../user-guide/configuration.md) for advanced settings