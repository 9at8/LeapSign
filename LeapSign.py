import Leap
import sys
import time
import vlc
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

TYPE_THUMB = TYPE_METACARPAL = 0
TYPE_INDEX = TYPE_PROXIMAL = 1
TYPE_MIDDLE = TYPE_INTERMEDIATE = 2
TYPE_RING = TYPE_DISTAL = 3

lastWord = -1


def player(file):
    # p = vlc.MediaPlayer('Audio\' + raw(file) + raw()'.mp3')
    p = vlc.MediaPlayer("Audio/" + file + ".mp3")
    p.play()


def area(frame):
    global lastWord
    op = False
    for hand in frame.hands:
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2:
                    if hand.is_right:
                        if circle.state != Leap.Gesture.STATE_START:
                            if abs(hand.palm_normal.roll) * Leap.RAD_TO_DEG <= 45:
                                if abs(hand.direction.yaw) * Leap.RAD_TO_DEG <= 45:
                                    if circle.progress >= 1.75:
                                        op = True
    if op and lastWord != 'area':
        print 'area'
        player('area')
        lastWord = 'area'
        return True
    return False

def but(frame):
    global lastWord
    if lastWord == "but":
        return False
    lhand = rhand = False
    if len(frame.hands) == 2:
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
#                print str(swipe.direction.yaw * Leap.RAD_TO_DEG) + " " + str(swipe.direction.roll * Leap.RAD_TO_DEG)
                if abs(swipe.direction.yaw * Leap.RAD_TO_DEG - 90) <= 35 and abs(swipe.direction.roll * Leap.RAD_TO_DEG - 90) <= 35:
                    lhand = True
#                    print "Left ok !"
                if abs(swipe.direction.yaw * Leap.RAD_TO_DEG + 90) <= 35 and abs(swipe.direction.roll * Leap.RAD_TO_DEG + 90) <= 35:
                    rhand = True
#                    print "Right ok !"
    if lhand and rhand:
        lastWord = "but"
        print "but"
        return True
    return False

def can(frame):
    global lastWord
    if lastWord == "can":
        return False
    if len(frame.hands) != 2:
        return False
    hand0 = frame.hands[0]
    hand1 = frame.hands[1]
    if hand0.grab_strength > 0.7 and hand1.grab_strength > 0.7:
        if hand0.sphere_radius < 40 and hand1.sphere_radius < 40:
            if hand0.palm_velocity.magnitude > 700 and hand1.palm_velocity.magnitude > 700:
                time.sleep(0.5)
                print "can"
                player('can')
                lastWord = "can"
                return True
    return False


def cold(frame):
    global lastWord
    cold = [False, False]

    for hand in frame.hands:

        normal = hand.palm_normal
        strength = hand.grab_strength

        if hand.is_left and strength == 1:
            if 110 >= (normal.roll * Leap.RAD_TO_DEG) >= 70 and abs(hand.direction.pitch * Leap.RAD_TO_DEG) <=20:
                cold[0] = True
            else:
                cold[0] = False
        elif hand.is_right and strength == 1:
            if -110 <= (normal.roll * Leap.RAD_TO_DEG) <= -70  and abs(hand.direction.pitch * Leap.RAD_TO_DEG) <=20:
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


def day(frame):
    global lastWord
    lefthand = False
    righthand = False
    if frame.hands == 2:
        lefthand = True
        righthand = True
    for hand in frame.hands:
        if hand.is_left:
#            print "LEFT: " + str(hand.palm_normal.roll * Leap.RAD_TO_DEG) + " " + str(hand.direction.roll * Leap.RAD_TO_DEG)
            lefthand = (abs(hand.palm_normal.roll * Leap.RAD_TO_DEG + 180) <=50) and (abs(hand.direction.roll * Leap.RAD_TO_DEG-90) <= 50)
        else:
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    if swipe.state != Leap.Gesture.STATE_START:
#                        print "RIGHT " + str(swipe.direction.yaw * Leap.RAD_TO_DEG) + " " + str(swipe.direction.roll * Leap.RAD_TO_DEG)
                        righthand = abs(swipe.direction.yaw * Leap.RAD_TO_DEG - 90) <= 50 and abs(swipe.direction.roll * Leap.RAD_TO_DEG - 130) <= 50
    if lefthand and righthand and lastWord != 'day':
        print 'day'
        player('day')
        lastWord = 'day'
        return True
    return False


