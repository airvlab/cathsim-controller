# control each step have one image
import random

from motor import Motors

seed = 42

motorPort = "/dev/ttyUSB0"
motor = Motors(motorPort)
random.seed(seed)

linear, rotate = random.uniform(-10, 10), random.uniform(-1, 1)
motor.move(1, linear, rotate)
print(linear, rotate)

