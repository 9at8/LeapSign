pi=3.14159
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Motion Sensor Connected"

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        previous_sign = "Lol"
        gesture_hands=[]
        for hand in frame.hands:
            #print "Pitch of direction: " + str(hand.direction.pitch*Leap.RAD_TO_DEG) +"  Roll of palm_normal: "+ str(hand.palm_normal.roll*Leap.RAD_TO_DEG)
            #print "hand palm radius: " + str(hand.sphere_radius)
            #print "palm velocity: " + str(hand.palm_velocity.magnitude)
            if hand.sphere_radius > 80:
                handChirality = 1 if hand.is_right else -1
                if pi/6 < hand.direction.pitch < pi/3:
                    if -2*pi/3 < handChirality*hand.palm_normal.roll < -pi/3:
                        if previous_sign != "Mom":
                            print "Mom"
                            previous_sign="Mom"
                if pi/3 < hand.direction.pitch < 2*pi/3:
                    if -2*pi/3 < handChirality*hand.palm_normal.roll < -pi/3:
                        if previous_sign != "Dad":
                            print "Dad"
                            previous_sign="Dad"
def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print "Press enter to quit"
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
