from flask import Flask, render_template, request, jsonify
import pyautogui
import time
from PIL import Image, ImageFilter
import boto3
import datetime
import os
import math
from pynput import mouse, keyboard
import sys
import threading
import logging
import socket
import psutil  # For battery status

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
activity_log_file = 'activity_logs.txt'

# Default configuration
config = {
    "interval": 300,  # Default screenshot interval (in seconds)
    "blur": False,    # No blur by default
    "scripted_activity_threshold": 500,  # Threshold for scripted activity detection (in pixels)
    "battery_threshold": 20  # Low battery threshold percentage
}

bucket_name = 'my-pythonproject'  # Replace with your S3 bucket name

# AWS S3 client
s3 = boto3.client('s3')

# PID file for single instance management
pid_file = 'activity_tracker.pid'  # Use a relative path for Windows

# Variables to track mouse activity
mouse_last_position = None
scripted_activity_flagged = False  # Flag for scripted activity
last_timezone = None  # Variable to store the last detected timezone

# Queue for uploads when no internet connection is available
upload_queue = []

# Function to check internet connection
def check_internet_connection():
    try:
        # Attempt to connect to a public DNS server (Google)
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# Function to check battery status
def check_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        is_plugged = battery.power_plugged
        logging.info(f"Battery percentage: {percent}% | Charging: {'Yes' if is_plugged else 'No'}")
        return percent, is_plugged
    return None, None

# Function to log mouse movements and detect scripted activity
def detect_mouse_movement(x, y):
    global mouse_last_position, scripted_activity_flagged
    if mouse_last_position is not None:
        distance = math.sqrt((x - mouse_last_position[0]) ** 2 + (y - mouse_last_position[1]) ** 2)
        
        # Check for irregular mouse movements
        if distance > config["scripted_activity_threshold"]:
            scripted_activity_flagged = True
            logging.info("Scripted mouse movement detected! Distance: {}".format(distance))
            log_activity("Scripted mouse movement detected! Distance: {}".format(distance))
        else:
            scripted_activity_flagged = False  # Reset if movement is normal
    else:
        logging.info("First mouse movement detected.")

    mouse_last_position = (x, y)

# Function to log keyboard presses
def monitor_keyboard(key):
    logging.info(f"Key pressed: {key}")
    log_activity(f"Key pressed: {key}")

# Start input listeners
def start_input_listeners():
    mouse_listener = mouse.Listener(on_move=detect_mouse_movement)
    keyboard_listener = keyboard.Listener(on_press=monitor_keyboard)
    mouse_listener.start()
    keyboard_listener.start()

# Function to get the current time zone
def get_current_timezone():
    return time.tzname[time.daylight]

# Function to log the current time zone
def log_timezone():
    global last_timezone
    current_timezone = get_current_timezone()
    if current_timezone != last_timezone:
        logging.info(f"Time zone changed: {last_timezone} -> {current_timezone}")
        last_timezone = current_timezone

# Function to continuously monitor time zone changes in a separate thread
def monitor_timezone():
    global last_timezone
    last_timezone = get_current_timezone()  # Initial timezone
    while True:
        log_timezone()  # Check and log timezone
        time.sleep(60)  # Check every 60 seconds

### Screenshot Handling ###
def take_screenshot():
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"screenshot_{timestamp}.png"
    
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(file_name)  # Save locally
        logging.info(f"Screenshot taken and saved as {file_name}")  # Log screenshot saved
    except Exception as e:
        logging.error(f"Error taking screenshot: {e}")

    if config['blur']:
        try:
            img = Image.open(file_name)
            img = img.filter(ImageFilter.GaussianBlur(5))
            img.save(file_name)
            logging.info(f"Screenshot blurred and saved as {file_name}")
        except Exception as e:
            logging.error(f"Error applying blur: {e}")

    return file_name

### Upload to S3 with Error Handling ###
def upload_to_s3(file_name, bucket):
    if os.path.getsize(file_name) == 0:
        logging.error(f"Error: {file_name} is empty.")
        return

    try:
        logging.info(f"Uploading {file_name} to {bucket}...")
        s3.upload_file(file_name, bucket, file_name)
        logging.info(f"Uploaded {file_name} to {bucket}")
    except Exception as e:
        logging.error(f"Error uploading to S3: {e}")
        upload_queue.append(file_name)  # Queue for later upload

### Background Process ###
def start_tracking():
    start_input_listeners()  # Start tracking mouse and keyboard input
    threading.Thread(target=monitor_timezone, daemon=True).start()  # Start timezone monitoring in a new thread
    while True:
        # Check battery status before uploading
        battery_percentage, is_plugged = check_battery_status()
        if battery_percentage is not None:
            if battery_percentage < config["battery_threshold"] and not is_plugged:
                logging.warning("Low battery detected. Suspending activity tracking to save power.")
                time.sleep(60)  # Pause tracking if battery is low
                continue
        
        if check_internet_connection():  # Check for internet connection before uploading
            if upload_queue:  # If there are files queued for upload
                logging.info("Trying to upload queued files...")
                for file_name in upload_queue[:]:  # Use a copy of the list
                    upload_to_s3(file_name, bucket_name)
                    upload_queue.remove(file_name)  # Remove successfully uploaded file from queue

        file_name = take_screenshot()  # Always take a screenshot
        upload_to_s3(file_name, bucket_name)  # Upload to S3
        time.sleep(config['interval'])  # Wait for the next screenshot

### Activity Logging ###
def log_activity(activity):
    with open(activity_log_file, 'a') as log_file:
        log_file.write(f"{datetime.datetime.now()}: {activity}\n")

### Instance Management ###
def check_single_instance():
    if os.path.isfile(pid_file):
        print("Another instance is running. Exiting...")
        sys.exit()
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))

def cleanup():
    if os.path.isfile(pid_file):
        os.remove(pid_file)

### API Endpoint for Configuration ###
@app.route('/api/config', methods=['POST'])
def set_config():
    global config
    data = request.get_json()
    config['interval'] = int(data.get('interval', 300))
    config['blur'] = data.get('blur', 'false').lower() == 'true'
    config['scripted_activity_threshold'] = int(data.get('scripted_activity_threshold', 500))
    config['battery_threshold'] = int(data.get('battery_threshold', 20))  # Set battery threshold
    logging.info(f"Config updated: interval={config['interval']} seconds, blur={config['blur']}, scripted_activity_threshold={config['scripted_activity_threshold']}, battery_threshold={config['battery_threshold']}")
    return jsonify({"message": "Configuration updated successfully!"})

### Serve Frontend ###
@app.route('/')
def index():
    return render_template('index.html')

### Main Function ###
if __name__ == '__main__':
    check_single_instance()  # Ensure only one instance is running
    try:
        start_tracking()  # Start the screenshot tracking directly in the main thread
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    finally:
        cleanup()  # Cleanup PID file on exit
