import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
lastWord = "lol"
TYPE_THUMB=TYPE_METACARPAL=0;
TYPE_INDEX=TYPE_PROXIMAL=1
TYPE_MIDDLE=TYPE_INTERMEDIATE=2
TYPE_RING=TYPE_DISTAL=3
TYPE_PINKY=4
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def mom_grandma_dad_grandpa(frame):
    global lastWord
    for hand in frame.hands:
        if hand.sphere_radius > 80:
            handChirality = 1 if hand.is_right else -1
            if Leap.PI/6 < hand.direction.pitch < Leap.PI/3:
                if -2*Leap.PI/3 < handChirality*hand.palm_normal.roll < -Leap.PI/3:
                    for gesture in frame.gestures():
                        if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                            circle = CircleGesture(gesture)
                            if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2) if handChirality == -1 else not (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2): #clockwise
                                if circle.state != Leap.Gesture.STATE_START:
                                    if circle.progress >= .75:
                                        if lastWord != "grandma":
                                            print "grandma"
                                            lastWord = "grandma"
                                            return True
                    if lastWord != "mom":
                        print "mom"
                        lastWord = "mom"
                        return True
            if Leap.PI/3 < hand.direction.pitch < 2*Leap.PI/3:
                if -2*Leap.PI/3 < handChirality*hand.palm_normal.roll < -Leap.PI/3:
                    for gesture in frame.gestures():
                        if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                            circle = CircleGesture(gesture)
                            if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2) if handChirality == -1 else not (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2): #clockwise
                                if circle.state != Leap.Gesture.STATE_START:
                                    if circle.progress >= .75:
                                        if lastWord != "grandpa":
                                            print "grandpa"
                                            lastWord = "grandpa"
                                            return True
                    if lastWord != "dad":
                        print "dad"
                        lastWord = "dad"
                        return True
        return False
def cross_fingers(frame):
    for hand in frame.hands:
        disp_metacarpal=0.0
        disp_distal=0.0
        index_finger =None
        middle_finger =None
        index_finger_distal =None
        middle_finger_distal =None
        index_finger_metacarpal =None
        middle_finger_metacarpal =None
        for i in xrange(0,5):
            finger_i=hand.fingers[i]
            if finger_i.type==TYPE_MIDDLE:
                middle_finger=finger_i
            elif finger_i.type==TYPE_INDEX:
                index_finger=finger_i
        for i in xrange(0,4):
            bone1=index_finger.bone(i)
            bone2=middle_finger.bone(i)
            if bone1.type==TYPE_DISTAL:
                index_finger_distal=bone1
            elif bone1.type==TYPE_METACARPAL:
                index_finger_metacarpal=bone1
            if bone2.type==TYPE_DISTAL:
                middle_finger_distal=bone2
            elif bone2.type==TYPE_METACARPAL:
                middle_finger_metacarpal=bone2
        if (index_finger_distal.center-middle_finger_distal.center).angle_to(index_finger_metacarpal.center-middle_finger_metacarpal.center) > Leap.PI/2:
            if lastWord != "are":
                print "are"
                lastWord="are"
                return True
        return False
        #print str((index_finger_distal.center-middle_finger_distal.center).angle_to(index_finger_metacarpal.center-middle_finger_metacarpal.center))



