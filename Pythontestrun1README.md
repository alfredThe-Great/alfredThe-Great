import serial
import time

# Change this to your actual COM port
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

# Connect to Arduino
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print("Connected to Arduino!")

while True:
    try:
        angle = input("Enter angle (0-180 or 'q' to quit): ")
        if angle.lower() == 'q':
            break

        angle = int(angle)
        if 0 <= angle <= 180:
            arduino.write(f"{angle}\n".encode())
            print(f"Sent angle: {angle}")
        else:
            print("Angle must be between 0 and 180")

    except ValueError:
        print("Invalid input, try again.")

arduino.close()
print("Connection closed.")
