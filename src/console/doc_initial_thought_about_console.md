

joystick = init_joystick()

if joystick is not None:

while True:

button_state = get_button_state(joystick)

print(button_state)

check if it is initialized  如果 joystick 模块已经初始化，返回 True。

pygame.joystick.get_init()

back the number of consoles 返回游戏杆的数量。

pygame.joystick.get_count()

pygame.joystick.Joystick.init()  —  初始化

pygame.joystick.Joystick.quit()  —  卸载Joystick

pygame.joystick.Joystick.get_init()  —  检查Joystick是否初始化

pygame.joystick.Joystick.get_id()  —  获得Joystick ID

pygame.joystick.Joystick.get_name()  —  获得 Joystick 系统名称

pygame.joystick.Joystick.get_numaxes()  —  获得 Joystick 操纵轴的数量

pygame.joystick.Joystick.get_axis()  —  获得操纵轴的当前坐标

pygame.joystick.Joystick.get_numballs()  —  获得 Joystick 上追踪球的数量

pygame.joystick.Joystick.get_ball()  —  获得追踪球的相对位置

pygame.joystick.Joystick.get_numbuttons()  —  获得 Joystick 上按钮的数量

pygame.joystick.Joystick.get_button()  —  获得当前按钮状态

pygame.joystick.Joystick.get_numhats()  —  获得 Joystick 上帽键的数量

pygame.joystick.Joystick.get_hat()  —  获得 帽键 的位置

位置包含 x，y 两个值。(0, 0) 表示在中间。-1 代表左/下，1 代表右/上。(x 对应左右, y 对应上下)。所以 (-1, 0) 代表左，(1, 0) 代表右，(0, 1) 代表上，(1, 1) 代表右上。

Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,

JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED

not available-->when the tracking not come , cannot get the button is been entered or not

One button-> control the start and end of  the controller

two ball

    one control the transaction

    one control the rotation