def hi(frame):
    global lastWord
    righthand = False

    for hand in frame.hands:
        if len(frame.hands) == 1:
            if hand.is_right:
                for gesture in frame.gestures():
                    if gesture.type == Leap.Gesture.TYPE_SWIPE:
                        swipe = SwipeGesture(gesture)
                        if (swipe.state != Leap.Gesture.STATE_START):
                            #                            print str(swipe.direction.yaw * Leap.RAD_TO_DEG) + " " + str(swipe.direction.roll * Leap.RAD_TO_DEG)
                            if (abs(swipe.direction.yaw * Leap.RAD_TO_DEG - 95) <= 30 and abs(
                                            swipe.direction.roll * Leap.RAD_TO_DEG - 95) <= 30):
                                #                                print str(hand.palm_normal.yaw * Leap.RAD_TO_DEG) + " " + str(hand.palm_normal.pitch * Leap.RAD_TO_DEG)
                                if abs(hand.palm_normal.yaw * Leap.RAD_TO_DEG + 30) <= 30 and abs(
                                                        hand.palm_normal.pitch * Leap.RAD_TO_DEG + 30) <= 30:
                                    righthand = True
    if righthand and lastWord != 'hi':
        print "hi"
        player('hi')
        lastWord = "hi"


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

def judges(frame):
    global lastWord
    if lastWord == "judges":
        return False;
    lhand = rhand = False
    if len(frame.hands) == 2:
        for hand in frame.hands:
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
    #                print str(swipe.direction.pitch * Leap.RAD_TO_DEG) + " " + str(swipe.direction.roll * Leap.RAD_TO_DEG)
                    if abs(abs(swipe.direction.pitch * Leap.RAD_TO_DEG)-90) <= 20 and abs(abs(swipe.direction.roll * Leap.RAD_TO_DEG)-180) <= 20 and hand.pinch_strength == 1 and hand.is_right == True:
                        lhand = True
    #                    print "Left ok !"
                    if abs(swipe.direction.pitch * Leap.RAD_TO_DEG + 90) <= 20 and abs(swipe.direction.roll * Leap.RAD_TO_DEG) <= 20 and hand.pinch_strength ==1 and hand.is_left == True:
                        rhand = True
    #                    print "Right ok !"
    if lhand and rhand:
        lastWord = "judges"
        print "judges"
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
            if abs(hand.palm_normal.angle_to(Leap.Vector(0,-1,0))) * Leap.RAD_TO_DEG <= 30:
                if lastWord != 'love':
                    print 'I love you'
                    lastWord = 'love'
                    player('ily')
                    return True
    return False


def mom_grandma_dad_grandpa(frame):
    global lastWord
    for hand in frame.hands:
        if len(frame.hands) == 1:
            if hand.sphere_radius > 80:
                handChirality = 1 if hand.is_right else -1
                if hand.palm_normal.angle_to(Leap.Vector(-1,0,0)) < Leap.PI/6 if handChirality==1 else hand.palm_normal.angle_to(Leap.Vector(1,0,0)) < Leap.PI/6:
                    if Leap.PI/6 < hand.direction.angle_to(Leap.Vector(0,0,-1)) < 3*Leap.PI/8:
                        for gesture in frame.gestures():
                            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                                circle = CircleGesture(gesture)
                                if (circle.pointable.direction.angle_to(
                                        circle.normal) <= Leap.PI / 2) if handChirality == -1 else not (
                                    circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2):  # clockwise
                                    if circle.state != Leap.Gesture.STATE_START:
                                        if circle.progress >= 1.25:
                                            if lastWord != "grandma":
                                                time.sleep(0.5)
                                                print "grandma"
                                                player('grandma')
                                                lastWord = "grandma"
                                                return True
                        if lastWord != "mom":
                            time.sleep(0.5)
                            print "mom"
                            player('mom')
                            lastWord = "mom"
                            return True
                    if 5*Leap.PI/12 < hand.direction.angle_to(Leap.Vector(0,0,-1)) < 2*Leap.PI/3:
                        for gesture in frame.gestures():
                            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                                circle = CircleGesture(gesture)
                                if (circle.pointable.direction.angle_to(
                                        circle.normal) <= Leap.PI / 2) if handChirality == -1 else not (
                                    circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2):  # clockwise
                                    if circle.state != Leap.Gesture.STATE_START:
                                        if circle.progress >= 1.25:
                                            if lastWord != "grandpa":
                                                print "grandpa"
                                                player('grandpa')
                                                lastWord = "grandpa"
                                                return True
                        if lastWord != "dad":
                            print "dad"
                            player('dad')
                            lastWord = "dad"
                            return True
        return False


