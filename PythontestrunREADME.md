import serial
import time

SERIAL_PORT = 'COM8'  # change this
BAUD_RATE = 9600

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print("Connected to Arduino!")

while True:
    val = input("Enter value (0-180, 90=stop, q=quit): ")
    if val.lower() == 'q':
        break

    try:
        value = int(val)
        if 0 <= value <= 180:
            arduino.write(f"{value}\n".encode())
            print(f"Sent: {value}")
        else:
            print("Value must be 0–180.")
    except ValueError:
        print("Invalid input.")

arduino.close()
