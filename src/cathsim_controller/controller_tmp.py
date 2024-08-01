from time import sleep

import serial


class Controller:
    _right_bound = 0.300
    _left_bound = -0.300
    # 1000mm, and one rotation is 100_000 steps
    # 360rotation is 800 steps
    _translation_step = 0.00001
    _rotation_step=0.45 #degree

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        translation_scale_factor: float = 0.005,  # 5 mm; 800 step one rotation -8mm
        rotation_scale_factor: float = 200,  # 90 degree; 800 step 360 degree
    ):
        self.translation_scale_factor = translation_scale_factor
        self.rotation_scale_factor = rotation_scale_factor
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
        translation_stepper = int(translation_data/self._translation_step)
        rotation_stepper = int(rotation_data)
        print(type(translation_stepper),type(rotation_stepper))
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

        self._serial.flush()
        self._serial.write(data)
        self._serial.flush()
        # self._listen_serial()

    def _listen_serial(self,):
        finished = False
        while not finished:
            finished=self._serial.read()
            finished=bool(finished)
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
            self._current_position,
            self._right_bound,
            self._left_bound ,
        )

    def _move_to_relative_position(self, translation: float, rotation: float):
        translation_motor = translation * float(self.translation_scale_factor)
        rotation_motor = rotation * float(self.rotation_scale_factor)
        expectPosition = self._current_position + translation_motor
        self._check_bound(check_position=expectPosition)
        self._send_serial_data(
            translation_data=translation_motor,
            rotation_data=rotation_motor,
            relative=True,
        )

    def _move_to_global_position(self, translation: float, rotation: float):
        translation_motor_scale_factor = 30000  # total 600 mm; 800 step one rotation -8mm
        rotation_motor_scale_factor = 800  # 360 degree;

        translation_motor = int(translation * float(translation_motor_scale_factor))
        rotation_motor = int(rotation * float(rotation_motor_scale_factor))
        self._send_serial_data(
            translation_data=translation_motor,
            rotation_data=rotation_motor,
            relative=True,
        )

    def move(self, translation: float, rotation: float, relative=True):
        self._check_type_range(translation, rotation)
        translation = -1 * translation
        if relative:
            self._move_to_relative_position(translation=translation, rotation=rotation)
        else:
            self._move_to_global_position(
                translation=translation, rotation=rotation)
