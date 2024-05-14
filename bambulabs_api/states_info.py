from enum import Enum

__all__ = ["PrintStatus", "GcodeState"]


class PrintStatus(Enum):
    """
    Enum class for the printer status

    The printer status is a value that indicates the current state of the printer.

    Attributes
    ----------

    PRINTING: The printer is currently printing.
    AUTO_BED_LEVELING: The printer is performing an automatic bed leveling.
    HEATBED_PREHEATING: The printer is preheating the heatbed.
    SWEEPING_XY_MECH_MODE: The printer is performing a sweeping XY mechanical mode.
    CHANGING_FILAMENT: The printer is changing the filament.
    M400_PAUSE: The printer is paused.
    PAUSED_FILAMENT_RUNOUT: The printer is paused due to filament runout.
    HEATING_HOTEND: The printer is heating the hotend.
    CALIBRATING_EXTRUSION: The printer is calibrating the extrusion.
    SCANNING_BED_SURFACE: The printer is scanning the bed surface.
    INSPECTING_FIRST_LAYER: The printer is inspecting the first layer.
    IDENTIFYING_BUILD_PLATE_TYPE: The printer is identifying the build plate type.
    CALIBRATING_MICRO_LIDAR: The printer is calibrating the micro LiDAR.
    HOMING_TOOLHEAD: The printer is homing the toolhead.
    CLEANING_NOZZLE_TIP: The printer is cleaning the nozzle tip.
    CHECKING_EXTRUDER_TEMPERATURE: The printer is checking the extruder temperature.
    PAUSED_USER: The printer is paused by the user.
    PAUSED_FRONT_COVER_FALLING: The printer is paused due to the front cover falling.
    CALIBRATING_LIDAR: The printer is calibrating the LiDAR.
    CALIBRATING_EXTRUSION_FLOW: The printer is calibrating the extrusion flow.
    PAUSED_NOZZLE_TEMPERATURE_MALFUNCTION: The printer is paused due to a nozzle temperature malfunction.
    PAUSED_HEAT_BED_TEMPERATURE_MALFUNCTION: The printer is paused due to a heat bed temperature malfunction.
    FILAMENT_UNLOADING: The printer is unloading the filament.
    PAUSED_SKIPPED_STEP: The printer is paused due to a skipped step.
    FILAMENT_LOADING: The printer is loading the filament.
    CALIBRATING_MOTOR_NOISE: The printer is calibrating the motor noise.
    PAUSED_AMS_LOST: The printer is paused due to an AMS lost.
    PAUSED_LOW_FAN_SPEED_HEAT_BREAK: The printer is paused due to a low fan speed heat break.
    PAUSED_CHAMBER_TEMPERATURE_CONTROL_ERROR: The printer is paused due to a chamber temperature control error.
    COOLING_CHAMBER: The printer is cooling the chamber.
    PAUSED_USER_GCODE: The printer is paused by the user GCODE.
    MOTOR_NOISE_SHOWOFF: The printer is showing off the motor noise.
    PAUSED_NOZZLE_FILAMENT_COVERED_DETECTED: The printer is paused due to a nozzle filament covered detected.
    PAUSED_CUTTER_ERROR: The printer is paused due to a cutter error.
    PAUSED_FIRST_LAYER_ERROR: The printer is paused due to a first layer error.
    PAUSED_NOZZLE_CLOG: The printer is paused due to a nozzle clog.
    UNKNOWN: The printer status is unknown.
    IDLE: The printer is idle.
    """  # noqa
    PRINTING = 0
    AUTO_BED_LEVELING = 1
    HEATBED_PREHEATING = 2
    SWEEPING_XY_MECH_MODE = 3
    CHANGING_FILAMENT = 4
    M400_PAUSE = 5
    PAUSED_FILAMENT_RUNOUT = 6
    HEATING_HOTEND = 7
    CALIBRATING_EXTRUSION = 8
    SCANNING_BED_SURFACE = 9
    INSPECTING_FIRST_LAYER = 10
    IDENTIFYING_BUILD_PLATE_TYPE = 11
    CALIBRATING_MICRO_LIDAR = 12  # Check this
    HOMING_TOOLHEAD = 13
    CLEANING_NOZZLE_TIP = 14
    CHECKING_EXTRUDER_TEMPERATURE = 15
    PAUSED_USER = 16
    PAUSED_FRONT_COVER_FALLING = 17
    CALIBRATING_LIDAR = 18  # Check this
    CALIBRATING_EXTRUSION_FLOW = 19
    PAUSED_NOZZLE_TEMPERATURE_MALFUNCTION = 20
    PAUSED_HEAT_BED_TEMPERATURE_MALFUNCTION = 21
    FILAMENT_UNLOADING = 22
    PAUSED_SKIPPED_STEP = 23
    FILAMENT_LOADING = 24
    CALIBRATING_MOTOR_NOISE = 25
    PAUSED_AMS_LOST = 26
    PAUSED_LOW_FAN_SPEED_HEAT_BREAK = 27
    PAUSED_CHAMBER_TEMPERATURE_CONTROL_ERROR = 28
    COOLING_CHAMBER = 29
    PAUSED_USER_GCODE = 30
    MOTOR_NOISE_SHOWOFF = 31
    PAUSED_NOZZLE_FILAMENT_COVERED_DETECTED = 32
    PAUSED_CUTTER_ERROR = 33
    PAUSED_FIRST_LAYER_ERROR = 34
    PAUSED_NOZZLE_CLOG = 35
    UNKNOWN = None
    IDLE = 255

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class GcodeState(str, Enum):
    """
    Enum class for the Gcode State

    Gcode State that the printer can be in.

    Attributes
    ----------
    IDLE: The printer is idle.
    PREPARING: The printer is preparing (File upload).
    RUNNING: The printer is running.
    PAUSED: The printer is paused.
    FINISHED: The printer has finished.
    UNKNOWN: The printer state is unknown.
    FAILED: The printer has failed.
    """
    IDLE = "IDLE"
    PREPARE = "PREPARE"
    RUNNING = "RUNNING"
    PAUSE = "PAUSE"
    FINISH = "FINISH"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
