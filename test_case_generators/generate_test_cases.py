#!/usr/bin/env python3
"""
Test Case Generator using Ollama

This script generates test cases from feature descriptions using the Ollama API
with the codellama model. It outputs clean JSON with test cases for QA automation.

Usage:
    python generate_test_cases.py "User login functionality with email and password"
    
    python generate_test_cases.py "Shopping cart add/remove items feature" --format text
    
    python generate_test_cases.py "File upload with validation for PDF and images" --model codellama
    
    python generate_test_cases.py "User registration" --model codellama --format json
    
    python generate_test_cases.py "Payment processing" --base-url http://localhost:11434

Example output:
    {
        "test_cases": [
            "Verify that the user can do X.",
            "Verify that the user can do Y.",
            "Verify a negative case for Z."
        ]
    }
"""

import argparse
import json
import requests
import sys


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
        description="Generate test cases from feature descriptions using Ollama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_test_cases.py "User login with email and password"
  python generate_test_cases.py "Shopping cart add/remove items" --format text
  python generate_test_cases.py "File upload with PDF validation" --model codellama
  python generate_test_cases.py "Payment processing" --base-url http://localhost:11434
  python generate_test_cases.py "User registration" --model codellama --format json
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
