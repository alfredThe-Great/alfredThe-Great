import serial, time

arduino = serial.Serial('COM3', 9600)  # change COM3 to your port
time.sleep(2)

for angle in [0, 90, 180, 90]:
    arduino.write(f"{angle}\n".encode())
    print(f"Sent {angle}")
    time.sleep(1)
