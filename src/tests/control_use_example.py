# control the motor randomRun run or run To
from control import Controller

control = Controller("/dev/ttyUSB0")
for i in range(2):
    control.randomRun()

# control.run(0.5, 0)
