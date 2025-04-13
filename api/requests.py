import subprocess
import time  # Optional: to wait for the server to start

def start_dash_server(project_path="."):
    """
    Starts the Next.js development server in the specified project path.

    Args:
        project_path (str): The path to your Next.js project directory.
                           Defaults to the current working directory.
    """
    try:
        # Construct the command
        command = ["npm", "run", "dev"]

        # Execute the command in the specified directory
        process = subprocess.Popen(command, cwd=project_path)

        print(f"Started Next.js development server in the background (PID: {process.pid}).")
        print(f"Make sure your Next.js app is configured to run on the desired port (e.g., http://localhost:3000 or http://localhost:5000).")

        # Optional: Wait for a short period to allow the server to start
        time.sleep(5)  # Adjust this value as needed

        return process  # Return the process object if you need to interact with it later

    except FileNotFoundError:
        print("Error: 'npm' command not found. Make sure Node.js and npm are installed and in your PATH.")
        return None
    except Exception as e:
        print(f"An error occurred while starting the Next.js server: {e}")
        return None