def number(frame):
    global lastWord
    for hand in frame.hands:
        handChirality = 1 if hand.is_right else -1
        if -Leap.PI/3 < handChirality*hand.palm_normal.roll < Leap.PI/3:
            #print "pitch of direction: " + str(hand.direction.pitch*Leap.RAD_TO_DEG) +"  Roll of palm_normal: "+ str(hand.palm_normal.roll*Leap.RAD_TO_DEG)
            #print "hand palm radius: " + str(hand.sphere_radius)
            #print "palm velocity: " + str(hand.palm_velocity.magnitude)
                #print "cross product between index-distal and other finger distals: "
            angle_to_index=0.0
            angle_to_middle=0.0
            angle_to_ring=0.0
            angle_to_pinky=0.0
            angle_between_thumb=0.0
            projection_on_direction_thumb=0.0
            for finger in hand.fingers:
                '''if finger.type==TYPE_THUMB:
                    for i in xrange(4):
                        bone_i=finger.bone(i)
                        if bone_i.type==TYPE_DISTAL:
                            for j in xrange(i+1,4):
                                bone_j=finger.bone(j)
                                if bone_j.type==TYPE_INTERMEDIATE:
                                    angle_between_thumb=bone_i.direction.angle_to(bone_j.direction)
                                    break
                            break
                        elif bone_i.type==TYPE_INTERMEDIATE:
                            for j in xrange(i+1,4):
                                bone_j=finger.bone(j)
                                if bone_j.type==TYPE_DISTAL:
                                    angle_between_thumb=bone_i.direction.angle_to(bone_j.direction)
                                    break
                            break'''
                if finger.type==TYPE_THUMB:
                    for i in xrange(4):
                        bone=finger.bone(i)
                        if bone.type==TYPE_PROXIMAL:
                            projection_on_direction_thumb=bone.direction.dot(hand.palm_normal+hand.direction)/(hand.palm_normal+hand.direction).magnitude

                elif finger.type==TYPE_INDEX:
                    for i in xrange(4):
                        bone=finger.bone(i)
                        if bone.type==TYPE_DISTAL:
                            angle_to_index=bone.direction.angle_to(hand.direction)
                elif finger.type==TYPE_MIDDLE:
                    for i in xrange(4):
                        bone=finger.bone(i)
                        if bone.type==TYPE_DISTAL:
                            angle_to_middle=bone.direction.angle_to(hand.direction)
                elif finger.type==TYPE_RING:
                    for i in xrange(4):
                        bone=finger.bone(i)
                        if bone.type==TYPE_DISTAL:
                            angle_to_ring=bone.direction.angle_to(hand.direction)
                else:
                    for i in xrange(4):
                        bone=finger.bone(i)
                        if bone.type==TYPE_DISTAL:
                            angle_to_pinky=bone.direction.angle_to(hand.direction)

            index_up = False if angle_to_index < 1 else True
            middle_up = False if angle_to_middle < 1 else True
            ring_up = False if angle_to_ring < 1 else True
            pinky_up = False if angle_to_pinky < 1 else True
            thumb_up = False if projection_on_direction_thumb < -.9 else True
            #print str(int(pinky_up)) + str(int(ring_up)) + str(int(middle_up)) + str(int(index_up)) + str(int(thumb_up))
            #print str(projection_on_direction_thumb)
            if not index_up and not middle_up and not ring_up and not pinky_up and not thumb_up:
                if RepresentsInt(lastWord):
                    if int(lastWord) != 0:
                        print "0"
                        lastWord = "0"
                        return True
                else:
                    print "0"
                    lastWord = "0"
                    return True
            if index_up and not middle_up and not ring_up and not pinky_up and not thumb_up:
                if RepresentsInt(lastWord):
                    if int(lastWord) != 1:
                        print "1"
                        lastWord = "1"
                        return True
                else:
                    print "1"
                    lastWord = "1"
                    return True
            elif index_up and middle_up and not ring_up and not pinky_up and not thumb_up:
                if RepresentsInt(lastWord):
                    if int(lastWord) != 2:
                        print "2"
                        lastWord = "2"
                        return True
                else:
                    print "2"
                    lastWord = "2"
                    return True
            elif index_up and middle_up and not ring_up and not pinky_up and thumb_up:
                if RepresentsInt(lastWord):
                    if int(lastWord) != 3:
                        print "3"
                        lastWord = "3"
                        return True
                else:
                    print "3"
                    lastWord = "3"
                    return True
            elif index_up and middle_up and ring_up and pinky_up and not thumb_up:
                if RepresentsInt(lastWord):
                    if int(lastWord) != 4:
                        print "4"
                        lastWord = "4"
                        return True
                else:
                    print "4"
                    lastWord = "4"
                    return True
            elif index_up and middle_up and ring_up and pinky_up and thumb_up:
                if RepresentsInt(lastWord):
                    if int(lastWord) != 5:
                        print "5"
                        lastWord = "5"
                        return True
                else:
                    print "5"
                    lastWord = "5"
                    return True
            elif index_up and middle_up and ring_up and not pinky_up and not thumb_up:
                if RepresentsInt(lastWord):
                    if int(lastWord) != 6:
                        print "6"
                        lastWord = "6"
                        return True
                else:
                    print "6"
                    lastWord = "6"
                    return True
            elif index_up and middle_up and not ring_up and pinky_up and thumb_up:
                if RepresentsInt(lastWord):
                    if int(lastWord) != 7:
                        print "7"
                        lastWord = "7"
                        return True
                else:
                    print "7"
                    lastWord = "7"
                    return True
            elif index_up and not middle_up and ring_up and pinky_up and thumb_up:
                if RepresentsInt(lastWord):
                    if int(lastWord) != 8:
                        print "8"
                        lastWord = "8"
                        return True
                else:
                    print "8"
                    lastWord = "8"
                    return True
            elif not index_up and middle_up and ring_up and pinky_up and thumb_up:
                if RepresentsInt(lastWord):
                    if int(lastWord) != 9:
                        print "9"
                        lastWord = "9"
                        return True
                else:
                    print "9"
                    lastWord = "9"
                    return True
            elif not index_up and not middle_up and not ring_up and not pinky_up and thumb_up:
                if RepresentsInt(lastWord):
                    if int(lastWord) != 10:
                        print "10"
                        lastWord = "10"
                        return True
                else:
                    print "10"
                    lastWord = "10"
                    return True
    return False


def no(controller):
    frame = controller.frame()
    past = 1
    last_frame = controller.frame(past)
    if  not last_frame.is_valid:
        return False
    while last_frame.is_valid:
        pinch = None
        last_pinch = None
        for hand in frame.hands:
            pinch = hand.pinch_strength
        for hand in last_frame.hands:
            last_pinch = hand.pinch_strength
        if pinch > last_pinch:
            break
        past +=1
        last_frame = controller.frame(past)
    if past < frame.current_frames_per_second:
        if lastWord != "no"
            print "no"
            lastWord = "no"
            return True
        else return False

class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'pinky']
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
        '''if not mom_grandma_dad_grandpa(frame):
            number(frame)'''
        time.sleep(1.1)

        no(controller)
        #cross_fingers(frame)
        #number(frame)
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
