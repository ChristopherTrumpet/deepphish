import ollama
import os

def check_ollama_running():
    """
    Checks if the Ollama server is running by attempting to list models.
    Returns:
        bool: True if Ollama is running, False otherwise.
    """
    try:
        ollama.list()
        return True
    except Exception:
        return False

def get_ollama_response(model_name, prompt):
    """
    Calls the specified Ollama model with a given prompt.

    Args:
        model_name (str): The name of the Ollama model to use (e.g., 'llama2').
        prompt (str): The text prompt to send to the model.

    Returns:
        str: The generated response from the Ollama model.  Returns an empty
             string if there's an error.
    """
    try:
        response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
        # Extract the text from the response.  Handles potential errors.
        if 'message' in response and 'content' in response['message']:
            return response['message']['content']
        else:
            print(f"Error: Unexpected response format from Ollama: {response}")
            return ""
    except ollama.RequestError as e:
        print(f"Error: Ollama request failed: {e}")
        return ""
    except ollama.ResponseError as e:
        print(f"Error: Ollama server error: {e}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""

def get_string_response(model_name, prompt):
    """
    Calls the specified Ollama model and returns the response as a string.
    Wraps the core logic and adds error handling.

    Args:
        model_name (str): The name of the Ollama model to use.
        prompt (str): The input prompt for the model.

    Returns:
        str: The string response from the model, or an error message.
    """
    if not check_ollama_running():
        return "Error: Ollama server is not running or is not accessible.  Please ensure Ollama is running and accessible, and that the model is installed."

    if not prompt:
        return "Error: The input prompt cannot be empty."

    try:
        response_text = get_ollama_response(model_name, prompt)
        if not response_text:  # Check for empty string, indicating an error
             return "Error: Failed to get a valid response from Ollama."
        return response_text
    except Exception as e:
        return f"An error occurred: {e}"

def prompt_internal(difficulty, data):
    """
    Prompts an internal-email model with a specific difficulty level and data.
    """
    if difficulty == ""
    response = get_string_response(model_name, prompt)

    return response

def main():
    """
    Main function to demonstrate the usage of the get_string_response function.
    """
    model_name = "phish"
    prompt = "chris trumpet, Purdue Univeristy student in computer science, works at Envision Center for VR game development, has issues with Outlook authentication."

    response = get_string_response(model_name, prompt)
    print(f"Model: {model_name}")
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    
if __name__ == "__main__":
    main()
