import serial
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt


ser = serial.Serial('COM4', 115200)  


csv_file_path = 'C:/users/zangt/onedrive/desktop/kexxu/ps4con_script/motor_speed_log.csv'


with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Motor Speed', 'Distance'])  

    print("Logging data... Press Ctrl+C to stop.")
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()  
                print(f"Received line: {line}")  
                if "Motor Speed:" in line and "Distance:" in line:
                    parts = line.split()
                    motor_speed = parts[2]  
                    distance = parts[-1]  
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  
                    writer.writerow([timestamp, motor_speed, distance])  
                    print(f"Logged: {timestamp}, Motor Speed: {motor_speed}, Distance: {distance}")

            time.sleep(0.1) 

    except KeyboardInterrupt:
        print("Logging stopped.")


data = pd.read_csv(csv_file_path)
print(data.head())  


data['Timestamp'] = pd.to_datetime(data['Timestamp'])


plt.figure(figsize=(10, 5))


plt.subplot(2, 1, 1)
plt.plot(data['Timestamp'], data['Motor Speed'], label='Motor Speed', color='b')
plt.xlabel('Timestamp')
plt.ylabel('Motor Speed')
plt.title('Motor Speed Over Time')
plt.legend()


plt.subplot(2, 1, 2)
plt.plot(data['Timestamp'], data['Distance'], label='Distance', color='r')
plt.xlabel('Timestamp')
plt.ylabel('Distance')
plt.title('Distance Over Time')
plt.legend()


plt.tight_layout()
plt.show()
