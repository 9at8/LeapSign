import Leap, sys, time


def house(frame):
    house = [False, False]

    for hand in frame.hands:

        normal = hand.palm_normal
        direction = hand.direction

        if hand.is_left:
            if (100 >= (direction.yaw * Leap.RAD_TO_DEG) >= 60) and (50 >= (normal.roll * Leap.RAD_TO_DEG) >= 20):
                house[0] = True
            else:
                house[0] = False
        elif hand.is_right:
            if (-100 <= direction.yaw * Leap.RAD_TO_DEG <= -60) and (-50 <= normal.roll * Leap.RAD_TO_DEG <= -20):
                house[1] = True
            else:
                house[1] = False

        time.sleep(0.3)

        if house[0] and house[1]:
            print 'House'
            # sys.exit(0)


class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpol', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print 'Initialized'

    def on_connect(self, controller):
        print 'Connected'

    def on_disconnect(self, controller):
        print 'Disconnected'

    def on_frame(self, controller):
        frame = (controller.frame())
        house(frame)


def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print 'Press enter to exit'
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == '__main__':
    main()
