#!/usr/bin/env python3
"""
Test Case Generator with Model Manager using Ollama

This script generates test cases from feature descriptions using the Ollama API
with automatic model management - it checks if models are available and offers
to download them with detailed information.

Usage:
    python generate_test_cases_with_model_manager.py "User login functionality with email and password"
    
    python generate_test_cases_with_model_manager.py "Shopping cart add/remove items feature" --format text
    
    python generate_test_cases_with_model_manager.py "File upload with validation for PDF and images" --model llama3:latest
    
    python generate_test_cases_with_model_manager.py "User registration" --model codellama --format json

Example output:
    {
        "test_cases": [
            "Verify that the user can do X.",
            "Verify that the user can do Y.",
            "Verify a negative case for Z."
        ]
    }

Features:
    - Automatic model availability checking
    - Interactive model download confirmation with detailed info
    - Progress tracking during model downloads
    - Smart error handling and recovery
"""

import argparse
import json
import requests
import sys
import time


def get_available_models(base_url="http://localhost:11434"):
    """
    Get list of available models from Ollama.
    
    Args:
        base_url (str): The base URL for the Ollama API
        
    Returns:
        list: List of available model names
        
    Raises:
        requests.exceptions.RequestException: If the API call fails
    """
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=10)
        response.raise_for_status()
        data = response.json()
        return [model['name'] for model in data.get('models', [])]
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to get available models: {e}")


def get_model_info(model_name, base_url="http://localhost:11434"):
    """
    Get detailed information about a model from Ollama.
    
    Args:
        model_name (str): Name of the model to get info for
        base_url (str): The base URL for the Ollama API
        
    Returns:
        dict: Model information including size, parameters, etc.
        
    Raises:
        requests.exceptions.RequestException: If the API call fails
    """
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for model in data.get('models', []):
            if model['name'] == model_name:
                return model
                
        return None
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to get model info: {e}")