# def represents_int(s):
#     try:
#         int(s)
#         return True
#     except ValueError or TypeError:
#         return False
#
#
# def number(frame):
#     global lastWord
#     for hand in frame.hands:
#         hand_chirality = 1 if hand.is_right else -1
#         if -Leap.PI / 3 < hand_chirality * hand.palm_normal.roll < Leap.PI / 3:
#             angle_to_index = 0.0
#             angle_to_middle = 0.0
#             angle_to_ring = 0.0
#             angle_to_pinky = 0.0
#             projection_on_direction_thumb = 0.0
#             for finger in hand.fingers:
#                 if finger.type == TYPE_THUMB:
#                     for i in xrange(4):
#                         bone = finger.bone(i)
#                         if bone.type == TYPE_PROXIMAL:
#                             projection_on_direction_thumb = bone.direction.dot(hand.palm_normal + hand.direction) / (
#                                 hand.palm_normal + hand.direction).magnitude
#
#                 elif finger.type == TYPE_INDEX:
#                     for i in xrange(4):
#                         bone = finger.bone(i)
#                         if bone.type == TYPE_DISTAL:
#                             angle_to_index = bone.direction.angle_to(hand.direction)
#                 elif finger.type == TYPE_MIDDLE:
#                     for i in xrange(4):
#                         bone = finger.bone(i)
#                         if bone.type == TYPE_DISTAL:
#                             angle_to_middle = bone.direction.angle_to(hand.direction)
#                 elif finger.type == TYPE_RING:
#                     for i in xrange(4):
#                         bone = finger.bone(i)
#                         if bone.type == TYPE_DISTAL:
#                             angle_to_ring = bone.direction.angle_to(hand.direction)
#                 else:
#                     for i in xrange(4):
#                         bone = finger.bone(i)
#                         if bone.type == TYPE_DISTAL:
#                             angle_to_pinky = bone.direction.angle_to(hand.direction)
#
#             index_up = False if angle_to_index < 1 else True
#             middle_up = False if angle_to_middle < 1 else True
#             ring_up = False if angle_to_ring < 1 else True
#             pinky_up = False if angle_to_pinky < 1 else True
#             thumb_up = False if projection_on_direction_thumb < -.9 else True
#
#             if not index_up and not middle_up and not ring_up and not pinky_up and not thumb_up:
#                 if represents_int(lastWord):
#                     if int(lastWord) != 0:
#                         print '0'
#                         player('zero')
#                         lastWord = '0'
#                         return True
#                 else:
#                     print '0'
#                     player('zero')
#                     lastWord = '0'
#                     return True
#             elif index_up and not middle_up and not ring_up and not pinky_up and not thumb_up:
#                 if represents_int(lastWord):
#                     if int(lastWord) != 1:
#                         print '1'
#                         player('one')
#                         lastWord = '1'
#                         return True
#                 else:
#                     print '1'
#                     player('one')
#                     lastWord = '1'
#                     return True
#             elif index_up and middle_up and not ring_up and not pinky_up and not thumb_up:
#                 if represents_int(lastWord):
#                     if int(lastWord) != 2:
#                         print '2'
#                         player('two')
#                         lastWord = '2'
#                         return True
#                 else:
#                     print '2'
#                     player('two')
#                     lastWord = '2'
#                     return True
#             elif index_up and middle_up and not ring_up and not pinky_up and thumb_up:
#                 if represents_int(lastWord):
#                     if int(lastWord) != 3:
#                         print '3'
#                         player('three')
#                         lastWord = '3'
#                         return True
#                 else:
#                     print '3'
#                     player('three')
#                     lastWord = '3'
#                     return True
#             elif index_up and middle_up and ring_up and pinky_up and not thumb_up:
#                 if represents_int(lastWord):
#                     if int(lastWord) != 4:
#                         print '4'
#                         player('four')
#                         lastWord = '4'
#                         return True
#                 else:
#                     print '4'
#                     player('four')
#                     lastWord = '4'
#                     return True
#             elif index_up and middle_up and ring_up and pinky_up and thumb_up:
#                 if represents_int(lastWord):
#                     if int(lastWord) != 5:
#                         print '5'
#                         player('five')
#                         lastWord = '5'
#                         return True
#                 else:
#                     print '5'
#                     player('five')
#                     lastWord = '5'
#                     return True
#             elif index_up and middle_up and ring_up and not pinky_up and not thumb_up:
#                 if represents_int(lastWord):
#                     if int(lastWord) != 6:
#                         print '6'
#                         player('six')
#                         lastWord = '6'
#                         return True
#                 else:
#                     print '6'
#                     player('six')
#                     lastWord = '6'
#                     return True
#             elif index_up and middle_up and not ring_up and pinky_up and thumb_up:
#                 if represents_int(lastWord):
#                     if int(lastWord) != 7:
#                         print '7'
#                         player('seven')
#                         lastWord = '7'
#                         return True
#                 else:
#                     print '7'
#                     player('seven')
#                     lastWord = '7'
#                     return True
#             elif index_up and not middle_up and ring_up and pinky_up and thumb_up:
#                 if represents_int(lastWord):
#                     if int(lastWord) != 8:
#                         print '8'
#                         player('eight')
#                         lastWord = '8'
#                         return True
#                 else:
#                     print '8'
#                     player('eight')
#                     lastWord = '8'
#                     return True
#             elif not index_up and middle_up and ring_up and pinky_up and thumb_up:
#                 if represents_int(lastWord):
#                     if int(lastWord) != 9:
#                         print '9'
#                         player('nine')
#                         lastWord = '9'
#                         return True
#                 else:
#                     print '9'
#                     player('nine')
#                     lastWord = '9'
#                     return True
#             elif not index_up and not middle_up and not ring_up and not pinky_up and thumb_up:
#                 if represents_int(lastWord):
#                     if int(lastWord) != 10:
#                         print '10'
#                         player('ten')
#                         lastWord = '10'
#                         return True
#                 else:
#                     print '10'
#                     player('ten')
#                     lastWord = '10'
#                     return True
#     return False


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
                                if abs(hand.direction.yaw * Leap.RAD_TO_DEG +65 ) <= 30:
                                    if circle.progress >= 1.75:
                                        if lastWord != 'please':
                                            lastWord = 'please'
                                            print 'please'
                                            player('please')
                                            return True
    return False


