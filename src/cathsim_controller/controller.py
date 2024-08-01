import serial


class Controller:
    _right_bound = 0.3  # 0.3m
    _left_bound = -0.3  # -0.3m
    _translation_factor = 100_000  # 100_000 steps is 1m
    _rotation_factor = 800 / 360  # 800 steps is 360 degree

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        translation_step_size: float = 0.001,  # 1mm
        rotation_step_size: int = 15,  # 15 degree
    ):
        self._port = port
        self._serial = serial.Serial(self._port, baudrate=115200)
        self._current_position = 0
        self._is_running = False

        # set to negative as the motor is inverted
        self._translation_step_size = -translation_step_size
        self._rotation_step_size = rotation_step_size

    def __del__(self):
        self._move_to_global_position(0, 0)
        self._serial.close()

    @property
    def is_running(self):
        return int(self._serial.read(1)) == 0x81

    def _send_serial_data(
        self, translation_data: int, rotation_data: int, relative: bool = True
    ):
        translation_stepper = translation_data
        rotation_stepper = rotation_data

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

    def get_info(self):
        return dict(
            current_position=self._current_position,
        )

    def _move_to_relative_position(self, translation: float, rotation: float):
        translation = translation * self._translation_step_size
        translation_steps = int(translation * self._translation_factor)

        rotation = rotation * self._rotation_step_size
        rotation_steps = int(rotation * self._rotation_factor)

        self._send_serial_data(
            translation_data=translation_steps,
            rotation_data=rotation_steps,
            relative=True,
        )

        self._current_position += translation

    def _move_to_global_position(self, translation: float, rotation: float):
        translation_steps = int(translation * self._translation_factor)
        rotation_steps = int(rotation * self._rotation_factor)

        self._send_serial_data(
            translation_data=translation_steps,
            rotation_data=rotation_steps,
            relative=False,
        )

    def move(self, translation: float, rotation: float, relative=True):
        self._check_input_type(translation, rotation)
        if relative:
            self._check_relative_input(translation, rotation)
            self._move_to_relative_position(translation=translation, rotation=rotation)
        else:
            self._check_global_input(translation, rotation)
            self._move_to_global_position(translation=translation, rotation=rotation)

    def _check_input_type(self, translation, rotation):
        assert isinstance(
            translation, float
        ), f"Got translation {type(translation)}, expected float"
        assert isinstance(
            rotation, float
        ), f"Got rotation {type(rotation)}, expected float"
        return True

    def _check_relative_input(self, translation, rotation):
        assert (
            -1 <= translation <= 1
        ), f"Got translation {translation}, expected in range (-1 1)"
        assert (
            -1 <= rotation <= 1
        ), f"Got rotation {rotation}, expected in range (-1, 1)"
        return True

    def _check_global_input(self, translation, rotation):
        assert (
            self._left_bound <= translation <= self._right_bound
        ), f"Got translation {translation}, expected in range ({self._left_bound}, {self._right_bound})"
        return True
