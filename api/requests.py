from pynpm import NPMPackage
import threading
import time
import webbrowser

def open_web():
    dashboard_path = "/Users/chris/Development/hack/deepphish/dashboard/package.json"
    pkg = NPMPackage(dashboard_path)
    pkg.run_script('dev')

def start_dash_server(project_path="."):
    """
    Starts the Next.js development server in the specified project path.

    Args:
        project_path (str): The path to your Next.js project directory.
                           Defaults to the current working directory.
    """
    try:
        thread = threading.Thread(target=open_web)
        thread.start()
        time.sleep(1)
        webbrowser.open_new("http://localhost:3000/dashboard")


    except FileNotFoundError:
        print("Error: 'npm' command not found. Make sure Node.js and npm are installed and in your PATH.")
        return None
    except Exception as e:
        print(f"An error occurred while starting the Next.js server: {e}")
        return None
