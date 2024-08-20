import threading

import serial


class Controller:
    _left_translation_bound = -0.300  # -0.3m
    _right_translation_bound = 0.300  # 0.3m

    _left_rotation_bound = -180  # -180 degree
    _right_rotation_bound = 180  # 180 degree

    _translation_factor = 100_000  # 100_000 steps is 1m
    _rotation_factor = 800 / 360  # 800 steps is 360 degree

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        translation_step_size: float = 0.001,  # 5mm
        rotation_step_size: int = 15,  # 15 degree
    ):
        self._translation_step_size = translation_step_size
        self._rotation_step_size = rotation_step_size

        self._port = port
        self._serial = serial.Serial(self._port, baudrate=115200)
        self._is_running = False
        self._done = threading.Event()

        # Start a thread to listen to the Arduino
        self._listener_thread = threading.Thread(target=self._listen_to_arduino)
        self._listener_thread.daemon = True
        self._listener_thread.start()

        self._current_translation_position = 0

    def __del__(self):
        self.move(translation=0, rotation=0, relative=False)
        self._serial.close()

    @property
    def is_running(self):
        return int(self._serial.read(1)) == 0x81

    def _send_serial_data(
        self, translation_data: float, rotation_data: float, relative: bool = True
    ):
        # flip as the motor is inverted
        translation_data = -translation_data
        rotation_data = -rotation_data

        translation_stepper = int(translation_data * self._translation_factor)
        rotation_stepper = int(rotation_data * self._rotation_factor)

        data = bytearray(11)
        data[0] = 0x81  # set to 0x81 if enable, 0x80 if disable
        data[1] = 0x88  # signals that the data is ready to be read
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

    def _in_bound(self, position):
        return self._left_translation_bound <= position <= self._right_translation_bound

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
        translation = translation * self._translation_step_size
        rotation = rotation * self._rotation_step_size

        new_position = self._current_translation_position + translation

        in_bound = self._in_bound(new_position)
        if not in_bound:
            translation = 0

        # if the movement is too small then don't move
        if (abs(translation) < 0.0001) and (abs(rotation) < 1):
            return

        self._send_serial_data(
            translation_data=translation,
            rotation_data=rotation,
            relative=True,
        )

        self._current_translation_position = translation

    def _unnormalize(self, value: float, left_bound: float, right_bound: float):
        """
        .. math::
            x_{\text{unnormalized}} = \frac{(x_{\text{normalized}} + 1)}{2} \times (\text{max} - \text{min}) + \text{min}
        """
        return float(
            left_bound + (value - (-1.0)) * (right_bound - left_bound) / (1.0 - (-1.0))
        )

    def _move_to_global_position(self, translation: float, rotation: float):
        self._check_type_range(translation, rotation)

        translation_data = self._unnormalize(
            translation, self._left_translation_bound, self._right_translation_bound
        )
        rotation_data = self._unnormalize(
            rotation, self._left_rotation_bound, self._right_rotation_bound
        )

        self._send_serial_data(
            translation_data=translation_data,
            rotation_data=rotation_data,
            relative=False,
        )
        self._current_translation_position = translation_data

    def move(self, translation: float, rotation: float, relative=True):
        self._check_type_range(translation, rotation)
        if relative:
            self._move_to_relative_position(translation=translation, rotation=rotation)
        else:
            self._move_to_global_position(translation=translation, rotation=rotation)

        self._is_running = True
        self._done.clear()
        self._done.wait()  # Wait until the "done" signal is received
        self._is_running = False

    def get_info(self):
        return dict(
            current_translation_position=self._current_translation_position,
        )

    def _listen_to_arduino(self):
        while True:
            try:
                line = self._serial.readline().decode("utf-8", errors="ignore").strip()
                if line == "done":
                    self._done.set()
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                break
