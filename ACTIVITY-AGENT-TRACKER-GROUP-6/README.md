# Activity Tracker Agent

GROUP - 6		
(Deepesh Mishra -	7078023111	- deepeshmishra444@gmail.com)
Brajendra Singh Pal	7355053477	palbrajendrasinghpal@gmail.com
dheeraj kumar	9546448566	dheerajroydss@gmail.com
Divyanshu kumar singh	8218618312	divyanshukumarsingh32@gmail.com
Garv Singh	7982823197	garvkrsingh100@gmail.com

## Overview
The **Activity Tracker Agent** is a Python-based application designed to monitor user activity, capture screenshots, and upload activity data to Amazon S3. It operates in the background, detecting real-time user input, handling time zone changes, managing configuration updates, and suspending tracking during low battery situations. The agent also includes error handling for network issues, firewalls, and other disruptions, ensuring seamless data management.

## Core Features

- **Activity Tracking**:
  - Monitors and captures user activity in the background.
  - Differentiates between genuine user inputs and script-based emulators (e.g., irregular mouse movements, unnatural keyboard inputs).
  - Provides options to discard or flag detected scripted activity.

- **Configurable Screenshot Intervals**:
  - Allows users to define intervals for taking screenshots (e.g., every 5, 10 minutes, etc.).
  - Supports configuration updates through a web interface (e.g., screenshot enable/disable, blurred/unblurred captures).

- **Time Zone Management**:
  - Detects time zone changes and adjusts timestamps accordingly.
  - Ensures time zone changes are reflected in activity logs in real time.

- **Data Upload**:
  - Automatically uploads captured screenshots and activity logs to AWS S3.
  - Implements mechanisms for large file uploads, including chunked uploads and compression.
  - Data is encrypted before upload, ensuring secure transmission.

- **Error Handling and Resilience**:
  - Handles scenarios like no internet connection by queuing uploads and retrying when the connection is restored.
  - Safely handles abrupt disconnections to maintain data integrity.
  - Detects firewall issues and provides user-friendly error messages.

- **Instance Management**:
  - Ensures only one instance of the application can run at a time using a lock file.

- **Low Battery Detection**:
  - Detects low battery situations (on laptops) and suspends activity tracking to save power.

- **Website for Configuration**:
  - Provides a user-friendly interface to adjust settings such as screenshot intervals, blur options, and thresholds for scripted activity detection.

## Project Structure


Activity-Tracker-Agent/
│
├── app.py                    # Main application file responsible for running the Flask web server
├── config.txt                # Configuration file for settings such as screenshot intervals and AWS credentials
├── README.md                 # Project documentation with setup instructions and details
├── requirements.txt          # List of Python dependencies needed for the project
│
├── templates/                # Folder containing HTML templates for the web interface
│   └── index.html            # Main HTML configuration page
│
├── static/                   # Folder containing static assets like CSS and JavaScript files
│   ├── css/
│   │   └── styles.css        # CSS for styling the web configuration interface
│   └── js/
│       └── script.js         # JavaScript for handling dynamic interactions on the web page
│
├── logs/                     # Directory for storing activity logs
│   └── activity_logs.txt     # Log file where user activity is recorded
│
└── tests/                    # Directory containing unit tests and integration tests
    └── test_activity.py      # Test cases to validate core features like activity tracking and error handling





## Libraries and Dependencies
The following libraries are required to run the Activity Tracker Agent:

- **Flask**: Web framework for the configuration web interface.
- **Pillow**: For capturing and processing screenshots (blurring, compression).
- **Boto3**: AWS SDK for uploading files to Amazon S3.
- **Pynput**: Monitors keyboard and mouse events.
- **Psutil**: Monitors battery status and system resources.
- **PyAutoGUI**: Captures screenshots at configurable intervals.
- **ConfigParser**: For reading and managing configuration settings.
- **Logging**: Logs all activities and errors.

