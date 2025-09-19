import serial
import time

# Replace "COM3" with your Arduino port (Linux/macOS use "/dev/ttyUSB0" or "/dev/ttyACM0")
arduino = serial.Serial("COM3", 9600, timeout=1)
time.sleep(2)  # wait for Arduino to reset

print("Moving servo...")

# Sweep servo using Python
for angle in range(0, 181, 30):
    arduino.write(f"{angle}\n".encode())
    print(f"Sent angle: {angle}")
    time.sleep(1)

arduino.close()
