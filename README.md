# DevCrew - AI Development Assistant

DevCrew helps you build software projects using AI. It can create web apps, APIs, and full applications by following your instructions.

## 🚀 Quick Start (5 minutes)

1. Install Python 3.10 or newer from [python.org](https://python.org)

2. Open your terminal and run these commands:
   ```bash
   # Clone the project
   git clone https://github.com/yourusername/dev-crew.git
   cd dev-crew

   # Set up Python environment
   python -m venv .venv
   
   # Activate the environment:
   # On Windows:
   .venv\Scripts\activate
   # On Mac/Linux:
   source .venv/bin/activate

   # Install required packages
   pip install 'crewai[tools]'
   pip install -e .
   ```

3. Get your API keys:
   - Get OpenAI API key from [platform.openai.com](https://platform.openai.com)
   - Get Serper API key from [serper.dev](https://serper.dev)

4. Copy `.env.example` to `.env` and add your API keys:
   ```env
   OPENAI_API_KEY=your-openai-key-here
   SERPER_API_KEY=your-serper-key-here
   ```

5. Try it out:
   ```bash
   # Create a basic website
   python -m dev_crew "Create a simple Next.js website with a homepage and about page"
   ```

## 🎯 What You'll Get

The AI will:
1. Plan your project
2. Set up the code
3. Create documentation
4. Add tests
5. Provide instructions

All files will be in the `workspace` folder.

## 🤔 Need Help?

- Make sure Python is installed correctly
- Check that your API keys are in the `.env` file
- Make sure you activated the environment (you'll see (.venv) in your terminal)
- Look at the [detailed guide](./docs/getting-started/beginner-setup.md) if you need more help

## 📚 Examples

Create a website:
```bash
python -m dev_crew "Create a Next.js website with:
- Homepage
- About page
- Contact form
- Navigation menu"
```

Create an API:
```bash
python -m dev_crew "Create a simple API with:
- User login
- Database
- Basic CRUD operations"
```

## 🛠️ Features

- Creates full projects from descriptions
- Sets up best practices automatically
- Generates documentation
- Adds testing
- Follows modern development standards