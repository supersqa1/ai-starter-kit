# 🤖 AI Test Case Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Compatible-green.svg)](https://ollama.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-Powered-purple.svg)](https://github.com/ollama/ollama)

> **AI-powered test case generation tools using Ollama for developers and QA engineers.**

## 🚀 Overview

This repository provides **AI-powered test case generation tools** that use local AI models through Ollama. It's designed for developers and QA engineers who want to quickly generate comprehensive test cases from natural language feature descriptions. The tools are simple to use and require minimal setup.

### ✨ Key Features

- 🧪 **Test Case Generation** - Generate test cases from feature descriptions
- 🔧 **Model Management** - Automatic model detection and download (enhanced version)
- 🎯 **Multiple Output Formats** - JSON and text output options
- 🚀 **Easy Setup** - Minimal dependencies and clear documentation
- 🔄 **Flexible Configuration** - Support for different AI models and endpoints

## 🛠️ What's Inside

### 📁 Test Case Generators

Two Python scripts for generating test cases from natural language descriptions:

- **`generate_test_cases.py`** - Basic test case generation with Ollama integration
- **`generate_test_cases_with_model_manager.py`** - Enhanced version with automatic model management

#### 🎯 Capabilities

- **Test Case Generation**: Convert feature descriptions into test cases
- **Model Support**: Works with various AI models (CodeLlama, Llama3, etc.)
- **Output Formats**: JSON and text output options
- **Error Handling**: Basic error handling with helpful messages
- **Model Management**: Automatic model detection and download (enhanced version only)

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** 
- **Ollama** running locally ([Install Ollama](https://ollama.ai))
- **Virtual Environment** (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-starter-kit.git
   cd ai-starter-kit
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install requests
   ```

4. **Start Ollama and pull a model**
   ```bash
   ollama serve
   ollama pull codellama  # or llama3:latest
   ```

### 🎯 Basic Usage

#### Generate Test Cases (Basic Version)
```bash
python test_case_generators/generate_test_cases.py "User login with email and password"
```

#### Generate Test Cases (Enhanced Version)
```bash
python test_case_generators/generate_test_cases_with_model_manager.py "Shopping cart functionality"
```

#### Advanced Examples
```bash
# Custom model with text output
python test_case_generators/generate_test_cases_with_model_manager.py \
  "File upload with PDF validation" \
  --model llama3:latest \
  --format text

# Remote Ollama instance
python test_case_generators/generate_test_cases_with_model_manager.py \
  "Payment processing" \
  --base-url http://remote-server:11434
```

## 📖 Detailed Documentation

### Test Case Generator Features

#### 🔧 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `feature` | Feature description to generate test cases for | Required |
| `--model` | AI model to use (codellama, llama3:latest, etc.) | codellama |
| `--base-url` | Ollama API endpoint | http://localhost:11434 |
| `--format` | Output format (json, text) | json |

#### 🎯 Example Output

**Input:**
```bash
python generate_test_cases.py "User authentication with email and password"
```

**Output:**
```json
{
  "test_cases": [
    "Verify that a user can log in with valid email and password",
    "Verify that login fails with invalid email format",
    "Verify that login fails with incorrect password",
    "Verify that login fails with empty email field",
    "Verify that login fails with empty password field",
    "Verify that user is redirected to dashboard after successful login",
    "Verify that login attempts are logged for security monitoring"
  ]
}
```

### 🧠 Supported AI Models

- **CodeLlama** - Optimized for code-related tasks
- **Llama3** - General-purpose language model
- **Custom Models** - Any Ollama-compatible model

### 🔄 Model Manager Features

The enhanced version includes:

- **Automatic Model Detection** - Checks if requested models are available
- **Interactive Downloads** - Prompts before downloading large models
- **Progress Tracking** - Shows download progress with detailed information
- **Smart Error Recovery** - Better error messages and recovery suggestions
- **Model Information** - Displays model size, parameters, and family details

## 🎨 Use Cases

### 👨‍💻 For Developers
- **API Testing** - Generate test cases for REST API endpoints
- **Feature Validation** - Create comprehensive test scenarios
- **Documentation** - Generate test documentation from specifications

### 🧪 For QA Engineers
- **Test Planning** - Convert requirements into test cases
- **Regression Testing** - Generate edge case scenarios
- **Automation Scripts** - Create test data for automation frameworks

### 🤖 For AI Enthusiasts
- **Model Comparison** - Test different AI models for quality
- **Prompt Engineering** - Experiment with different prompt strategies
- **Local AI Development** - Learn practical AI integration patterns

## 🛠️ Development

### Project Structure
```
ai-starter-kit/
├── test_case_generators/
│   ├── generate_test_cases.py              # Core generator
│   ├── generate_test_cases_with_model_manager.py  # Enhanced version
│   └── README.md                          # Detailed documentation
├── venv/                                  # Virtual environment
├── ai_automation_starter_kit.pdf         # Additional documentation
└── README.md                             # This file
```

### Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🔧 Troubleshooting

### Common Issues

**Model not found error:**
```bash
Error: Model 'codellama' is not available. Please pull it with: ollama pull codellama
```
**Solution:** Run `ollama pull codellama` to download the model.

**Connection refused:**
```bash
Error: Failed to call Ollama API: Connection refused
```
**Solution:** Ensure Ollama is running with `ollama serve`.

**JSON parsing error:**
```bash
Error: Failed to parse JSON response from Ollama
```
**Solution:** Try running the command again or use a different model.

### Getting Help

- 📖 Check the [detailed documentation](test_case_generators/README.md)
- 🐛 [Report issues](https://github.com/yourusername/ai-starter-kit/issues)
- 💬 [Start a discussion](https://github.com/yourusername/ai-starter-kit/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for providing the local AI infrastructure
- [Meta AI](https://ai.meta.com) for the Llama and CodeLlama models
- The open-source community for inspiration and contributions

## 🔗 Related Projects

- [Ollama](https://github.com/ollama/ollama) - Local AI model runner
- [CodeLlama](https://github.com/facebookresearch/codellama) - Code generation models
- [Llama](https://github.com/facebookresearch/llama) - Large language models

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

[🔝 Back to Top](#-ai-test-case-generator)

</div>