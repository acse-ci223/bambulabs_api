"""
Client module for connecting to the Bambulabs 3D printer API
and getting all the printer data.
"""

from typing import BinaryIO

from bambulabs_api.states_info import PrintStatus
from .camera_client import PrinterCamera
from .ftp_client import PrinterFTPClient
from .mqtt_client import PrinterMQTTClient
from .filament_info import Filament, AMSFilamentSettings

__all__ = ['Printer']


class Printer:
    """
    Client Class for connecting to the Bambulabs 3D printer
    """
    def __init__(self, ip_address, access_code, serial):
        self.ip_address = ip_address
        self.access_code = access_code
        self.serial = serial

        self.__printerMQTTClient = PrinterMQTTClient(self.ip_address,
                                                     self.access_code,
                                                     self.serial)
        self.__printerCamera = PrinterCamera(self.ip_address,
                                             self.access_code)
        self.__printerFTPClient = PrinterFTPClient(self.ip_address,
                                                   self.access_code)

    def connect(self):
        """
        Connect to the printer
        """
        self.__printerMQTTClient.connect()
        self.__printerMQTTClient.start()
        self.__printerCamera.start()

    def disconnect(self):
        """
        Disconnect from the printer
        """
        self.__printerMQTTClient.stop()
        self.__printerCamera.stop()

    def get_time(self) -> (int | str | None):
        """
        Get the remaining time of the print job in seconds.

        Returns
        -------
        int
            Remaining time of the print job in seconds.
        str
            "Unknown" if the remaining time is unknown.
        None if the printer is not printing.
        """
        return self.__printerMQTTClient.get_remaining_time()

    def get_percentage(self) -> (int | str | None):
        """
        Get the percentage of the print job completed.

        Returns
        -------
        int
            Percentage of the print job completed.
        str
            "Unknown" if the percentage is unknown.
        None if the printer is not printing.
        """
        return self.__printerMQTTClient.get_last_print_percentage()

    def get_state(self) -> str:
        """
        Get the state of the printer.

        Returns
        -------
        str
            The state of the printer.
        """
        return self.__printerMQTTClient.get_printer_state().name

    def get_print_speed(self) -> int:
        """
        Get the print speed of the printer.

        Returns
        -------
        int
            The print speed of the printer.
        """
        return self.__printerMQTTClient.get_print_speed()

    def get_bed_temperature(self) -> float | None:
        """
        Get the bed temperature of the printer.
        NOT IMPLEMENTED YET

        Returns
        -------
        float
            The bed temperature of the printer.
        None if the printer is not printing.
        """
        return self.__printerMQTTClient.get_bed_temperature()

    def get_nozzle_temperature(self) -> float | None:
        """
        Get the nozzle temperature of the printer.
        NOT IMPLEMENTED YET

        Returns
        -------
        float
            The nozzle temperature of the printer.
        None if the printer is not printing.
        """
        return self.__printerMQTTClient.get_nozzle_temperature()

    def get_file_name(self) -> str:
        """
        Get the name of the file being printed.

        Returns
        -------
        str
            The name of the file being printed.
        """
        return self.__printerMQTTClient.get_file_name()

    def get_light_state(self) -> str:
        """
        Get the state of the printer light.

        Returns
        -------
        str
            The state of the printer light.
        """
        return self.__printerMQTTClient.get_light_state()

    def turn_light_on(self) -> bool:
        """
        Turn on the printer light.

        Returns
        -------
        bool
            True if the light is turned on successfully.
        """
        return self.__printerMQTTClient.turn_light_on()

    def turn_light_off(self) -> bool:
        """
        Turn off the printer light.

        Returns
        -------
        bool
            True if the light is turned off successfully.
        """
        return self.__printerMQTTClient.turn_light_off()

    def upload_file(self, file: BinaryIO, filename: str = "ftp_upload.gcode") -> str:  # noqa
        """
        Upload a file to the printer.

        Parameters
        ----------
        file : BinaryIO
            The file to be uploaded.
        filename : str, optional
            The name of the file, by default "ftp_upload.gcode".

        Returns
        -------
        str
            The path of the uploaded file.
        """
        try:
            if file and filename:
                return self.__printerFTPClient.upload_file(file, filename)
        except Exception as e:
            raise Exception(f"Exception occurred during file upload: {e}")  # noqa  # pylint: disable=raise-missing-from,broad-exception-raised
        finally:
            file.close()
        return "No file uploaded."

    def start_print(self, filename: str,
                    plate_number: int,
                    use_ams: bool = True,
                    ams_mapping: list[int] = [0],
                    skip_objects: list[int] = [],
                    ) -> bool:
        """
        Start printing a file.

        Parameters
        ----------
        filename : str
            The name of the file to be printed.
        plate_number : int
            The plate number of the file to be printed.
        use_ams : bool, optional
            Whether to use the AMS system, by default True.
        ams_mapping : list[int], optional
            The mapping of the filament trays to the plate numbers,
            by default [0].
        skip_objects (list[int], optional): List of gcode objects to skip.
            Defaults to [].

        Returns
        -------
        bool
            True if the file is printed successfully.
        """
        return self.__printerMQTTClient.start_print_3mf(filename,
                                                        plate_number,
                                                        use_ams,
                                                        ams_mapping,
                                                        skip_objects)

    def stop_print(self) -> bool:
        """
        Stop the printer from printing.

        Returns
        -------
        bool
            True if the printer is stopped successfully.
        """
        return self.__printerMQTTClient.stop_print()

    def pause_print(self) -> bool:
        """
        Pause the printer from printing.

        Returns
        -------
        bool
            True if the printer is paused successfully.
        """
        return self.__printerMQTTClient.pause_print()

    def resume_print(self) -> bool:
        """
        Resume the printer from printing.

        Returns
        -------
        bool
            True if the printer is resumed successfully.
        """
        return self.__printerMQTTClient.resume_print()

    def set_bed_temperature(self, temperature: int) -> bool:
        """
        Set the bed temperature of the printer.

        Parameters
        ----------
        temperature : int
            The temperature to be set.

        Returns
        -------
        bool
            True if the temperature is set successfully.
        """
        return self.__printerMQTTClient.set_bed_temperature(temperature)

    def home_printer(self) -> bool:
        """
        Home the printer.

        Returns
        -------
        bool
            True if the printer is homed successfully.
        """
        return self.__printerMQTTClient.auto_home()

    def move_z_axis(self, height: int) -> bool:
        """
        Move the Z-axis of the printer.

        Parameters
        ----------
        height : float
            The height for the bed.

        Returns
        -------
        bool
            True if the Z-axis is moved successfully.
        """
        return self.__printerMQTTClient.set_bed_height(height)

    def set_filament_printer(self, color: str, filament: str | AMSFilamentSettings) -> bool:  # noqa
        """
        Set the filament of the printer.

        Parameters
        ----------
        color : str
            The color of the filament.
        filament : str | AMSFilamentSettings
            The filament to be set.

        Returns
        -------
        bool
            True if the filament is set successfully.
        """
        assert len(color) == 6, "Color must be a 6 character hex code"
        if isinstance(filament, str) or isinstance(filament, AMSFilamentSettings):  # noqa
            filament = Filament(filament)
        else:
            raise ValueError(
                "Filament must be a string or AMSFilamentSettings object")
        return self.__printerMQTTClient.set_printer_filament(filament, color)

    def set_nozzle_temperature(self, temperature: int) -> bool:
        """
        Set the nozzle temperature of the printer.

        Parameters
        ----------
        temperature : int
            The temperature to be set.

        Returns
        -------
        bool
            True if the temperature is set successfully.
        """
        return self.__printerMQTTClient.set_nozzle_temperature(temperature)

    def set_print_speed(self, speed_lvl: int) -> bool:
        """
        Set the print speed of the printer.

        Parameters
        ----------
        speed_lvl : int
            The speed level to be set.
            0: Slowest
            1: Slow
            2: Fast
            3: Fastest

        Returns
        -------
        bool
            True if the speed level is set successfully.
        """
        assert 0 <= speed_lvl <= 3, "Speed level must be between 0 and 3"
        return self.__printerMQTTClient.set_print_speed_lvl(speed_lvl)

    def delete_file(self, file_path: str) -> str:
        """
        Delete a file from the printer.

        Parameters
        ----------
        file_path : str
            The path of the file to be deleted.

        Returns
        -------
        str
            The path of the deleted file.
        """
        return self.__printerFTPClient.delete_file(file_path)

    def calibrate_printer(self, bed_level: bool = True,
                          motor_noise_calibration: bool = True,
                          vibration_compensation: bool = True) -> bool:
        """
        Calibrate the printer.

        Parameters
        ----------
        bed_level : bool, optional
            Whether to calibrate the bed level, by default True.
        motor_noise_calibration : bool, optional
            Whether to calibrate the motor noise, by default True.
        vibration_compensation : bool, optional
            Whether to calibrate the vibration compensation, by default True.

        Returns
        -------
        bool
            True if the printer is calibrated successfully.
        """
        return self.__printerMQTTClient.calibration(bed_level,
                                                    motor_noise_calibration,
                                                    vibration_compensation)

    def load_filament_spool(self) -> bool:
        """
        Load the filament spool to the printer.

        Returns
        -------
        bool
            True if the filament spool is loaded successfully.
        """
        return self.__printerMQTTClient.load_filament_spool()

    def unload_filament_spool(self) -> bool:
        """
        Unload the filament spool from the printer.

        Returns
        -------
        bool
            True if the filament spool is unloaded successfully.
        """
        return self.__printerMQTTClient.unload_filament_spool()

    def retry_filament_action(self) -> bool:
        """
        Retry the filament action.

        Returns
        -------
        bool
            True if the filament action is retried successfully.
        """
        return self.__printerMQTTClient.resume_filament_action()

    def get_camera_frame(self) -> str:
        """
        Get the camera frame of the printer.

        Returns
        -------
        str
            Base64 encoded image of the camera frame.
        """
        return self.__printerCamera.get_frame()

    def get_current_state(self) -> PrintStatus:
        """
        Get the current state of the printer.

        Returns
        -------
        PrintStatus
            The current state of the printer.
        """
        return self.__printerMQTTClient.get_current_state()
