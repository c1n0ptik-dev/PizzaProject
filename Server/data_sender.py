import serial
import time

# Initialize serial communication
ser = serial.Serial("COM3", baudrate=9600, timeout=1)

while True:
    # Prompt user for input
    user_input = input("Enter order number to start cooking (or 'q' to quit): ")

    if user_input.lower() == "q":
        print("Exiting program.")
        break
    elif user_input.isdigit():
        order_number = user_input
        command = f"Order{order_number}"
        ser.write((command + "\n").encode())
        print(f"Cooking started for Order {order_number}. Waiting for completion...")

        while True:
            if ser.in_waiting > 0:
                response = ser.readline().decode().strip()
                if response == f"Order {order_number} finished":
                    print(f"Order {order_number} is ready! Green LED is now ON.")
                    break
            time.sleep(1)
    else:
        print("Invalid input, please enter a numeric order number or 'q' to quit.")

ser.close()
