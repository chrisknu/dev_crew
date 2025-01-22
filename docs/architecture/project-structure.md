# Project Structure

## Directory Layout

DevCrew follows a structured organization for both the tool itself and the projects it creates:

```
dev_crew/
├── src/
│   └── dev_crew/
│       ├── api/               # API server implementation
│       │   ├── __init__.py
│       │   ├── main.py       # FastAPI application
│       │   ├── models.py     # API models
│       │   └── routes.py     # API endpoints
│       │
│       ├── config/           # Configuration management
│       │   ├── __init__.py
│       │   ├── settings.py   # Global settings
│       │   └── templates/    # Project templates
│       │
│       ├── tools/            # Tool implementations
│       │   ├── __init__.py
│       │   ├── shell_tool.py
│       │   ├── framework_tool.py
│       │   └── implementation_tool.py
│       │
│       ├── utils/            # Utility functions
│       │   ├── __init__.py
│       │   ├── file_utils.py
│       │   └── validation.py
│       │
│       ├── crew.py          # Core crew implementation
│       └── main.py          # CLI entry point
│
├── docs/                    # Documentation
│   ├── getting-started/     # Getting started guides
│   ├── architecture/        # Architecture documentation
│   ├── user-guide/         # User guides
│   ├── development/        # Development guides
│   ├── api/                # API documentation
│   └── deployment/         # Deployment guides
│
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/              # End-to-end tests
│
├── workspace/             # Generated project workspace
│   └── [project_name]/   # Individual project directory
│
├── .env                   # Environment configuration
├── .env.example          # Example environment file
├── pyproject.toml        # Project metadata and dependencies
├── README.md             # Project documentation
└── docker-compose.yml    # Docker configuration
```

## Generated Project Structure

When DevCrew creates a new project, it follows this structure:

```
[project_name]/
├── docs/
│   ├── requirements/    # Requirements documentation
│   │   └── project_plan.md
│   ├── architecture/   # Architecture documentation
│   │   └── architecture.md
│   ├── technical_design/ # Technical design docs
│   │   └── technical_design.md
│   └── implementation/ # Implementation docs
│       └── implementation_summary.md
│
├── src/
│   ├── app/           # Application code
│   ├── components/    # React components
│   ├── lib/          # Utility functions
│   └── styles/       # CSS/styling files
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── package.json      # Project dependencies
├── tsconfig.json    # TypeScript configuration
├── next.config.js   # Next.js configuration
├── .eslintrc.json  # ESLint configuration
└── README.md       # Project documentation
```

## Key Components

### 1. Source Code Organization

The source code is organized into logical modules:

#### API Module
- `api/`: Contains all API-related code
- FastAPI implementation
- Route definitions
- Request/response models

#### Configuration Module
- `config/`: Handles all configuration
- Settings management
- Environment variables
- Project templates

#### Tools Module
- `tools/`: Contains tool implementations
- Shell command execution
- Framework setup
- Implementation helpers

#### Utilities Module
- `utils/`: Common utility functions
- File operations
- Validation helpers
- Helper functions

### 2. Documentation Structure

Documentation is organized by purpose:

#### Getting Started
- Quick start guide
- Installation instructions
- Basic usage examples

#### Architecture
- System overview
- Component details
- Integration documentation

#### User Guide
- CLI documentation
- API reference
- Configuration guide

#### Development
- Contributing guidelines
- Development setup
- Testing guide

### 3. Test Organization

Tests are organized by scope:

#### Unit Tests
- Individual component tests
- Function-level testing
- Isolated testing

#### Integration Tests
- Component interaction tests
- API endpoint tests
- Database integration

#### End-to-End Tests
- Full workflow tests
- User journey tests
- System integration

## Workspace Management

### Project Isolation

Each generated project is isolated in its own directory:

```python
def create_project_directory(project_name: str) -> str:
    """Create isolated project directory
    
    Args:
        project_name: Name of the project
        
    Returns:
        Project directory path
    """
    project_dir = os.path.join('workspace', project_name)
    os.makedirs(project_dir, exist_ok=True)
    return project_dir
```

### Directory Structure Creation

Project structure is created using templates:

```python
def create_project_structure(project_dir: str):
    """Create project directory structure
    
    Args:
        project_dir: Project directory path
    """
    directories = [
        'docs/requirements',
        'docs/architecture',
        'docs/technical_design',
        'docs/implementation',
        'src/app',
        'src/components',
        'src/lib',
        'src/styles',
        'tests/unit',
        'tests/integration',
        'tests/e2e'
    ]
    
    for directory in directories:
        os.makedirs(os.path.join(project_dir, directory), exist_ok=True)
```

## Configuration Management

### Environment Configuration

Environment variables are managed through `.env` files:

```
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
MODEL_NAME=gpt-4
LOG_LEVEL=INFO
```

### Project Configuration

Project-specific configuration is stored in `best_practices.yaml`:

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

## Project Templates

DevCrew uses templates for generating project files:

```python
def apply_template(template_name: str, context: dict) -> str:
    """Apply template with context
    
    Args:
        template_name: Name of template
        context: Template context
        
    Returns:
        Rendered template
    """
    template = load_template(template_name)
    return template.render(context)
```

## Future Considerations

Planned improvements for project structure:

1. **Enhanced Templates**
   - More framework templates
   - Custom template support
   - Template versioning

2. **Workspace Features**
   - Project archiving
   - Resource cleanup
   - Space optimization

3. **Configuration Management**
   - Advanced configuration
   - Environment profiles
   - Configuration validation