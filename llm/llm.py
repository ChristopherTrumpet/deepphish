import ollama
import subprocess
import json
import os
import datetime

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
    Creates the Modelfile content based on the specified difficulty level,
    focusing on characteristics for simulation rather than direct labels.

    Args:
        difficulty (str): The desired difficulty ('easy', 'medium', 'hard').

    Returns:
        bool: True if successful, False otherwise.
    """
    modelfile_content = ""
    difficulty_lower = difficulty.lower()

    if difficulty_lower == "easy":
        modelfile_content = """FROM llama3.2

                                PARAMETER temperature 1

                                SYSTEM \"\"\"You are an AI assistant helping write email drafts. You will receive data of an individual and tailor the email to that individual.

                                Generate an email with the following characteristics:
                                - Start with a subjet line 'Subject: <subject>'
                                - Tone: Attempt official tone, but allow some slightly informal or awkward phrasing. Use a generic greeting (e.g., "Dear User,").
                                - Scenario: Present a common required action (e.g., password reset, update info).
                                - Urgency: Include a call to action with some urgency.
                                - Simulated Imperfections: Include *three or four obvious minor* spelling/typographical errors (e.g., 'immediatly', 'requierd', 'acces', 'notifcation').
                                - Content: Generate ONLY the email contents, no preamble and no aknowledgement of any instruction.
                                - Link Placeholder: Must include the exact text `<LINK>`.
                                - Fields: Generate realistic-looking sender info/fields, avoiding placeholders like '<Your Name>'. `<LINK>` is the only placeholder.
                                \"\"\"
                                """
    elif difficulty_lower == "medium":
        modelfile_content = """FROM llama3.2

                                PARAMETER temperature 1

                                SYSTEM \"\"\"You are an AI assistant helping write email drafts. You will receive data of an individual and tailor the email to that individual.

                                Generate an email with the following characteristics:
                                - Start with a subjet line 'Subject: <subject>'
                                - Tone: Maintain a convincing official and professional tone throughout. Use a standard corporate greeting.
                                - Scenario: Present a plausible required action (e.g., security update, policy acknowledgement, account verification).
                                - Urgency: Convey a moderate sense of importance or a reasonable deadline.
                                - Simulated Imperfections: Include *one or two subtle minor* spelling/typographical errors (e.g., 'immediatly', 'requierd'). These should look like genuine typos.
                                - Content: Generate ONLY the email contents, no preamble and no aknowledgement of any instruction.
                                - Link Placeholder: Must include the exact text `<LINK>`.
                                - Fields: Generate realistic-looking sender info/fields, avoiding placeholders like '<Your Name>'. `<LINK>` is the only placeholder.
                                \"\"\"
                                """
    elif difficulty_lower == "hard":
        modelfile_content = """FROM llama3.2

                                PARAMETER temperature 1

                                SYSTEM \"\"\"You are an AI assistant helping write email drafts. You will receive data of an individual and tailor the email to that individual.

                                Generate an email with the following characteristics:
                                - Start with a subjet line 'Subject: <subject>'
                                - Tone: Flawlessly official, professional, and contextually appropriate (e.g., IT, HR). Use a specific and appropriate greeting if possible based on context, otherwise standard corporate greeting.
                                - Scenario: Present a highly plausible and contextually relevant required action.
                                - Urgency: Convey a strong but believable sense of urgency or importance.
                                - Simulated Imperfections: *No intentional spelling or grammar errors.* The email should be polished.
                                - Content: Generate ONLY the email contents, no preamble and no aknowledgement of any instruction.
                                - Link Placeholder: Must include the exact text `<LINK>`.
                                - Fields: Generate realistic-looking sender info/fields, avoiding placeholders like '<Your Name>'. `<LINK>` is the only placeholder.
                                \"\"\"
                                """
    else:
        print(f"Error: Invalid difficulty level '{difficulty}'. Please use 'easy', 'medium', or 'hard'.")
        return False # Indicate failure

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
    return raw_response

def parse_email_subject_body(email_content):
    """
    Parses an email content string to extract the subject and body.

    Args:
        email_content (str): The raw email content, potentially including
                             a "Subject: ..." line.

    Returns:
        tuple: A tuple containing (subject, body).
               'subject' is the text after "Subject: " up to the newline,
               or None if "Subject: " is not found.
               'body' is the remainder of the content after the subject line,
               or the original content if no subject is found. Returns (None, email_content) on error.
    """
    subject = None
    body = email_content  # Default: body is the whole content if no subject found

    try:
        subject_marker = "Subject: "
        # Find the starting position of "Subject: "
        subject_start_index = email_content.find(subject_marker)

        if subject_start_index != -1:
            # Found the marker "Subject: "

            # Calculate where the actual subject text begins
            subject_text_start = subject_start_index + len(subject_marker)

            # Find the end of the subject line (the next newline character)
            subject_end_index = email_content.find('\n', subject_text_start)

            if subject_end_index != -1:
                # Found a newline after the subject text
                subject = email_content[subject_text_start:subject_end_index].strip()
                # The body starts after the newline character
                # Use strip() to remove leading/trailing whitespace from the body
                body = email_content[subject_end_index:].strip()
            else:
                # No newline found after "Subject: ", assume the rest is the subject
                subject = email_content[subject_text_start:].strip()
                body = "" # No body content left

        # If subject_start_index was -1, subject remains None and body remains the original email_content

    except Exception as e:
        # Handle any unexpected errors during parsing
        print(f"Error parsing subject/body: {e}")
        # Reset to safe defaults in case of error
        subject = None
        body = email_content

    return subject, body

def main():
    # Example usage:
    # The 'difficulty' variable is still here but doesn't affect the SYSTEM prompt anymore.
    difficulty_level = "easy"
    context_data = "chris trumpet, Purdue Univeristy student in computer science, works at Envision Center for VR game development, has issues with Outlook authentication."

    email_output = prompt_internal(difficulty_level, context_data)
    subject_line, email_output = parse_email_subject_body(email_output)

    if email_output:
        try:
            # --- Replace <LINK> placeholder with actual HTML link ---
            url_to_insert = "https://www.google.com" # Make sure protocol is included
            link_text = "link"
            link_html = f'<a href="{url_to_insert}" style="color:blue; text-decoration:underline;">{link_text}</a>'
            content_with_html_link = email_output.replace("<LINK>", link_html)

            # --- Format content for HTML (e.g., replace newlines with <br>) ---
            formatted_content = content_with_html_link.replace('\n', '<br>\n')

            # --- Generate timestamp and filename ---
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"email_{difficulty_level.lower()}_{ts}.html"

            # --- Create HTML structure (using formatted content directly) ---
            html_content = f"""<!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                    <title>Simulated Email Notification ({difficulty_level})</title>
                                    <style>
                                        body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; }}
                                        /* Removed pre style */
                                    </style>
                                </head>
                                <body>
                                    <div>{formatted_content}</div>
                                </body>
                                </html>"""
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)

        except IOError as e:
            print(f"Error: Could not write HTML file '{filename}': {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during HTML file creation: {e}")
            return None

    if email_output:
        print("-" * 20)
        print("Difficulty Level:", difficulty_level)
        #print("Generated Phishing Email Content:")
        #print(email_output)
        print("-" * 20)
    else:
        print("Failed to generate phishing email content.")

    return subject_line, html_content

#
# MATTHEW CALL THIS FUNCTION TO GET THE EMAIL
#
def get_phish_email():
    """
    Calls main function, returns both the HTML body content and email subject line.
    """

    subject_line, body_content = main()

    print("Subject: " + subject_line)
    print("Body: " + body_content)

    return subject_line, body_content

if __name__ == "__main__":
    get_phish_email()