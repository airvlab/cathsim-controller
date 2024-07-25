# control each step have one image
import random
from motor import Motors


seed = 42

motorPort = "/dev/ttyUSB0"
my_motor = Motors(motorPort)
random.seed(seed)

linear, rotate = random.uniform(-1, 1), random.uniform(-1, 1)
my_motor.move(True, linear, rotate)
print(linear, rotate)

