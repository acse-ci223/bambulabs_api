"""
Client module for connecting to the Bambulabs 3D printer API
and getting telemetry data from it in real time using MQTT protocol.
"""

from datetime import datetime, timedelta
# from pathlib import Path

import json
import ssl

import paho.mqtt.client as mqtt  # type: ignore
import webcolors  # type: ignore


__all__ = ['Client']


class Client:
    """
    Client Class for connecting to the Bambulabs 3D printer
    """
    def __init__(self, ip_address, access_code, serial, output_path="./"):
        self.ip_address = ip_address
        self.access_code = access_code
        self.serial = serial
        self.values = {}
        self.client = mqtt.Client()
        self.client.check_hostname = False
        self.client.username_pw_set('bblp', self.access_code)
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS,
                            cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def connect(self) -> None:
        """
        connect Connect to the Bambulabs 3D printer

        Returns
        -------
        None
            Nothing
        """
        self.client.connect(self.ip_address, 8883, 60)
        return None

    def _on_connect(self, client, userdata, flags, rc) -> None:
        """
        _on_connect Callback function for when the client
        receives a CONNACK response from the server.

        Parameters
        ----------
        client : mqtt.Client
            The client instance for this callback
        userdata : String
            User data
        flags : Arraylike
            Response flags sent by the broker
        rc : int
            The connection result
        """
        print("Connected with result code " + str(rc))
        self.client.subscribe(f"device/{self.serial}/report")
        return None

    def _split_string(self, string) -> tuple:
        """
        _split_string Split a string into a tuple of 3 integers

        Parameters
        ----------
        string : String
            String to split

        Returns
        -------
        tuple
            Tuple of 3 integers representing the RGB value
        """
        tuple_result = (int(string[:2], 16),
                        int(string[2:4], 16),
                        int(string[4:6], 16))
        return tuple_result

    def _rgb_to_color_name(self, rgb) -> str:
        """
        _rgb_to_color_name Convert an RGB value to a color name

        Parameters
        ----------
        rgb : String
            RGB value to convert to a color name (e.g. "FF0000")

        Returns
        -------
        str
            Color name (e.g. "red")
        """
        try:
            color_tuple = self._split_string(rgb)
            color_name = webcolors.rgb_to_name(color_tuple)
        except ValueError:
            # If the RGB value doesn't match any known color,
            # return the hex code with a 0x prefeix
            color_name = f"0x{rgb}"
        return color_name

    def _on_message(self, client, userdata, msg) -> None:
        """
        _on_message Callback function for when a PUBLISH message
        is received from the server.

        Parameters
        ----------
        client : mqtt.Client
            The client instance for this callback
        userdata : String
            User data
        msg : mqtt.MQTTMessage
            An instance of MQTTMessage. This is a class with members topic,
            payload, qos, retain.

        Returns
        -------
        None
        """
        # Current date and time
        now = datetime.now()
        doc = json.loads(msg.payload)
        # Have something to look at on screen so you know it's spinning
        print(doc)
        # output_dir = Path(self.output_path)
        # JSON blobs written just for debug convenience
        # telem_json_path = output_dir / "telemetry.json"
        # telem_json_err_path = output_dir / "telemetry.err.txt"

        # only reason I split these into separate files was so they could
        # easily be modeled as separate text boxes in OBS
        # telem_text_path = output_dir / "telemetry.txt"
        # ams_text_path = output_dir / "ams.txt"

        try:
            # Write the raw JSON first incase there's a key error
            # when we start trying to access it
            # with telem_json_path.open("w") as fp:
            #     fp.write(json.dumps(doc))

            if not doc:
                return

            globals()['values'] = dict(self.values, **doc['print'])

            print(self.values)

            layer = self.values.get('layer_num', '?')
            speed = self.values.get('spd_lvl', 2)
            speed_map = {1: 'Silent', 2: 'Standard', 3: 'Sport', 4: 'Ludacris'}

            min_remain = self.values['mc_remaining_time']
            # Time 15 minutes in the future
            future_time = now + timedelta(minutes=min_remain)
            future_time_str = future_time.strftime("%Y-%m-%d %H:%M")

            # active_ams = self.values['ams']['tray_now']

            print(f"Layer: {layer} ({self.values['mc_percent']} %)\n"
                  f"Nozzle Temp: {self.values['nozzle_temper']} / \
                    {self.values['nozzle_target_temper']}\n"
                  f"Bed Temp: {self.values['bed_temper']} / \
                    {self.values['bed_target_temper']}\n"
                  f"Finish ETA: {future_time_str}\n"
                  f"Speed: {speed_map[speed]}")

            # with telem_text_path.open("w") as fp:
            #     fp.write(f"Layer: {layer} ({self.values['mc_percent']} %)\n"
            #             f"Nozzle Temp: {self.values['nozzle_temper']}/
            # {self.values['nozzle_target_temper']}\n"
            #             f"Bed Temp: {self.values['bed_temper']}/
            # {self.values['bed_target_temper']}\n"
            #             f"Finish ETA: {future_time_str}\n"
            #             f"Speed: {speed_map[speed]}")

            # with ams_text_path.open("w") as fp:
            #     for tray in self.values['ams']['ams'][0]['tray']:
            #         tray_remain = ''
            #         color_name = self._rgb_to_color_name(tray['cols'][0])
            #         if active_ams == tray['id']:
            #             active = " - In Use"
            #         else:
            #             active = ""
            #         if tray['remain'] != -1:
            #             tray_remain = f"({tray['remain']}% remain)"
            #         if tray['tray_sub_brands'] == '':
            #             tray_type = tray['tray_type']
            #         else:
            #             tray_type = tray['tray_sub_brands']
            #         fp.write(f"Tray {tray['id']}:
            # {tray_type} {color_name} {tray_remain}  {active}\n")

            #     if active_ams == "254":
            #         active = " - In Use"
            #     else:
            #         active = ""

            #     color_name = self._rgb_to_color_name(
            # self.values['vt_tray']['cols'][0])

            #     fp.write(f"Ext. : {self.values['vt_tray']['tray_type']}
            # {color_name} {active}")

        # Sometimes empty or diff doc structure returned
        # Swallow exception here and it'll just get retried next iteration
        except KeyError:
            print("Logging error json")
            # with telem_json_err_path.open("w") as fp:
            #     fp.write(json.dumps(doc))

        return None

    def publish(self, msg) -> None:
        """
        publish Publish a message to the Bambulabs 3D printer

        Parameters
        ----------
        msg : JSON
            JSON message to send to the Bambulabs 3D printer

        Returns
        -------
        None
        """
        self.client.publish(f"device/{self.serial}/request", json.dumps(msg))
        return None

    def loop_forever(self) -> None:
        """
        loop_forever Loop forever and process network traffic,
        dispatches callbacks and handles reconnecting.

        Returns
        -------
        None
        """
        self.client.loop_forever()
        return None


# client = mqtt.Client()
# client.check_hostname = False

# # set username and password
# # Username isn't something you can change, so hardcoded here
# client.username_pw_set('bblp', ACCESS_CODE)

# # These 2 lines are required to bypass self signed certificate errors,
# at least on my machine
# # these things can be finicky depending on your system setup
# client.tls_set(tls_version=ssl.PROTOCOL_TLS, cert_reqs=ssl.CERT_NONE)
# client.tls_insecure_set(True)

# client.on_connect = on_connect
# client.on_message = on_message
# client.connect(BAMBU_IP_ADDRESS, 8883, 60)

# client.publish(f"device/{SERIAL}/request", '{"pushing":
# {"command": "start", "sequence_id": 0}}')
# # Blocking call that processes network traffic, dispatches callbacks and
# # handles reconnecting.
# # Other loop*() functions are available that give a threaded interface and a
# # manual interface.
# client.loop_forever()
