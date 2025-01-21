# DevCrew Documentation

This documentation provides a comprehensive overview of the DevCrew project, which is built using crewAI v0.95.0.

## Directory Structure

```
docs/
├── README.md           - This file
├── architecture/      - System architecture documentation
├── config/           - Configuration documentation
└── tools/            - Tools and utilities documentation

src/
├── dev_crew/
│   ├── config/       - Project configuration files
│   ├── tools/        - Custom tools implementation
│   ├── crew.py       - Main crew implementation
│   └── main.py       - Application entry point
├── tests/            - Test suite
└── output/           - Generated outputs

```

## Quick Links

- [Configuration Guide](config/README.md)
- [Tools Documentation](tools/README.md)
- [Architecture Overview](architecture/README.md)

## Getting Started

1. Ensure Python >=3.10 <3.13 is installed
2. Install UV package manager: `pip install uv`
3. Install dependencies: `crewai install`
4. Add your `OPENAI_API_KEY` to `.env`
5. Run the project: `crewai run`

## Environment Setup

Required environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `BROWSERLESS_API_KEY`: For web automation (optional)
- `SERPER_API_KEY`: For search capabilities (optional)

## Project Overview

DevCrew is a crewAI-based project that implements a multi-agent AI system for development tasks. The system uses:

- crewAI for agent orchestration
- OpenAI's models for agent intelligence
- Custom tools for specific tasks
- YAML-based configuration for flexibility

For more detailed information, please refer to the specific documentation sections linked above.
