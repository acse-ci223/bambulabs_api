import bambulabs_api as bl

IP = '192.168.1.200'
SERIAL = 'AC12309BH109'
ACCESS_CODE = '12347890'

# Create a new instance of the API
api = bl.Client(IP, SERIAL, ACCESS_CODE)

api.connect()

api.loop_forever()
