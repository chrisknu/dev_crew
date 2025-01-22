# Setting Up DevCrew (Beginner's Guide)

This guide will walk you through setting up DevCrew from scratch, even if you're new to Python.

## Step 1: Install Python

1. Go to [python.org/downloads](https://python.org/downloads)
2. Download Python version 3.10 or higher (but lower than 3.13)
3. Run the installer
   - On Windows: Make sure to check "Add Python to PATH" during installation
   - On Mac: Follow the standard installation process

To verify Python is installed, open a terminal (Command Prompt on Windows) and type:
```bash
python --version
# or
python3 --version
```

## Step 2: Set Up Your Project

1. Open your terminal/Command Prompt
2. Navigate to where you want your project (replace `your-location` with your desired path):
   ```bash
   # Windows
   cd C:\your-location

   # Mac/Linux
   cd /your-location
   ```

3. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Mac/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

   Your prompt should change to show (.venv) at the start.

## Step 3: Install Required Packages

With your virtual environment active, install the required packages:

```bash
pip install 'crewai[tools]'
```

## Step 4: Get Your API Keys

1. Get an OpenAI API key:
   - Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Sign up or log in
   - Create a new API key
   - Copy the key (you'll need it soon)

2. Get a Serper API key:
   - Go to [serper.dev](https://serper.dev)
   - Sign up for an account
   - Get your API key
   - Copy the key

## Step 5: Configure Environment

1. Create a new file named `.env` in your project directory
2. Add your API keys to this file:
   ```
   OPENAI_API_KEY=your-openai-key-here
   SERPER_API_KEY=your-serper-key-here
   ```

## Step 6: Run the Crew

Now you're ready to run! Use this command:

```bash
# Basic usage
python -m dev_crew "Create a modern web app"

# With a specific project name
python -m dev_crew --project-name my-first-app "Create a modern web app"
```

## Common Issues & Solutions

### "Python not found" or "python: command not found"
- Make sure Python is installed
- Try using `python3` instead of `python`
- On Windows: Check if Python was added to PATH during installation

### "ModuleNotFoundError: No module named 'crewai'"
- Make sure your virtual environment is activated (you should see (.venv) in your prompt)
- Try reinstalling the package: `pip install 'crewai[tools]'`

### "Error: OpenAI API key not found"
- Double-check your `.env` file exists and has the correct API keys
- Make sure there are no spaces around the equals sign in the `.env` file
- Make sure the file is named exactly `.env` (including the dot)

### Virtual Environment Not Activating
- On Windows: If you get a permission error, try running PowerShell as administrator
- On Mac/Linux: If `source` doesn't work, try `. .venv/bin/activate`

## Need Help?

If you run into any issues:
1. Double-check each step
2. Make sure you're in the right directory
3. Verify your Python version
4. Ensure your virtual environment is activated
5. Check that your API keys are correctly set up

## Next Steps

Once you've successfully run your first project:
1. Try different project requirements
2. Explore the generated code
3. Read through the project documentation