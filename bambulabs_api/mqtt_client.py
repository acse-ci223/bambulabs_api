import json
import logging
import ssl
from typing import Any

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from .filament_info import Filament
from .states_info import GcodeState, PrintStatus


class PrinterMQTTClient:
    """
    Printer class for handling MQTT communication with the printer
    """

    def __init__(self, hostname: str, access: str, printer_serial: str,
                 username: str = "bblp", port: int = 8883, timeout: int = 60):
        self._hostname = hostname
        self._access = access
        self._username = username
        self._printer_serial = printer_serial

        self._port = port
        self._timeout = timeout

        self._client: mqtt.Client = mqtt.Client(CallbackAPIVersion.VERSION2)
        self._client.username_pw_set(username, access)
        self._client.tls_set(tls_version=ssl.PROTOCOL_TLS,
                             cert_reqs=ssl.CERT_NONE)
        self._client.tls_insecure_set(True)

        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

        self.command_topic = f"device/{printer_serial}/request"
        logging.info(f"{self.command_topic}")   # noqa  # pylint: disable=logging-fstring-interpolation
        self._data = {}

    def _on_message(self, client, userdata, msg) -> None:  # pylint: disable=unused-argument  # noqa
        # Current date and time
        doc = json.loads(msg.payload)

        if "print" in doc:
            self._data |= doc["print"]
            logging.debug(self._data)

    def _on_connect(self, client: mqtt.Client, serial, userdata, flags, rc) -> None:  # pylint: disable=unused-argument  # noqa
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
        client.subscribe(f"device/{self._printer_serial}/report")

    def connect(self) -> None:
        """
        Connects to the MQTT server asynchronously
        """
        self._client.connect_async(self._hostname, self._port, self._timeout)

    def start(self):
        """
        Starts the MQTT client
        """
        self._client.loop_start()

    def loop_forever(self):
        """
        Loop client forever (synchonous, blocking call)
        """
        self._client.loop_forever()

    def stop(self):
        """
        Stops the MQTT client
        """
        self._client.loop_stop()

    def __get(self, key: str, default: Any = None) -> Any:
        self.manual_update()
        return self._data.get(key, default)

    def manual_update(self) -> bool:
        return self.__publish_command({"pushing": {"command": "pushall"}})

    def get_last_print_percentage(self) -> int | str | None:
        """
        Get the last print percentage

        Returns:
            int | str | None: The last print percentage
        """
        return self.__get("mc_percent", None)

    def get_remaining_time(self) -> int | str | None:
        """
        Get the remaining time for the print

        Returns:
            int | str | None: The remaining time for the print
        """
        return self.__get("mc_remaining_time", None)

    def get_printer_state(self) -> GcodeState:
        """
        Get the printer state

        Returns:
            PrintStatus: printer state
        """
        return GcodeState(self.__get("gcode_state", -1))

    def get_file_name(self) -> str:
        """
        Get the file name of the current/last print

        Returns:
            str: file name
        """
        return self.__get("gcode_file", "")

    def get_print_speed(self) -> int:
        """
        Get the print speed

        Returns:
            int: print speed
        """
        return int(self.__get("spd_mag", 100))

    def __publish_command(self, payload: dict[Any, Any]) -> bool:
        """
        Generate a command payload and publish it to the MQTT server

        Args:
            payload (dict[Any, Any]): command to send to the printer
        """
        if self._client.is_connected() is False:
            logging.error("Not connected to the MQTT server")
            return False

        command = self._client.publish(self.command_topic, json.dumps(payload))
        logging.info(f"Published command: {payload}")   # noqa  # pylint: disable=logging-fstring-interpolation
        command.wait_for_publish()
        return command.is_published()

    def turn_light_off(self) -> bool:
        """
        Turn off the printer light
        """
        return self.__publish_command({"system": {"led_mode": "off"}})

    def turn_light_on(self) -> bool:
        """
        Turn on the printer light
        """
        return self.__publish_command({"system": {"led_mode": "on"}})

    def get_light_state(self) -> str:
        """
        Get the printer light state

        Returns:
            str: led_mode
        """
        light_report: list[dict[str, str]] = self.__get(
            "lights_report", [])

        if not light_report:
            return "unknown"

        return light_report[0].get("mode", "unknown")

    def start_print_3mf(self, filename: str, plate_number: int) -> bool:
        """
        Start the print

        Returns:
            str: print_status
        """
        return self.__publish_command(
            {
                "print":
                {
                    "command": "project_file",
                    "param": f"Metadata/plate_{plate_number}.gcode",
                    "subtask_name": filename,
                    "bed_leveling": True,
                    "flow_calibration": True,
                    "vibration_calibration": True,
                    "url": f"ftp://{filename}",
                    "layer_inspect": False,
                    "use_ams": False,
                }
            })

    def get_current_state(self) -> str:
        """
        Get the current printer state from stg_cur

        Returns:
            str: current_state
        """
        return PrintStatus(self.__get("stg_cur", -1)).name

    def stop_print(self) -> bool:
        """
        Stop the print

        Returns:
            str: print_status
        """
        return self.__publish_command({"print": {"command": "stop"}})

    def pause_print(self) -> bool:
        """
        Pause the print

        Returns:
            str: print_status
        """
        if self.get_printer_state() == GcodeState.PAUSED:
            return True
        return self.__publish_command({"print": {"command": "pause"}})

    def resume_print(self) -> bool:
        """
        Resume the print

        Returns:
            str: print_status
        """
        if self.get_printer_state() == GcodeState.RUNNING:
            return True
        return self.__publish_command({"print": {"command": "resume"}})

    def __send_gcode_line(self, gcode_command: str) -> bool:
        """
        Send a G-code line command to the printer

        Args:
            gcode_command (str): G-code command to send to the printer
        """
        return self.__publish_command({"print": {"command": "gcode_line",
                                                 "param": f"{gcode_command}"}})

    def set_bed_temperature(self, temperature: int) -> bool:
        """
        Set the bed temperature

        Args:
            temperature (int): The temperature to set the bed to

        Returns:
            bool: success of setting the bed temperature
        """
        return self.__send_gcode_line(f"M140 S{temperature}\n")

    def set_bed_height(self, height: int) -> bool:
        """
        Set the absolute height of the bed (Z-axis). 
        0 is the bed at the nozzle tip and 256 is the bed at the bottom of the printer.

        Args:
            height (int): height to set the bed to 

        Returns:
            bool: success of the bed height setting
        """  # noqa
        return self.__send_gcode_line(f"G90\nG0 Z{height}\n")

    def auto_home(self) -> bool:
        """
        Auto home the printer

        Returns:
            bool: success of the auto home command
        """
        return self.__send_gcode_line("G28\n")

    def set_print_speed_lvl(self, speed_lvl: int = 1) -> bool:
        """
        Set the print speed

        Args:
            speed_lvl (int, optional): Set the speed level of printer. Defaults to 1.

        Returns:
            bool: success of setting the print speed
        """  # noqa
        return self.__publish_command(
            {"print": {"command": "print_speed", "param": f"{speed_lvl}"}}
        )

    def set_nozzle_temperature(self, temperature: int) -> bool:
        """
        Set the nozzle temperature

        Args:
            temperature (int): temperature to set the nozzle to

        Returns:
            bool: success of setting the nozzle temperature
        """
        return self.__send_gcode_line(f"M104 S{temperature}\n")

    def set_printer_filament(self, filament_material: Filament, colour: str) -> bool:  # noqa
        """
        Set the printer filament manually fed into the printer

        Args:
            filament_material (Filament): filament material to set
            colour (str): colour of the filament

        Returns:
            bool: success of setting the printer filament
        """
        assert len(colour) == 6, "Colour must be a 6 character hex string"

        return self.__publish_command(
            {
                "print": {
                    "command": "ams_filament_setting",
                    "ams_id": 255,
                    "tray_id": 254,
                    "tray_info_idx": filament_material.tray_info_idx,
                    "tray_color": f"{colour.upper()}FF",
                    "nozzle_temp_min": filament_material.nozzle_temp_min,
                    "nozzle_temp_max": filament_material.nozzle_temp_max,
                    "tray_type": filament_material.tray_type
                }
            }
        )

    def load_filament_spool(self) -> bool:
        """
        Load the filament into the printer

        Returns:
            bool: success of loading the filament
        """
        return self.__publish_command(
            {
                "print": {
                    "command": "ams_change_filament",
                    "target": 255,
                    "curr_temp": 215,
                    "tar_temp": 215,
                }
            }
        )

    def unload_filament_spool(self) -> bool:
        """
        Unload the filament from the printer

        Returns:
            bool: success of unloading the filament
        """
        return self.__publish_command(
            {
                "print": {
                    "command": "ams_change_filament",
                    "target": 254,
                    "curr_temp": 215,
                    "tar_temp": 215,
                }
            }
        )

    def resume_filament_action(self) -> bool:
        """
        Resume the current filament action

        Returns:
            bool: success of resuming the filament action
        """
        return self.__publish_command(
            {
                "print": {
                    "command": "ams_control",
                    "param": "resume",
                }
            }
        )

    def calibration(
            self,
            bed_levelling: bool = True,
            motor_noise_cancellation: bool = True,
            vibration_compensation: bool = True) -> bool:
        """
        Start the full calibration process

        Returns:
            bool: success of starting the full calibration process
        """
        bitmask = 0

        if bed_levelling:
            bitmask |= 1 << 1
        if vibration_compensation:
            bitmask |= 1 << 2
        if motor_noise_cancellation:
            bitmask |= 1 << 3

        return self.__publish_command(
            {
                "print": {
                    "command": "calibration",
                    "option": bitmask
                }
            }
        )
