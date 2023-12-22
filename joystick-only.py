import serial

# Connect to Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)


def read_arduino_data():
    try:
        serial_data = arduino.readline().decode().strip().split(",")
        joystick_x = int(serial_data[0])
        joystick_y = int(serial_data[1])
    except (ValueError, IndexError):
        joystick_x, joystick_y = 0, 0

    if 0 <= joystick_x <= 250 and 251 <= joystick_y <= 512:
        return 1
    elif 560 <= joystick_x and 402 <= joystick_y <= 512:
        return 2
    elif 251 <= joystick_x <= 512 and 560 <= joystick_y:
        return 3
    elif 251 <= joystick_x <= 512 and 0 <= joystick_y <= 250:
        return 4
    print(joystick_x, joystick_y)
    return 0  # Return 0 if none of the conditions are met


if __name__ == '__main__':
    read_arduino_data()
