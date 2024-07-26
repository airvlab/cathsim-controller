from controller import Controller

my_controller=Controller("/dev/ttyUSB0")
my_controller.move( translation=0.025, rotation=0.9, relative=True)