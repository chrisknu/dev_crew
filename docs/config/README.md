# Configuration Guide

This document outlines the configuration structure for the DevCrew project.

## Configuration Files

The project uses YAML files for configuration, located in `src/dev_crew/config/`:

- `agents.yaml`: Defines agent roles and capabilities
- `tasks.yaml`: Defines tasks and their requirements

## Agent Configuration

Agents are defined in `agents.yaml` with the following structure:

```yaml
agent_name:
  role: Agent's role title
  goal: Primary objective
  backstory: Context and background
  allow_delegation: true/false
  verbose: true/false
  tools:
    - tool1
    - tool2
```

### Example Agent Configuration

```yaml
senior_react_engineer:
  role: Senior React Engineer
  goal: Build high-quality React components
  backstory: Expert in React development with focus on performance
```

## Task Configuration

Tasks are defined in `tasks.yaml` with the following structure:

```yaml
task_name:
  description: Task description
  agent: agent_name
  dependencies:
    - other_task_name
  expected_output: Expected result description
```

### Example Task Configuration

```yaml
analyze_requirements:
  description: Analyze project requirements and create technical specifications
  agent: senior_analyst
  dependencies: []
  expected_output: Technical specification document
```

## Environment Variables

Environment variables are managed through `.env` file:

```
OPENAI_API_KEY=your_key_here
BROWSERLESS_API_KEY=your_key_here (optional)
SERPER_API_KEY=your_key_here (optional)
```

## Best Practices

1. Keep sensitive information in `.env`
2. Use descriptive names for agents and tasks
3. Define clear goals and expectations
4. Document dependencies between tasks
5. Use version control for configuration changes
