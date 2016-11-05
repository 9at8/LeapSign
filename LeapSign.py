import Leap
import sys
import time
import vlc
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

TYPE_THUMB = TYPE_METACARPAL = 0
TYPE_INDEX = TYPE_PROXIMAL = 1
TYPE_MIDDLE = TYPE_INTERMEDIATE = 2
TYPE_RING = TYPE_DISTAL = 3

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
            if lastWord != 'cold':
                lastWord = 'cold'
                print 'cold'
                player('cold')
                return True
    return False


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
            if lastWord != 'house':
                lastWord = 'house'
                print 'house'
                player('house')
                return True
    return False


def love(frame):
    global lastWord
    for hand in frame.hands:
        angle_to_index = 0.0
        angle_to_middle = 0.0
        angle_to_ring = 0.0
        angle_to_pinky = 0.0
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
            if lastWord != 'love':
                print 'I love you'
                lastWord = 'love'
                player('ily')
                return True
    return False


def mom_grandma_dad_grandpa(frame):
    global lastWord
    for hand in frame.hands:
        if hand.sphere_radius > 80:
            hand_chirality = 1 if hand.is_right else -1
            if Leap.PI / 6 < hand.direction.pitch < Leap.PI / 3:
                if -2 * Leap.PI / 3 < hand_chirality * hand.palm_normal.roll < -Leap.PI / 3:
                    for gesture in frame.gestures():
                        if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                            circle = CircleGesture(gesture)
                            if (circle.pointable.direction.angle_to(
                                    circle.normal) <= Leap.PI / 2) if hand_chirality == -1 else not (
                                        circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2):  # clockwise
                                if circle.state != Leap.Gesture.STATE_START:
                                    if circle.progress >= .75:
                                        if lastWord != 'grandma':
                                            print 'grandma'
                                            player('grandma')
                                            lastWord = 'grandma'
                                            return True
                    if lastWord != 'mom':
                        print 'mom'
                        player('mom')
                        lastWord = 'mom'
                        return True
            if Leap.PI / 3 < hand.direction.pitch < 2 * Leap.PI / 3:
                if -2 * Leap.PI / 3 < hand_chirality * hand.palm_normal.roll < -Leap.PI / 3:
                    for gesture in frame.gestures():
                        if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                            circle = CircleGesture(gesture)
                            if (circle.pointable.direction.angle_to(
                                    circle.normal) <= Leap.PI / 2) if hand_chirality == -1 else not (
                                        circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2):  # clockwise
                                if circle.state != Leap.Gesture.STATE_START:
                                    if circle.progress >= .75:
                                        if lastWord != 'grandpa':
                                            print 'grandpa'
                                            player('grandpa')
                                            lastWord = 'grandpa'
                                            return True
                    if lastWord != 'dad':
                        print 'dad'
                        player('dad')
                        lastWord = 'dad'
                        return True
        return False


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def number(frame):
    global lastWord
    for hand in frame.hands:
        hand_chirality = 1 if hand.is_right else -1
        if -Leap.PI / 3 < hand_chirality * hand.palm_normal.roll < Leap.PI / 3:
            angle_to_index = 0.0
            angle_to_middle = 0.0
            angle_to_ring = 0.0
            angle_to_pinky = 0.0
            projection_on_direction_thumb = 0.0
            for finger in hand.fingers:
                if finger.type == TYPE_THUMB:
                    for i in xrange(4):
                        bone = finger.bone(i)
                        if bone.type == TYPE_PROXIMAL:
                            projection_on_direction_thumb = bone.direction.dot(hand.palm_normal + hand.direction) / (
                                hand.palm_normal + hand.direction).magnitude

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
            thumb_up = False if projection_on_direction_thumb < -.9 else True

            if not index_up and not middle_up and not ring_up and not pinky_up and not thumb_up:
                if represents_int(lastWord):
                    if int(lastWord) != 0:
                        print '0'
                        player('zero')
                        lastWord = '0'
                        return True
                else:
                    print '0'
                    player('zero')
                    lastWord = '0'
                    return True
            elif index_up and not middle_up and not ring_up and not pinky_up and not thumb_up:
                if represents_int(lastWord):
                    if int(lastWord) != 1:
                        print '1'
                        player('one')
                        lastWord = '1'
                        return True
                else:
                    print '1'
                    player('one')
                    lastWord = '1'
                    return True
            elif index_up and middle_up and not ring_up and not pinky_up and not thumb_up:
                if represents_int(lastWord):
                    if int(lastWord) != 2:
                        print '2'
                        player('two')
                        lastWord = '2'
                        return True
                else:
                    print '2'
                    player('two')
                    lastWord = '2'
                    return True
            elif index_up and middle_up and not ring_up and not pinky_up and thumb_up:
                if represents_int(lastWord):
                    if int(lastWord) != 3:
                        print '3'
                        player('three')
                        lastWord = '3'
                        return True
                else:
                    print '3'
                    player('three')
                    lastWord = '3'
                    return True
            elif index_up and middle_up and ring_up and pinky_up and not thumb_up:
                if represents_int(lastWord):
                    if int(lastWord) != 4:
                        print '4'
                        player('four')
                        lastWord = '4'
                        return True
                else:
                    print '4'
                    player('four')
                    lastWord = '4'
                    return True
            elif index_up and middle_up and ring_up and pinky_up and thumb_up:
                if represents_int(lastWord):
                    if int(lastWord) != 5:
                        print '5'
                        player('five')
                        lastWord = '5'
                        return True
                else:
                    print '5'
                    player('five')
                    lastWord = '5'
                    return True
            elif index_up and middle_up and ring_up and not pinky_up and not thumb_up:
                if represents_int(lastWord):
                    if int(lastWord) != 6:
                        print '6'
                        player('six')
                        lastWord = '6'
                        return True
                else:
                    print '6'
                    player('six')
                    lastWord = '6'
                    return True
            elif index_up and middle_up and not ring_up and pinky_up and thumb_up:
                if represents_int(lastWord):
                    if int(lastWord) != 7:
                        print '7'
                        player('seven')
                        lastWord = '7'
                        return True
                else:
                    print '7'
                    player('seven')
                    lastWord = '7'
                    return True
            elif index_up and not middle_up and ring_up and pinky_up and thumb_up:
                if represents_int(lastWord):
                    if int(lastWord) != 8:
                        print '8'
                        player('eight')
                        lastWord = '8'
                        return True
                else:
                    print '8'
                    player('eight')
                    lastWord = '8'
                    return True
            elif not index_up and middle_up and ring_up and pinky_up and thumb_up:
                if represents_int(lastWord):
                    if int(lastWord) != 9:
                        print '9'
                        player('nine')
                        lastWord = '9'
                        return True
                else:
                    print '9'
                    player('nine')
                    lastWord = '9'
                    return True
            elif not index_up and not middle_up and not ring_up and not pinky_up and thumb_up:
                if represents_int(lastWord):
                    if int(lastWord) != 10:
                        print '10'
                        player('ten')
                        lastWord = '10'
                        return True
                else:
                    print '10'
                    player('ten')
                    lastWord = '10'
                    return True
    return False


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
                                        if lastWord != 'please':
                                            lastWord = 'please'
                                            print 'please'
                                            player('please')
                                            return True
    return False


class LeapMotionListener(Leap.Listener):
    def on_init(self, controller):
        print 'Initialized'

    def on_connect(self, controller):
        print 'Motion Sensor Connected'

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print 'Motion Sensor Disconnected'

    def on_exit(self, controller):
        print 'Exited'

    def on_frame(self, controller):
        global lastWord
        frame = controller.frame()

        if lastWord != 'please':
            please(frame)

        if lastWord != 'house':
            house(frame)

        if lastWord != 'cold':
            cold(frame)

        if lastWord != 'love':
            love(frame)
        if not please(frame):
            if not house(frame):
                if not love(frame):
                    if not cold(frame):
                        if not mom_grandma_dad_grandpa(frame):
                            number(frame)
                            time.sleep(0.7)


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