def strong(frame):
    global lastWord
    strong = [False, False]

    for hand in frame.hands:

        normal = hand.palm_normal
        direction = hand.direction
        strength = hand.grab_strength

        if hand.is_left and strength >= 0.9:
            if 100 >= (direction.yaw * Leap.RAD_TO_DEG) >= 60:
                strong[0] = True
            else:
                strong[0] = False
        elif hand.is_right and strength >= 0.9:
            if -100 <= direction.yaw * Leap.RAD_TO_DEG <= -60:
                strong[1] = True
            else:
                strong[1] = False

        if strong[0] and strong[1]:
            if lastWord != 'strong':
                lastWord = 'strong'
                print 'strong'
                player('strong')
                return True
    return False


def what(frame):
    global lastWord
    lhand = False
    rhand = False
    controller = Leap.Controller()
    for hand in frame.hands:
        if abs(hand.palm_normal.roll) * Leap.RAD_TO_DEG > 150:
            if abs(hand.palm_normal.pitch * Leap.RAD_TO_DEG - 90) < 30:
                if hand.is_left and hand.grab_strength == 0:
                    lhand = True
                if hand.is_right and hand.grab_strength == 0:
                    rhand = True
    if lhand and rhand and lastWord != 'what':
        print 'what'
        player('what')
        lastWord = 'what'
        return True
    return False