Install all required dependencies using:
```bash
pip install -r requirements.txt


Configuration
The agent's behavior can be customized using the config.txt file. The following settings can be adjusted:

[settings]
screenshot_interval = 300           # Time (in seconds) between screenshots
blur_screenshots = False            # Whether to blur screenshots (True or False)
aws_access_key = YOUR_ACCESS_KEY    # AWS Access Key
aws_secret_key = YOUR_SECRET_KEY    # AWS Secret Key
bucket_name = your-s3-bucket-name   # AWS S3 Bucket Name
scripted_activity_threshold = 500   # Threshold for detecting scripted activity (in pixels)
battery_threshold = 20              # Battery percentage threshold below which tracking is suspended

[settings]
screenshot_interval = 300           # Time (in seconds) between screenshots
blur_screenshots = False            # Whether to blur screenshots (True or False)
aws_access_key = yicIeqUnoJ+Biv2xvsT5zpyQ5md60sJ1WpZB4owi    # AWS Access Key
aws_secret_key = AKIAS2VS4XVD4XCLEHPQ    # AWS Secret Key
bucket_name = my-pythonproject   # AWS S3 Bucket Name
scripted_activity_threshold = 500   # Threshold for detecting scripted activity (in pixels)
battery_threshold = 20              # Battery percentage threshold below which tracking is suspended


Real-time Configuration
You can update configuration settings through the web interface. Navigate to http://127.0.0.1:5000 in your browser and modify the following parameters:

Screenshot interval (in seconds)
Blurring options (enable/disable)
Scripted activity detection threshold
Low battery threshold

Running the Application
1. Clone the repository:
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository

2. Install the dependencies:
pip install -r requirements.txt

Start the Flask web application:
python app.py

4. Access the Web Interface:
Visit http://127.0.0.1:5000 in your web browser to access the configuration page. From here, you can adjust the agent's settings in real-time.

5. Monitor Activity:
The agent runs in the background, capturing screenshots and tracking user inputs. It uploads activity logs and screenshots to AWS S3 according to the defined settings.

To stop the agent, press Ctrl+C in the terminal running the application.

Error Handling and Resilience
No Internet Connection: If the internet connection is lost, the agent will queue the screenshots for later upload and retry when the connection is restored.
Low Battery: On laptops, if the battery level falls below a defined threshold (default: 20%), the agent suspends tracking until the system is plugged in or the battery level recovers.
Abrupt Disconnection: If the agent is abruptly stopped (e.g., power failure), it will resume from the last state upon restart, ensuring that no data is lost.
Firewall Restrictions: If the application encounters firewall restrictions during uploads, it will log the error and provide an appropriate message.
Testing
Unit Tests:
Ensure core functionalities such as activity tracking, screenshot capturing, and file uploads work as expected. Error scenarios (like internet disconnection) are also tested.

Run the tests:
python -m unittest discover -s tests


Security Considerations
AWS Credentials: Avoid hardcoding AWS credentials directly in the code. Use the config.txt file for storing AWS credentials securely, or set them as environment variables.
Data Encryption: All data is encrypted in transit using secure HTTPS protocols.
Access Control: Ensure that proper access control policies are applied to your S3 bucket to prevent unauthorized access.
License
This project is licensed under the MIT License. See the LICENSE file for more details.


---

### Key Sections of the README:
- **Overview**: A brief introduction to the project, explaining the key functionalities.
- **Project Structure**: A breakdown of all project directories and files, helping developers navigate the codebase.
- **Libraries and Dependencies**: Lists the required Python libraries for the project.
- **Configuration**: Details how to modify the agent’s behavior using the `config.txt` file and the web interface.
- **Running the Application**: Step-by-step instructions on how to clone, set up, and run the application.
- **Error Handling**: Information about how the agent handles network disconnections, battery issues, and abrupt shutdowns.
- **Testing**: Describes how to run unit tests to validate core functionalities.

This README is comprehensive and should provide everything needed to understand and set up the **Activity Tracker Agent**. Let me know if you need any further changes!




