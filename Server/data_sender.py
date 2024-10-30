import serial
import time

# Initialize serial communication with Arduino
ser = serial.Serial("COM4", baudrate=9600, timeout=1)
time.sleep(2)  # Allow time for Arduino to initialize

# Send the command to start the sequence
ser.write("StartSequence\n".encode())
print("Command sent: StartSequence")

# Wait for response from Arduino
while True:
    if ser.in_waiting > 0:
        response = ser.readline().decode().strip()
        print("Arduino:", response)

        # Break if the sequence is finished
        if response == "Sequence finished":
            break

# Close the serial connection
ser.close()
