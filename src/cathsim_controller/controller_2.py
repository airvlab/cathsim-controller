import serial


class Controller:
    _right_bound = 0.300
    _left_bound = -0.300
    # 1000mm, and one rotation is 100_000 steps
    # 360rotation is 800 steps
    _translation_step = 0.00001

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        translation_scale_factor: float = 0.1,
        rotation_scale_factor: float = 0.1,
    ):
        self._port = port
        self._serial = serial.Serial(self._port, baudrate=115200)
        self._current_position = 0
        self._is_running = False

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
        motor3_scale_factor = 500  # 5 mm; 800 step one rotation -8mm
        motor4_scale_factor = 200  # 90 degree; 800 step 360 degree

        motor3 = int(translation * float(motor3_scale_factor))
        motor4 = int(rotation * float(motor4_scale_factor))
        self._send_serial_data(
            motor1=0,
            motor2=0,
            translation_data=motor3,
            rotation_data=motor4,
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
        self._send_serial_data(
            enable=True,
            translation_data=motor3,
            rotation_data=motor4,
            relative=False,
        )

    def move(self, translation: float, rotation: float, relative=True):
        if relative:
            self._check_type_range(translation, rotation)
            self._move_to_relative_position(translation=translation, rotation=rotation)
        else:
            self._move_to_global_position(translation=translation, rotation=rotation)


if __name__ == "__main__":
    controller = Controller()
    controller.move(0.1, 0.1)