def pull_model(model_name, base_url="http://localhost:11434"):
    """
    Pull a model from Ollama.
    
    Args:
        model_name (str): Name of the model to pull
        base_url (str): The base URL for the Ollama API
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Pulling model '{model_name}'... This may take a few minutes.")
        
        response = requests.post(
            f"{base_url}/api/pull",
            json={"name": model_name},
            stream=True,
            timeout=300  # 5 minute timeout for pulling
        )
        response.raise_for_status()
        
        # Stream the response to show progress
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    if 'status' in data:
                        print(f"Status: {data['status']}")
                    if 'completed' in data and 'total' in data:
                        completed = data['completed']
                        total = data['total']
                        if total > 0:
                            percent = (completed / total) * 100
                            print(f"Progress: {completed}/{total} ({percent:.1f}%)")
                except json.JSONDecodeError:
                    continue
        
        print(f"Successfully pulled model '{model_name}'!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error pulling model '{model_name}': {e}")
        return False


def format_size(size_bytes):
    """Convert bytes to human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def confirm_model_download(model_name, model_info):
    """
    Ask user to confirm model download with detailed information.
    
    Args:
        model_name (str): Name of the model to download
        model_info (dict): Model information from Ollama
        
    Returns:
        bool: True if user confirms, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Model '{model_name}' is not available locally.")
    print(f"{'='*60}")
    
    if model_info:
        size = format_size(model_info.get('size', 0))
        modified = model_info.get('modified_at', 'Unknown')
        details = model_info.get('details', {})
        param_size = details.get('parameter_size', 'Unknown')
        family = details.get('family', 'Unknown')
        
        print(f"Model Information:")
        print(f"  • Size: {size}")
        print(f"  • Parameters: {param_size}")
        print(f"  • Family: {family}")
        print(f"  • Last Modified: {modified}")
    else:
        print(f"Model Information: Not available locally")
        print(f"  • Will be downloaded from Ollama registry")
    
    print(f"\nThis will download the model to your local Ollama installation.")
    print(f"Download time depends on your internet connection and model size.")
    
    while True:
        response = input(f"\nDo you want to download '{model_name}'? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def ensure_model_available(model_name, base_url="http://localhost:11434"):
    """
    Ensure the requested model is available, pulling it if necessary.
    
    Args:
        model_name (str): Name of the model to ensure is available
        base_url (str): The base URL for the Ollama API
        
    Returns:
        bool: True if model is available, False otherwise
    """
    try:
        # Check if model is already available
        available_models = get_available_models(base_url)
        if model_name in available_models:
            print(f"Model '{model_name}' is available locally.")
            return True
        
        # Get model information for confirmation (only available for local models)
        print(f"Checking model information for '{model_name}'...")
        model_info = get_model_info(model_name, base_url)
        
        # Ask user to confirm download
        if not confirm_model_download(model_name, model_info):
            print("Model download cancelled by user.")
            return False
        
        # Pull the model
        return pull_model(model_name, base_url)
        
    except requests.exceptions.RequestException as e:
        print(f"Error checking model availability: {e}")
        return False


def call_ollama_api(feature_description, model="codellama", base_url="http://localhost:11434"):
    """
    Call the Ollama API to generate test cases from a feature description.
    
    Args:
        feature_description (str): The feature description to generate test cases for
        model (str): The Ollama model to use (default: codellama)
        base_url (str): The base URL for the Ollama API (default: localhost:11434)
    
    Returns:
        dict: The parsed JSON response containing test cases
        
    Raises:
        requests.exceptions.RequestException: If the API call fails
        json.JSONDecodeError: If the response is not valid JSON
    """
    # Ensure model is available
    if not ensure_model_available(model, base_url):
        raise requests.exceptions.RequestException(f"Model '{model}' is not available and could not be downloaded.")
    
    # Construct the prompt for the AI
    prompt = f"""You are a QA automation expert. Given the following feature description, write a list of high-level test cases in JSON format. The JSON should have a single key called 'test_cases'. The test cases should cover functional and edge cases. Feature: {feature_description}."""
    
    # Prepare the API payload
    payload = {
        "model": model,
        "prompt": prompt,
        "format": "json",  # Ensure JSON output format
        "stream": False    # We want the complete response, not streaming
    }
    
    # Make the API call to Ollama
    try:
        response = requests.post(
            f"{base_url}/api/generate",
            json=payload,
            timeout=30  # 30 second timeout
        )
        
        # Check for specific error responses
        if response.status_code == 404:
            try:
                error_data = response.json()
                if 'error' in error_data and 'not found' in error_data['error'].lower():
                    raise requests.exceptions.RequestException(f"Model '{model}' is not available. Please pull it with: ollama pull {model}")
            except (ValueError, KeyError):
                pass  # Fall through to generic 404 error
        
        response.raise_for_status()  # Raise an exception for bad status codes
        
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to call Ollama API: {e}")
    
    # Parse the JSON response
    try:
        response_data = response.json()
        # The actual response content is in the 'response' field
        generated_text = response_data.get('response', '')
        
        # Parse the generated JSON
        test_cases_data = json.loads(generated_text)
        return test_cases_data
        
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Failed to parse JSON response from Ollama: {e}")


def main():
    """
    Main function to handle command-line arguments and generate test cases.
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Generate test cases from feature descriptions using Ollama (V2 with auto-model management)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_test_cases_v2.py "User login with email and password"
  python generate_test_cases_v2.py "Shopping cart add/remove items" --format text
  python generate_test_cases_v2.py "File upload with PDF validation" --model llama3:latest
  python generate_test_cases_v2.py "Payment processing" --base-url http://localhost:11434
  python generate_test_cases_v2.py "User registration" --model codellama --format json
        """
    )
    
    parser.add_argument(
        "feature",
        help="The feature description to generate test cases for"
    )
    
    parser.add_argument(
        "--model",
        default="codellama",
        help="The Ollama model to use (default: codellama)"
    )
    
    parser.add_argument(
        "--base-url",
        default="http://localhost:11434",
        help="The base URL for the Ollama API (default: http://localhost:11434)"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format for test cases (default: json)"
    )
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    try:
        # Call the Ollama API to generate test cases
        print(f"Generating test cases for: {args.feature}")
        print(f"Using model: {args.model}")
        print(f"Output format: {args.format}")
        print("Calling Ollama API...")
        
        test_cases_data = call_ollama_api(
            args.feature,
            model=args.model,
            base_url=args.base_url
        )
        
        # Validate the response structure
        if "test_cases" not in test_cases_data:
            print("Error: Response does not contain 'test_cases' key")
            sys.exit(1)
        
        if not isinstance(test_cases_data["test_cases"], list):
            print("Error: 'test_cases' value is not a list")
            sys.exit(1)
        
        # Print the results as formatted JSON
        print("\nGenerated test cases:")
        print(json.dumps(test_cases_data, indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print("\nMake sure Ollama is running and accessible at the specified URL.")
        print("You can start Ollama with: ollama serve")
        sys.exit(1)
        
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        print("The AI response was not valid JSON. Try running the command again.")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
