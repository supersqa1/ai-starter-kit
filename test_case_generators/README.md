# Test Case Generators

A collection of Python scripts for generating test cases using AI models via Ollama.

## Table of Contents

- [Setup](#setup)
- [Scripts](#scripts)
  - [generate_test_cases.py](#generate_test_casespy)

## Setup

- **Python 3.8+** required
- **Ollama** running on default port (http://localhost:11434)
- **Virtual environment** suggested (use `python3 -m venv venv`)
- **Dependencies**: `pip install requests`
- **Models**: Pull at least one model like `ollama pull llama3:latest`

## Scripts

### generate_test_cases.py

Generates test cases from feature descriptions using AI models.

### generate_test_cases_with_model_manager.py

Enhanced version with automatic model management - checks if models are available and offers to download them with detailed information.

**Help Commands:**
```bash
# V1 (basic)
python test_case_generators/generate_test_cases.py --help

# With model manager
python test_case_generators/generate_test_cases_with_model_manager.py --help
```

**Output:**
```
usage: generate_test_cases.py [-h] [--model MODEL] [--base-url BASE_URL] [--format {json,text}] feature

Generate test cases from feature descriptions using Ollama

positional arguments:
  feature               The feature description to generate test cases for

options:
  -h, --help            show this help message and exit
  --model MODEL         The Ollama model to use (default: codellama)
  --base-url BASE_URL   The base URL for the Ollama API (default: http://localhost:11434)
  --format {json,text}  Output format for test cases (default: json)

Examples:
  python generate_test_cases.py "User login with email and password"
  python generate_test_cases.py "Shopping cart add/remove items" --format text
  python generate_test_cases.py "File upload with PDF validation" --model codellama
  python generate_test_cases.py "Payment processing" --base-url http://localhost:11434
  python generate_test_cases.py "User registration" --model codellama --format json
```

## Usage Examples

```bash
# Basic usage (V1)
python test_case_generators/generate_test_cases.py "User login with email and password"

# Basic usage (with model manager)
python test_case_generators/generate_test_cases_with_model_manager.py "User login with email and password"

# With custom model (will auto-download if needed)
python test_case_generators/generate_test_cases_with_model_manager.py "Shopping cart functionality" --model llama3:latest

# With text output
python test_case_generators/generate_test_cases_with_model_manager.py "File upload feature" --format text

# With custom Ollama URL
python test_case_generators/generate_test_cases_with_model_manager.py "Payment processing" --base-url http://remote-server:11434
```

### Model Manager Features

- **Automatic model checking** - Verifies if requested model is available
- **Model information display** - Shows size, parameters, and family before download
- **Interactive confirmation** - Asks user before downloading large models
- **Progress tracking** - Shows download progress for model pulling
- **Smart error handling** - Better error messages and recovery
