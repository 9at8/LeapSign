import Leap
import sys
import time
import vlc
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

lastWord = None


def player(file):
    p = vlc.MediaPlayer('Audio/' + file + '.mp3')
    p.play()


def cold(frame):
    global lastWord
    cold = [False, False]

    for hand in frame.hands:

        normal = hand.palm_normal
        strength = hand.grab_strength

        if hand.is_left and strength > 0.9:
            if 110 >= (normal.roll * Leap.RAD_TO_DEG) >= 70:
                cold[0] = True
            else:
                cold[0] = False
        elif hand.is_right and strength > 0.9:
            if -110 <= (normal.roll * Leap.RAD_TO_DEG) <= -70:
                cold[1] = True
            else:
                cold[1] = False
        if cold[0] and cold[1]:
            lastWord = 'cold'
            print 'cold'
            player('cold')


def house(frame):
    global lastWord
    house = [False, False]

    for hand in frame.hands:

        normal = hand.palm_normal
        direction = hand.direction
        strength = hand.grab_strength

        if hand.is_left and strength == 0:
            if (100 >= (direction.yaw * Leap.RAD_TO_DEG) >= 60) and (50 >= (normal.roll * Leap.RAD_TO_DEG) >= 20):
                house[0] = True
            else:
                house[0] = False
        elif hand.is_right and strength == 0:
            if (-100 <= direction.yaw * Leap.RAD_TO_DEG <= -60) and (-50 <= normal.roll * Leap.RAD_TO_DEG <= -20):
                house[1] = True
            else:
                house[1] = False

        if house[0] and house[1]:
            lastWord = 'house'
            print 'house'
            player('house')


def love(frame):
    global lastWord
    for hand in frame.hands:
        TYPE_THUMB = 0;
        TYPE_INDEX = TYPE_PROXIMAL = 1
        TYPE_MIDDLE = TYPE_INTERMEDIATE = 2
        TYPE_RING = TYPE_DISTAL = 3
        TYPE_PINKY = 4

        angle_to_index = 0.0
        angle_to_middle = 0.0
        angle_to_ring = 0.0
        angle_to_pinky = 0.0
        angle_between_thumb = 0.0
        projection_on_direction_thumb = 0.0

        for finger in hand.fingers:

            if finger.type == TYPE_THUMB:
                for i in xrange(4):
                    bone_i = finger.bone(i)
                    if bone_i.type == TYPE_PROXIMAL:
                        projection_on_direction_thumb = bone_i.direction.dot(hand.direction) / hand.direction.magnitude

            elif finger.type == TYPE_INDEX:
                for i in xrange(4):
                    bone = finger.bone(i)
                    if bone.type == TYPE_DISTAL:
                        angle_to_index = bone.direction.angle_to(hand.direction)

            elif finger.type == TYPE_MIDDLE:
                for i in xrange(4):
                    bone = finger.bone(i)
                    if bone.type == TYPE_DISTAL:
                        angle_to_middle = bone.direction.angle_to(hand.direction)

            elif finger.type == TYPE_RING:
                for i in xrange(4):
                    bone = finger.bone(i)
                    if bone.type == TYPE_DISTAL:
                        angle_to_ring = bone.direction.angle_to(hand.direction)
            else:
                for i in xrange(4):
                    bone = finger.bone(i)
                    if bone.type == TYPE_DISTAL:
                        angle_to_pinky = bone.direction.angle_to(hand.direction)

        index_up = False if angle_to_index < 1 else True
        middle_up = False if angle_to_middle < 1 else True
        ring_up = False if angle_to_ring < 1 else True
        pinky_up = False if angle_to_pinky < 1 else True
        thumb_up = False if projection_on_direction_thumb < -.75 else True

        if index_up and not middle_up and not ring_up and pinky_up and thumb_up:
            print 'I love you'
            lastWord = 'love'
            player('ily')


def please(frame):
    global lastWord
    for hand in frame.hands:
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2) == False:
                    if hand.is_right:
                        if circle.state != Leap.Gesture.STATE_START:
                            if hand.palm_normal.roll * Leap.RAD_TO_DEG <= -65 and hand.palm_normal.roll * Leap.RAD_TO_DEG >= -115:
                                if hand.direction.yaw * Leap.RAD_TO_DEG >= -115 and hand.direction.yaw * Leap.RAD_TO_DEG <= -65:
                                    if circle.progress >= 1.75:
                                        lastWord = 'please'
                                        print 'please'
                                        player('please')


class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print 'Initialized'

    def on_connect(self, controller):
        print 'Motion Sensor Connected'

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print 'Motion Sensor Disconnected'

    def on_exit(self, controller):
        print 'Exited'

    def on_frame(self, controller):
        global lastWord
        frame = controller.frame()

        time.sleep(0.2)

        if lastWord != 'please':
            please(frame)

        if lastWord != 'house':
            house(frame)

        if lastWord != 'cold':
            cold(frame)

        if lastWord != 'love':
            love(frame)


def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print 'Press enter to quit'
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == '__main__':
    main()
