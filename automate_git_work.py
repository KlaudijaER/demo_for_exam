import os
import subprocess
import sys
import logging

# Set up logging
logging.basicConfig(filename="todo_app_automation.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run_tests():
    """Run unit tests and return success status."""
    print("Running tests...")
    logging.info("Starting unit tests.")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test*.py"],
        capture_output=True,
        text=True,
    )
    # Print and log the output
    print(result.stdout)
    logging.info(result.stdout)

    if result.returncode == 0:
        print("All tests passed successfully!")
        logging.info("All tests passed successfully!")
        return True
    else:
        print("Some tests failed. Check the logs for details.")
        logging.error("Tests failed:\n%s", result.stderr)
        return False


def clean_test_db(test_db_name="test_todo.db"):
    """Clean up the test database if it exists."""
    if os.path.exists(test_db_name):
        os.remove(test_db_name)
        logging.info(f"Test database '{test_db_name}' removed.")


def run_application():
    """Run the TodoApp main application."""
    try:
        print("Starting the application...")
        logging.info("Launching the TodoApp.")
        subprocess.run([sys.executable, "git_work.py"]) 
    except Exception as e:
        logging.error("Failed to start the application: %s", e)
        print("Error while starting the application. Check the logs for details.")


def main():
    """Main procedure to automate testing and app execution."""
    # Clean up before starting
    clean_test_db()

    # Run tests and proceed only if they pass
    if run_tests():
        run_application()
    else:
        print("Automation aborted due to test failures.")
        logging.info("Automation aborted due to test failures.")


if __name__ == "__main__":
    main()
