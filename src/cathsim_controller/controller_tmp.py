import serial
from time import sleep

class Controller:
    _right_bound = 0.300  # 0.3m
    _left_bound = -0.300  # -0.3m
    # 1000mm, and one rotation is 100_000 steps
    # 360rotation is 800 steps
    _translation_factor = 100_000  # 100_000 steps is 1m
    _rotation_factor = 800 / 360  # 800 steps is 360 degree

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        translation_scale_factor: float = 0.005,  # 5 mm; 800 step one rotation -8mm
        rotation_scale_factor: float = 90,  # 90 degree; 800 step 360 degree
    ):
        self._translation_relative_scale_factor = -translation_scale_factor
        self._rotation_relative_scale_factor = rotation_scale_factor

        self._port = port
        self._serial = serial.Serial(self._port, baudrate=115200)
        self._current_position = 0

    def __del__(self):
        self._move_to_global_position(0, 0)
        self._serial.close()

    @property
    def is_running(self):
        return int(self._serial.read(1)) == 0x81

    def _send_serial_data(
        self, translation_data: float, rotation_data: int, relative: bool = True
    ):
        translation_stepper = int(translation_data * self._translation_factor)
        rotation_stepper = int(rotation_data * self._rotation_factor)

        # print(type(translation_stepper),type(rotation_stepper))
        data = bytearray(11)
        data[0] = 0x81  # set to 0x81 if enable, 0x80 if disable
        data[1] = 0x88  # setting this here as per the original C++ code
        if relative:
            data[10] = 0x80
        else:
            data[10] = 0x81

        data[2] = (translation_stepper & 0xFF000000) >> 24
        data[3] = (translation_stepper & 0x00FF0000) >> 16
        data[4] = (translation_stepper & 0x0000FF00) >> 8
        data[5] = translation_stepper & 0x000000FF

        data[6] = (rotation_stepper & 0xFF000000) >> 24
        data[7] = (rotation_stepper & 0x00FF0000) >> 16
        data[8] = (rotation_stepper & 0x0000FF00) >> 8
        data[9] = rotation_stepper & 0x000000FF

        self._serial.write(data)
        self._serial.flush()
        self._listen_serial()

    def _listen_serial(
        self,
    ):
        sleep(1)
        # finished =False
        print(self._serial.name)
        # while not finished:
            # print(f"Waiting for the response. Serial is {self._serial.in_waiting}, which is not ready", end='\r')
        # while self._serial.in_waiting():  
        #     finished = self._serial.read()
        #     self._serial.reset_input_buffer()
        #     finished = bool(finished)
        #     print(finished)
        
    def _check_bound(self, check_position):
        assert (
            self._left_bound <= check_position <= self._right_bound
        ), "The move out of range, and be cancelled"
        return True

    def _check_type_range(self, translation, rotation):
        # do the checks:type and range check
        assert isinstance(
            translation, (float, int)
        ), f"Got translation {type(translation)}, expected float or int"
        assert isinstance(
            rotation, (float, int)
        ), f"Got rotation {type(rotation)}, expected float or int"
        assert (
            -1 <= translation <= 1
        ), f"Got translation {translation}, expected in range (-1 1)"
        assert (
            -1 <= rotation <= 1
        ), f"Got rotation {rotation}, expected in range (-1, 1)"
        return True

    def _move_to_relative_position(self, translation: float, rotation: float):
        translation_data = translation * self._translation_relative_scale_factor
        rotation_data = rotation * self._rotation_relative_scale_factor

        if (
            abs(translation_data) < 0.0001 and abs(rotation_data) < 1
        ):  # the translation is smaller than 0.0001m and the rotation is smaller than 1 degree
            return

        expectPosition = self._current_position + translation_data
        self._check_bound(check_position=expectPosition)

        self._send_serial_data(
            translation_data=translation_data,
            rotation_data=rotation_data,
            relative=True,
        )
        self._current_position = expectPosition

    def _translation_global_scale(self, translation: float):
        return float(
            self._left_bound
            + (translation-(-1.0)) * (self._right_bound - self._left_bound) / (1.0 - (-1.0))
        )  # meters

    def _rotation_global_scale(self, rotation: float):
        return float(-180 + (rotation-(-1.0)) * 360 / (1.0 - (-1.0)))  # degree

    def _move_to_global_position(self, translation: float, rotation: float):
        # trans the translation -1 tp 1 between leftbound and right bound
        # trans the translation -1 tp 1 between -180 degree and 180 degree

        translation_data = self._translation_global_scale(translation=translation)
        rotation_data = self._rotation_global_scale(rotation=rotation)

        self._send_serial_data(
            translation_data=translation_data,
            rotation_data=rotation_data,
            relative=False,
        )
        self._current_position = translation_data

    def move(self, translation: float, rotation: float, relative=True):
        self._check_type_range(translation, rotation)
        if relative:
            self._move_to_relative_position(translation=translation, rotation=rotation)
        else:
            self._move_to_global_position(translation=translation, rotation=rotation)

    def get_info(self):
        return dict(
            current_position=self._current_position,
            right_bound=self._right_bound,
            left_bound=self._left_bound,
        )
