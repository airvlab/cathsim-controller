# control the motor randomRun run or run To
from control import control

control = control("/dev/ttyUSB0")
for i in range(2):
    control.randomRun()

# control.run(0.5, 0)
