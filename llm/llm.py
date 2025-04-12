import ollama
import subprocess
import json
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

def run_ollama_command(command_list):
    """
    Runs an Ollama command and returns the output.  Handles errors robustly.

    Args:
        command_list (list): A list representing the command and its arguments.

    Returns:
        str: The output of the command, or None on error.
    """
    try:
        process = subprocess.run(command_list, capture_output=True, text=True, check=True)
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"Error: Ollama command not found.  Make sure Ollama is installed and in your PATH.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

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

def modify_modelfile(difficulty):
    """
    Modifies the Modelfile to use the specific llama3.2 configuration
    for generating corporate email drafts with intentional errors and markers.
    """
    # Define the specific Modelfile content
    if (difficulty.lower() == "easy"):
        modelfile_content = """FROM llama3.2

                            PARAMETER temperature 1

                            SYSTEM \"\"\"You are an AI tasked with generating corporate email drafts. Your specific task is to create an email notification for an employee regarding a required action, typically involving accessing a link (like a password reset or account update) Make this really easy for a human to detect as AI generated, with spelling mistakes and informal tone.

                            Follow these rules STRICTLY:
                            1.  **Start Marker:** The entire output MUST begin *exactly* with 'START' and nothing before it.
                            2.  **End Marker:** The entire output MUST end *exactly* with `END` and nothing after it.
                            3.  **Link Placeholder:** You MUST include the exact text `<LINK>` within the email body where the action URL would normally be placed. Do not modify this placeholder.
                            4.  **Tone and Context:** The email's tone should be official and convey importance or urgency, simulating a communication from a company's IT department, HR, or an automated system. Mention things like "security update," "compliance requirement," "account verification," or "mandatory action" to enhance realism.
                            5.  **Minor Spelling Errors:** Intentionally introduce three or four *minor* spelling mistakes (e.g., 'immediatly', 'requierd', 'acces', 'pasword', 'notifcation'). These should look like typos, not grammatical errors. Do *not* misspell common short words like 'the', 'is', 'a'.
                            6.  **Content:** Generate only the email content between the start and end markers. Do not add explanations or preamble.
                            7.  **Other fields:** Do NOT include any other fields such as '<Your Name>' or '<Support Email>', all fields must also have some generated content or name. The only empty field should be the <LINK>.
                            \"\"\"
                            """
    elif (difficulty.lower() == "medium"):
        modelfile_content = """FROM llama3.2

                            PARAMETER temperature 1

                            SYSTEM \"\"\"You are an AI tasked with generating corporate email drafts. Your specific task is to create an email notification for an employee regarding a required action, typically involving accessing a link (like a password reset or account update) Make this moderately hard for a human to detect as AI generated, with only a few spelling errors but formal tone.

                            Follow these rules STRICTLY:
                            1.  **Start Marker:** The entire output MUST begin *exactly* with 'START' and nothing before it.
                            2.  **End Marker:** The entire output MUST end *exactly* with `END` and nothing after it.
                            3.  **Link Placeholder:** You MUST include the exact text `<LINK>` within the email body where the action URL would normally be placed. Do not modify this placeholder.
                            4.  **Tone and Context:** The email's tone should be official and convey importance or urgency, simulating a communication from a company's IT department, HR, or an automated system. Mention things like "security update," "compliance requirement," "account verification," or "mandatory action" to enhance realism.
                            5.  **Minor Spelling Errors:** Intentionally introduce one or two *minor* spelling mistakes (e.g., 'immediatly', 'requierd', 'acces', 'pasword', 'notifcation'). These should look like typos, not grammatical errors. Do *not* misspell common short words like 'the', 'is', 'a'.
                            6.  **Content:** Generate only the email content between the start and end markers. Do not add explanations or preamble.
                            7.  **Other fields:** Do NOT include any other fields such as '<Your Name>' or '<Support Email>', all fields must also have some generated content or name. The only empty field should be the <LINK>.
                            \"\"\"
                            """
    elif (difficulty.lower() == "hard"):
        modelfile_content = """FROM llama3.2

                            PARAMETER temperature 1

                            SYSTEM \"\"\"You are an AI tasked with generating corporate email drafts. Your specific task is to create an email notification for an employee regarding a required action, typically involving accessing a link (like a password reset or account update) Make this impossible for a human to detect as AI generated, it must be totally convincing and real.

                            Follow these rules STRICTLY:
                            1.  **Start Marker:** The entire output MUST begin *exactly* with 'START' and nothing before it.
                            2.  **End Marker:** The entire output MUST end *exactly* with `END` and nothing after it.
                            3.  **Link Placeholder:** You MUST include the exact text `<LINK>` within the email body where the action URL would normally be placed. Do not modify this placeholder.
                            4.  **Tone and Context:** The email's tone should be official and convey importance or urgency, simulating a communication from a company's IT department, HR, or an automated system. Mention things like "security update," "compliance requirement," "account verification," or "mandatory action" to enhance realism.
                            5.  **Content:** Generate only the email content between the start and end markers. Do not add explanations or preamble.
                            6.  **Other fields:** Do NOT include any other fields such as '<Your Name>' or '<Support Email>', all fields must also have some generated content or name. The only empty field should be the <LINK>.
                            \"\"\"
                            """

    # Write the specific content directly to the Modelfile, overwriting it.
    try:
        with open("Modelfile", "w") as f:
            f.write(modelfile_content)
        print("Modelfile updated successfully with the new configuration.")
        return True # Indicate success
    except Exception as e:
        print(f"Error writing Modelfile: {e}")
        return False # Indicate failure

