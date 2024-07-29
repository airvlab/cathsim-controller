from console import Console
from controller import RealEnv
import queue

action_queue=queue.Queue()

while not done:
            for events in event.get():
                if events.type == QUIT:
                    done = True  # Flag that we are done so we exit this loop.
                if events.type == JOYAXISMOTION:
                    (new_left_control,
                     new_right_control) = (self.joystick_obj[id].get_axis(i)
                                           for i in Axis_id)
                    (left_control, right_control) = (new_left_control,
                                                     new_right_control)
                    if abs(left_control - 0) > 1e-1 or abs(right_control -
                                                           0) > 1e-1:
                        print(left_control, right_control)
                    elif abs(left_control - new_left_control) < 1e-2 or abs(
                            right_control - new_right_control) < 1e-2:
                        pass
                if events.type == JOYBUTTONDOWN:
                    done = True

# set the function (will be controlled by the thread) that can store and deal with the data. In the meanwhile that it can be set the machine move when the condition satisfy the need
def operate_motor():
  # initial the env
  env = RealEnv(width=80, height=80)
  env.reset()
  cum_translation, cum_rotation=0,0


  while True:
    if 
    env.step()

# set the function that get the input from console 
def handle_input():
  # Initial console
  myconsole = Console()
  console_info = myconsole.get_info()
  print(
      f"You have {console_info.get(num) } consoles; {console_info.get(joystick_items)}"
  )
  input_user = input("which console are you gonna to use(default 0):")
  if not input_user.strip():
      id = 0
  try:
      id = int(input_user)
  except ValueError:
      print("Not a valid integer value, will be set as default 0")
      id = 0
  if id < 0 or id >= console_info.get(num):
      print("Value out of ranges, will be set as default 0")
      id = 0
          done = False
        Axis_id = [0, 3]
        if "Sony" in self.joystick_obj[id].get_name():
            Axis_id = [0, 3]
        elif "Google" in self.joystick_obj[id].get_name():
            Axis_id = [0, 2]
