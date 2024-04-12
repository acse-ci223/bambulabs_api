import bambulabs_api as bl

IP = '192.168.1.200'
SERIAL = 'AC12309BH109'
ACCESS_CODE = '12347890'

if __name__ == '__main__':
    print('Starting bambulabs_api example')
    print('Connecting to Bambulabs 3D printer')
    print(f'IP: {IP}')
    print(f'Serial: {SERIAL}')
    print(f'Access Code: {ACCESS_CODE}')

    # Create a new instance of the API
    printer = bl.Printer(IP, SERIAL, ACCESS_CODE)

    # Connect to the Bambulabs 3D printer
    printer.connect()

    # Get the printer status
    status = printer.get_state()
    print(f'Printer status: {status}')

    # Disconnect from the Bambulabs 3D printer
    printer.disconnect()