def retrain_model(model_name="phish"):
    """
    Retrains the Ollama model with the modified Modelfile.

    Args:
        model_name (str, optional): The name of the model to create/retrain. Defaults to "phish".

    Returns:
        bool: True if retraining was successful, False otherwise.
    """
    command = ["ollama", "create", model_name, "-f", "./Modelfile"]
    print(f"Retraining model '{model_name}' with updated Modelfile...")
    output = run_ollama_command(command)
    if output is None:
        print(f"Error: Failed to retrain model {model_name}.")
        return False # Indicate Failure
    else:
        # Check Ollama output for success indicators if possible
        # (Ollama's output might vary, simple check for now)
        print(f"Model {model_name} retraining process initiated.")
        # Add a small delay or check `ollama list` if needed to confirm creation
        return True # Indicate Success

def prompt_internal(difficulty, data):
    """
    Prompts an internal-email model with specific data, using the
    pre-defined Modelfile configuration.

    Args:
        difficulty (str): (Currently unused by modify_modelfile but kept for potential future use)
                          The conceptual difficulty level ('easy', 'medium', or 'hard').
        data (str): The data to use as context for the phishing email.

    Returns:
        str: The generated phishing email (between <START> and <END>), or None on error.
    """
    model_name = "phish"  # Consistent model name

    # 1. Modify the Modelfile (using the new fixed configuration).
    #    The 'difficulty' argument is no longer passed here.
    if not modify_modelfile(difficulty):
        return None  # Exit if Modelfile modification failed.

    # 2. Retrain the model.
    if not retrain_model(model_name):
        return None  # Exit if retraining failed.

    # 3. Generate the phishing email content.
    #    The prompt now just needs the contextual data.
    prompt = f"Generate the email based on this context: {data}"
    raw_response = get_string_response(model_name, prompt)

    if raw_response:
        # 4. Extract content between <START>/<END> or *START*/*END* markers.
        start_marker = None
        end_marker = None
        start_index = -1
        end_index = -1

        # --- Find start marker ---
        try:
            start_index = raw_response.index("<START>")
            start_marker = "<START>"
        except ValueError:
            try:
                start_index = raw_response.index("*START*")
                start_marker = "*START*"
            except ValueError:
                # Neither start marker found
                print("Error: Could not find <START> or *START* marker in the response.")
                print(f"Raw response was:\n---\n{raw_response}\n---")
                return None

        # --- Find end marker (must occur *after* start marker) ---
        try:
            end_index = raw_response.index("<END>", start_index)
            end_marker = "<END>"
        except ValueError:
            try:
                end_index = raw_response.index("*END*", start_index)
                end_marker = "*END*"
            except ValueError:
                # Neither end marker found after the start marker
                print(f"Error: Found start marker '{start_marker}' but could not find <END> or *END* marker after it.")
                print(f"Raw response was:\n---\n{raw_response}\n---")
                return None

        # --- Extract content if both markers were found correctly ---
        if start_marker and end_marker and start_index != -1 and end_index != -1:
            # Calculate the actual start position after the marker
            actual_start_index = start_index + len(start_marker)
            # Extract the content and strip leading/trailing whitespace
            extracted_content = raw_response[actual_start_index:end_index].strip()
            return extracted_content
        else:
            # This case should theoretically not be reached due to earlier checks
            print("Error: Failed to determine valid start/end markers for extraction despite initial checks.")
            print(f"Raw response was:\n---\n{raw_response}\n---")
            return None

    else:
        print("Error: Failed to get response from the model.")
        return None # Indicate failure in getting response

def main():
    # Example usage:
    # The 'difficulty' variable is still here but doesn't affect the SYSTEM prompt anymore.
    difficulty_level = "hard"
    context_data = "chris trumpet, Purdue Univeristy student in computer science, works at Envision Center for VR game development, has issues with Outlook authentication."

    email_output = prompt_internal(difficulty_level, context_data)

    if email_output:
        print("-" * 20)
        print("Difficulty Level:", difficulty_level)
        print("Generated Phishing Email Content:")
        print(email_output)
        print("-" * 20)
    else:
        print("Failed to generate phishing email content.")

if __name__ == "__main__":
    main()
