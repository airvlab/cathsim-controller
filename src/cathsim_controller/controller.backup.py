from time import sleep

import serial


class Controller:
    _right_bound = 30000  # the right bound of step position is 0
    _left_bound = -30000  # the left bound of step position is -6000

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        translation_scale_factor: float = 500,  # 5 mm; 800 step one rotation -8mm
        rotation_scale_factor: float = 200,  # 90 degree; 800 step 360 degree
    ):
        self.translation_scale_factor = translation_scale_factor
        self.rotation_scale_factor = rotation_scale_factor
        self._port = port
        self._serial = serial.Serial(self._port, baudrate=115200)
        self._current_position = 0

    def __del__(self):
        self._move_to_global_position(0, 0)
        sleep(1)
        self._serial.close()

    def send(self, enable, motor1, motor2, motor3, motor4, relative):
        data = bytearray(19)
        if enable:
            data[0] = 0x81
        else:
            data[0] = 0x80
        data[1] = 0x88  # setting this here as per the original C++ code
        if relative:
            data[18] = 0x80
        else:
            data[18] = 0x81
        data[2] = (motor1 & 0xFF000000) >> 24
        data[3] = (motor1 & 0x00FF0000) >> 16
        data[4] = (motor1 & 0x0000FF00) >> 8
        data[5] = motor1 & 0x000000FF
        data[6] = (motor2 & 0xFF000000) >> 24
        data[7] = (motor2 & 0x00FF0000) >> 16
        data[8] = (motor2 & 0x0000FF00) >> 8
        data[9] = motor2 & 0x000000FF
        data[10] = (motor3 & 0xFF000000) >> 24
        data[11] = (motor3 & 0x00FF0000) >> 16
        data[12] = (motor3 & 0x0000FF00) >> 8
        data[13] = motor3 & 0x000000FF
        data[14] = (motor4 & 0xFF000000) >> 24
        data[15] = (motor4 & 0x00FF0000) >> 16
        data[16] = (motor4 & 0x0000FF00) >> 8
        data[17] = motor4 & 0x000000FF
        self._serial.flush()
        self._serial.write(data)

        self._serial.flush()
        finished = False
        while not finished:
            finished = self._serial.read()
            print(finished)

    def _check_bound(self, check_position):
        assert (
            self._left_bound <= check_position <= self._right_bound
        ), "The move out of range, and be cancelled"
        return True

    def _check_type_range(self, translation, rotation):
        # do the checks:type and range check
        assert isinstance(
            translation, float
        ), f"Got translation {type(translation)}, expected float"
        assert isinstance(
            rotation, float
        ), f"Got rotation {type(rotation)}, expected float"
        assert (
            -1 <= translation <= 1
        ), f"Got translation {translation}, expected in range (-1 1)"
        assert (
            -1 <= rotation <= 1
        ), f"Got rotation {rotation}, expected in range (-1, 1)"
        return True

    def get_info(self):
        return (
            self._current_position / 100.0,
            self._right_bound / 100.0,
            self._left_bound / 100.0,
        )

    def _move_to_relative_position(self, translation: float, rotation: float):
        # motor3B, motor4B should be in range(-1,1)
        translation_motor = int(translation * float(self.translation_scale_factor))
        rotation_motor = int(rotation * float(self.rotation_scale_factor))
        expectPosition = self._current_position + translation_motor
        self._check_bound(check_position=expectPosition)
        self.send(
            enable=True,
            motor1=0,
            motor2=0,
            motor3=translation_motor,
            motor4=rotation_motor,
            relative=True,
        )

    def _move_to_global_position(self, translation: float, rotation: float):
        # motor3B, motor4B should be in range(0,1)
        # change range from(-1,1) to range (0,1)
        # translation = (translation + 1.0) / 2.0
        # rotation = (rotation + 1.0) / 2.0

        motor3_scale_factor = 30000  # total 600 mm; 800 step one rotation -8mm
        motor4_scale_factor = 800  # 360 degree;

        motor3 = int(translation * float(motor3_scale_factor))
        motor4 = int(rotation * float(motor4_scale_factor))
        self.send(
            enable=True,
            motor1=0,
            motor2=0,
            motor3=motor3,
            motor4=motor4,
            relative=False,
        )

    def move(self, translation: float, rotation: float, relative=True):
        self._check_type_range(translation, rotation)
        translation = -1 * translation
        if relative:
            self._move_to_relative_position(translation=translation, rotation=rotation)
        else:
            self._move_to_global_position(translation=translation, rotation=rotation)
