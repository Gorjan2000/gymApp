# ---------------------------------------
# KOD ZA DA SE DOZNAE PATEKATA DO FAJLOT
#
# import os
# import sys
#
# # Determine the base directory of the script
# base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#
# # Construct the file path relative to the base directory
# file_path = os.path.join(base_dir, 'data', 'card_ids.txt')
#
# # Print the resolved file path
# print('Resolved File Path:', file_path)
# ---------------------------------------

import serial
import datetime

# Construct the file path relative to the base directory
file_path = "/Users/gorjanspirovski/Desktop/Ivica app/pythonProject/data/card_ids.txt"

port = '/dev/cu.usbserial-110'  # Replace with the correct serial port
baud_rate = 9600

# Open the serial port
ser = serial.Serial(port, baud_rate)

# Open the text file in read mode
file = open(file_path, 'r')

# Read existing card IDs and dates from the file
existing_card_data = [line.strip().split(', ') for line in file]

# Close the file
file.close()

try:
    while True:
        # Read data from the serial port
        data = ser.readline().decode().strip()

        if data:
            print(data)

            # Check if the card ID exists and today's date is within the range
            for card_data in existing_card_data:
                if data == card_data[0]:  # Card ID matches
                    from_date = datetime.datetime.strptime(card_data[2], "%d-%m-%Y").date()
                    to_date = datetime.datetime.strptime(card_data[3], "%d-%m-%Y").date()
                    today = datetime.date.today()

                    if from_date <= today <= to_date:
                        response = '1'  # Card ID exists and today's date is within the range
                    else:
                        response = '0'  # Card ID exists, but today's date is not within the range
                    break
            else:
                # Card ID does not exist, add it to the file
                from_date = datetime.date.today().strftime("%d-%m-%Y")
                to_date = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%d-%m-%Y")
                existing_card_data.append([data, '', from_date, to_date])
                file = open(file_path, 'a')
                file.write(', '.join([data, '', from_date, to_date]) + '\n')
                file.close()
                response = '0'  # Card ID does not exist

            ser.write(response.encode())  # Send response to the Arduino
            print('Response Sent:', response)

except KeyboardInterrupt:
    print('Keyboard interrupt detected. Exiting...')

finally:
    # Close the serial port
    ser.close()
    file.close()
