import serial
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt

# Set up the serial port (adjust the port name and baud rate as needed)
ser = serial.Serial('COM4', 115200)  # Replace 'COM4' with your ESP32's serial port

# Use the full path for the CSV file
csv_file_path = 'C:/users/zangt/onedrive/desktop/kexxu/ps4con_script/motor_speed_log.csv'

# Open the CSV file for writing
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Motor Speed', 'Distance'])  # Write header

    print("Logging data... Press Ctrl+C to stop.")
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
                print(f"Received line: {line}")  # Debugging print statement
                if "Motor Speed:" in line and "Distance:" in line:
                    parts = line.split()
                    motor_speed = parts[2]  # Extract motor speed value
                    distance = parts[-1]  # Extract distance value
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
                    writer.writerow([timestamp, motor_speed, distance])  # Write to CSV file
                    print(f"Logged: {timestamp}, Motor Speed: {motor_speed}, Distance: {distance}")

            time.sleep(0.1)  # Small delay to avoid high CPU usage

    except KeyboardInterrupt:
        print("Logging stopped.")

# Load the CSV data
data = pd.read_csv(csv_file_path)
print(data.head())  # Print first few rows of the DataFrame to verify content

# Convert the Timestamp column to datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Plot the data
plt.figure(figsize=(10, 5))

# Plot motor speed
plt.subplot(2, 1, 1)
plt.plot(data['Timestamp'], data['Motor Speed'], label='Motor Speed', color='b')
plt.xlabel('Timestamp')
plt.ylabel('Motor Speed')
plt.title('Motor Speed Over Time')
plt.legend()

# Plot distance
plt.subplot(2, 1, 2)
plt.plot(data['Timestamp'], data['Distance'], label='Distance', color='r')
plt.xlabel('Timestamp')
plt.ylabel('Distance')
plt.title('Distance Over Time')
plt.legend()

# Adjust layout and show plot
plt.tight_layout()
plt.show()