def yes(frame):
    global lastWord
    if lastWord == "yes":
        return False
    if len(frame.hands) != 1:
        return False
    for hand in frame.hands:
        if hand.palm_normal.angle_to(Leap.Vector(0,-1,0)) > 1.0:
            return False
        if hand.grab_strength > 0.7:
            if hand.sphere_radius < 40:
                if hand.palm_velocity.magnitude > 700:
                    time.sleep(0.5)
                    print "yes"
                    player('yes')
                    lastWord = "yes"
                    time.sleep(0.5)
                    return True
    return False


# def you(frame):
#     global lastWord
#     f = [False, False, False, False, False]
#     for hand in frame.hands:
#         if hand.is_right and len(frame.hands) == 1:
#             for finger in hand.fingers:
#                 if finger.type == 1:
#                     for b in range(0, 4):
#                         bone = finger.bone(b)
#                         if bone.type == 3:
#                             f[1] = (abs(bone.direction.yaw * Leap.RAD_TO_DEG - 135) < 30) \
#                                    and (abs(bone.direction.pitch * Leap.RAD_TO_DEG + 165) < 30)
#                 elif finger.type != 0:
#                     for b in range(0, 4):
#                         bone = finger.bone(b)
#                         if bone.type == 1:
#                             f[finger.type] = (abs(bone.direction.yaw * Leap.RAD_TO_DEG - 90) < 30) \
#                                              and (abs(bone.direction.pitch * Leap.RAD_TO_DEG + 90) < 30)
#     if f[1] and f[2] and f[3] and f[4] and lastWord != 'you':
#         print 'you'
#         player('you')
#         lastWord = 'you'
#         return True
#     return False


def you(frame):
    global lastWord
    f = [False, False, False, False, False]
    for hand in frame.hands:
        if hand.is_right and len(frame.hands) == 1:
            for finger in hand.fingers:
                if finger.type == 1:
                    for b in range(0, 4):
                        bone = finger.bone(b)
                        if bone.type == 3:
                            #                            print "INDEX: " + str(bone.direction.yaw * Leap.RAD_TO_DEG) + " " + str(bone.direction.pitch * Leap.RAD_TO_DEG)
                            if abs(bone.direction.yaw * Leap.RAD_TO_DEG - 135) < 30 and abs(
                                                    bone.direction.pitch * Leap.RAD_TO_DEG + 165) < 30:
                                f[1] = True
                elif finger.type != 0:
                    for b in range(0, 4):
                        bone = finger.bone(b)
                        if bone.type == 1:
                            #                            print str(bone.direction.yaw * Leap.RAD_TO_DEG) + " " + str(bone.direction.pitch * Leap.RAD_TO_DEG)
                            if abs(bone.direction.yaw * Leap.RAD_TO_DEG - 90) < 30 and abs(
                                                    bone.direction.pitch * Leap.RAD_TO_DEG + 90) < 30:
                                f[finger.type] = True
    if f[1] and f[2] and f[3] and f[4]:
        if abs(hand.palm_normal.yaw * Leap.RAD_TO_DEG + 90) <= 30 and abs(
                                hand.palm_normal.roll * Leap.RAD_TO_DEG + 90) <= 30 and lastWord != 'you':
            print "you"
            player('you')
            lastWord = "you"
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

        time.sleep(0.2)

        # if not (cold(frame) or house(frame) or love(frame) or please(frame) or mom_grandma_dad_grandpa(frame)):
        #     number(frame)
        # else:
        #     if lastWord != 'please':
        #         please(frame)
        #
        #     if lastWord != 'house':
        #         house(frame)
        #
        #     if lastWord != 'cold':
        #         cold(frame)
        #
        #     if lastWord != 'love':
        #         love(frame)

        area(frame) or but(frame) or can(frame) or cold(frame) or day(frame) or hi(frame) or house(frame) or judges(frame) or love(frame) \
        or mom_grandma_dad_grandpa(frame) or please(frame) or strong(frame) or what(frame) or yes(frame) or you(frame)


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
