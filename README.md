# DevCrew - AI-Powered Software Development Lifecycle

DevCrew is an AI-powered software development automation tool that manages the entire software development lifecycle using specialized AI agents. It supports multiple frameworks and follows best practices for each chosen technology stack.

## Features

- 🤖 AI-powered development crew with specialized agents
- 🏗️ Framework-agnostic project setup
- 📝 Comprehensive documentation generation
- ✅ Automated testing setup
- 🔄 CI/CD pipeline configuration
- 🛠️ Best practices enforcement

## Prerequisites

- Python 3.9+
- Docker (for containerized usage)
- OpenAI API key
- Serper API key (for web searches)

## Installation

### Standalone Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/dev-crew.git
cd dev-crew
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your API keys
```

### Docker Installation

1. Build the Docker image:

```bash
docker build -t dev-crew .
```

## Usage

### Standalone Usage

1. Run as a CLI tool:

```bash
# Basic usage
crew run "Create a modern web application with Next.js and TypeScript"

# Specify project name
crew run --project-name my-app "Create a REST API with FastAPI"

# Set custom timeout
crew run --timeout 7200 "Create a full-stack application"
```

2. Available commands:

```bash
crew run      # Run a new project
crew train    # Train the crew (for development)
crew replay   # Replay a specific task
crew test     # Run test iterations
```

### API Server Usage

1. Start the API server:

```bash
# Using Python
uvicorn dev_crew.api.main:app --reload

# Using Docker
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key dev-crew
```

2. API Endpoints:

```bash
POST /projects/
- Create a new project
- Body: {
    "requirements": "Project requirements",
    "project_name": "optional-name",
    "timeout": 3600
  }

GET /projects/{project_id}
- Get project status

POST /projects/{project_id}/cancel
- Cancel a running project
```

### Docker Compose Usage

1. Start all services:

```bash
docker-compose up -d
```

2. Access the services:

- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Monitoring: http://localhost:8000/metrics

## Configuration

### Environment Variables

```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
MODEL_NAME=gpt-4  # or other OpenAI model
LOG_LEVEL=INFO
```

### Framework Configuration

Framework-specific configurations are stored in `src/dev_crew/config/best_practices.yaml`. Add new frameworks by following the existing structure:

```yaml
frameworks:
  nextjs:
    setup:
      - command: "..."
        description: "..."
    dependencies:
      core: [...]
      dev: [...]
```

## Development

1. Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

2. Run tests:

```bash
pytest
```

3. Format code:

```bash
black src/
isort src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:

1. Check the [documentation](docs/)
2. Open an issue
3. Contact the maintainers

## Acknowledgments

- OpenAI for the GPT models
- CrewAI framework
- All contributors
