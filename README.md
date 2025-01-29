# Sensitive Info App GUI

This application fetches sensitive information (PII) from a Snowflake database and displays it in a GUI window.

## Project Structure

sensitive_info_app_gui/
│
├── dist/                    # Directory for standalone executable (optional)
├── src/                     # Source code directory
│   └── fetch_pii_gui.py     # Main script to fetch and display PII data in a GUI
├── config.py                # Script to set environment variables
├── requirements.txt         # List of required Python packages
├── README.md                # Project setup and usage instructions

## Setup and Installation

1. Clone the Repository
First, clone the repository to your local machine:

"git clone https://github.com/kmallya7/sensitive_info_app_gui.git
cd sensitive_info_app_gui"

2. Set Up Virtual Environment (Recommended)
Create and activate a virtual environment to manage your dependencies.

On macOS/Linux:

"python3 -m venv venv
source venv/bin/activate"

On Windows:

"python -m venv venv
.\venv\Scripts\activate"

3. Install Dependencies
Install the required Python packages by running:

"pip install -r requirements.txt"

4. Set Environment Variables
Run the config.py script to set the necessary environment variables:

"python3 config.py"

5. Run the Application
Finally, run the application:

"python3 src/fetch_pii_gui.py"

