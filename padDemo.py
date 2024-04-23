import pygame
import curses

def update_buttons(stdscr, buttons):
    positions = {
        0: (4, 12),
        1: (3, 28),
        3: (3, 1),
        4: (2, 12),
        6: (6, 0),
        7: (6, 14),
        11: (8, 28),
        13: (8, 0),
        14: (8, 14)
    }
    for button, state in buttons.items():
        if button in positions:
            y, x = positions[button]
            stdscr.addstr(y, x, f"Button{button}: [{'x' if state else ' '}]")

def update_axes(stdscr, axes):
    stdscr.addstr(10, 0, f"Axis5: {axes.get(5, 0):.3f}   Axis4: {axes.get(4, 0):.3f} ")
    stdscr.addstr(12, 0, f"Axis0X: {axes.get(0, 0):.3f}")
    stdscr.addstr(13, 0, f"Axis1Y: {axes.get(1, 0):.3f}")
    stdscr.addstr(12, 18, f"Axis2X: {axes.get(2, 0):.3f}")
    stdscr.addstr(13, 18, f"Axis3Y: {axes.get(3, 0):.3f}")

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() < 1:
        stdscr.addstr(0, 0, "No joystick detected!")
        stdscr.refresh()
        return
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    buttons = {i: False for i in range(joystick.get_numbuttons())}
    axes = {i: 0.0 for i in range(joystick.get_numaxes())}

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    buttons[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    buttons[event.button] = False
                elif event.type == pygame.JOYAXISMOTION:
                    axes[event.axis] = event.value

            update_buttons(stdscr, buttons)
            update_axes(stdscr, axes)
            stdscr.refresh()

            char = stdscr.getch()
            if char == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        pygame.joystick.quit()
        pygame.quit()

curses.wrapper(main)
