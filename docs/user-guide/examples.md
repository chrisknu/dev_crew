# DevCrew Usage Examples

## Starting the API Server

1. Start the server:
```bash
uvicorn dev_crew.api.main:app --reload --port 8000
```

The API server will be available at `http://localhost:8000`. You can access the Swagger documentation at `http://localhost:8000/docs`.

## Common Usage Patterns

### 1. Creating a Next.js Application

```bash
python -m dev_crew "Create a Next.js application with the following features:
- TypeScript configuration
- TailwindCSS for styling
- Authentication using NextAuth.js
- Blog functionality with MDX
- PostgreSQL database
- API routes for data management"
```

Expected output:
```
Starting SDLC process for project: next_js_20240122_123456
Requirements: Create a Next.js application...

[Project Manager] Analyzing requirements...
[Architect] Designing system architecture...
[Senior Engineer] Setting up framework...
[Senior Engineer] Implementing requirements...
[QA Engineer] Testing solution...
[Technical Writer] Creating documentation...

✅ Project setup validation passed

Generated Artifacts:
    docs/
        requirements/
            project_plan.md
        architecture/
            architecture.md
        technical_design/
            technical_design.md
        implementation/
            implementation_summary.md
    src/
        app/
        components/
        lib/
        styles/
```

### 2. Creating a Backend API

```bash
python -m dev_crew --project-name api-server "Create a FastAPI backend with:
- User authentication and authorization
- PostgreSQL database with SQLAlchemy
- RESTful endpoints for CRUD operations
- Swagger documentation
- Rate limiting
- Error handling
- Unit tests"
```

Expected output:
```
Starting SDLC process for project: api-server
Requirements: Create a FastAPI backend...

[Project Manager] Analyzing requirements...
[Architect] Designing system architecture...
[Senior Engineer] Setting up framework...
[Senior Engineer] Implementing requirements...
[QA Engineer] Testing solution...
[Technical Writer] Creating documentation...

✅ Project setup validation passed

Generated Artifacts:
    docs/
        requirements/
            project_plan.md
        architecture/
            architecture.md
        technical_design/
            technical_design.md
        implementation/
            implementation_summary.md
    src/
        api/
        models/
        database/
        tests/
```

### 3. Full-Stack Application

```bash
python -m dev_crew --project-name fullstack-app "Create a full-stack application with:
- Next.js frontend
- FastAPI backend
- PostgreSQL database
- Docker configuration
- CI/CD pipeline
- Authentication
- Testing setup"
```

### 4. Documentation Generation

```bash
python -m dev_crew --project-name docs-update "Generate comprehensive documentation for a project with:
- API documentation
- User guides
- Developer guides
- Architecture diagrams
- Deployment instructions"
```

## Project Requirements Format

When providing requirements, structure them clearly:

```bash
python -m dev_crew "Create a [type] application with:
- [Feature 1]
- [Feature 2]
- [Feature 3]
...
Additional context:
- [Context 1]
- [Context 2]"
```

## What to Expect

1. **Initial Analysis**
   - Project Manager analyzes requirements
   - Creates detailed project plan
   - Breaks down tasks

2. **Architecture Design**
   - Architect designs system architecture
   - Selects technology stack
   - Creates technical specifications

3. **Implementation**
   - Sets up project structure
   - Installs dependencies
   - Implements features
   - Follows best practices

4. **Testing**
   - Creates test suites
   - Runs tests
   - Validates implementation

5. **Documentation**
   - Generates comprehensive docs
   - Creates user guides
   - Documents API endpoints

## Output Structure

The generated project will have this structure:
```
project_name/
├── docs/                    # Documentation
│   ├── requirements/        # Project requirements and plan
│   ├── architecture/        # System architecture
│   ├── technical_design/    # Technical specifications
│   └── implementation/      # Implementation details
│
├── src/                     # Source code
│   ├── app/                # Application code
│   ├── components/         # React components
│   ├── lib/               # Utility functions
│   └── styles/            # CSS/styling
│
├── tests/                  # Test suites
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── package.json           # Project dependencies
├── tsconfig.json         # TypeScript configuration
├── next.config.js       # Next.js configuration
└── README.md           # Project documentation
```

## Common Issues and Solutions

### 1. API Key Issues
```
Error: OpenAI API key not found
Solution: Check .env file configuration
```

### 2. Project Creation Issues
```
Error: Directory already exists
Solution: Use a different project name or remove existing directory
```

### 3. Dependency Issues
```
Error: Module not found
Solution: Run pip install -e . again
```

## Best Practices

1. **Clear Requirements**
   - Be specific about features
   - Include any constraints
   - Specify technology preferences

2. **Project Organization**
   - Use meaningful project names
   - Keep requirements focused
   - Review generated documentation

3. **Development Flow**
   - Review the project plan first
   - Check the architecture design
   - Test implemented features
   - Review generated tests