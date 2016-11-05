pi=3.14159
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
previous_sign=""
def mom_dad(frame):
    for hand in frame.hands:
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
def number(frame):
    for hand in frame.hands:
        #print "Pitch of direction: " + str(hand.direction.pitch*Leap.RAD_TO_DEG) +"  Roll of palm_normal: "+ str(hand.palm_normal.roll*Leap.RAD_TO_DEG)
        #print "hand palm radius: " + str(hand.sphere_radius)
        #print "palm velocity: " + str(hand.palm_velocity.magnitude)
        #print "cross product between index-distal and other finger distals: "

        TYPE_THUMB=0;
        TYPE_INDEX=TYPE_PROXIMAL=1
        TYPE_MIDDLE=TYPE_INTERMEDIATE=2
        TYPE_RING=TYPE_DISTAL=3
        TYPE_PINKY=4
        '''print "Middle: "+ str(hand.fingers[TYPE_INDEX].bone(TYPE_DISTAL).direction.angle_to(hand.fingers[TYPE_MIDDLE].bone(TYPE_DISTAL).direction)*Leap.RAD_TO_DEG)
        print "Ring: " + str(hand.fingers[TYPE_INDEX].bone(TYPE_DISTAL).direction.angle_to(hand.fingers[TYPE_RING].bone(TYPE_DISTAL).direction)*Leap.RAD_TO_DEG)
        print "Pinky: " + str(hand.fingers[TYPE_INDEX].bone(TYPE_DISTAL).direction.angle_to(hand.fingers[TYPE_PINKY].bone(TYPE_DISTAL).direction)*Leap.RAD_TO_DEG)'''

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
                    bone_i=finger.bone(i)
                    if bone_i.type==TYPE_PROXIMAL:
                        projection_on_direction_thumb=bone_i.direction.dot(hand.direction)/hand.direction.magnitude

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
        thumb_up = False if projection_on_direction_thumb < -.75 else True
        #print str(int(pinky_up)) + str(int(ring_up)) + str(int(middle_up)) + str(int(index_up)) + str(int(thumb_up))
        #print str(projection_on_direction_thumb)
        if index_up and not middle_up and not ring_up and not pinky_up and not thumb_up:
            print "One"
        elif index_up and middle_up and not ring_up and not pinky_up and not thumb_up:
            print "Two"
        elif index_up and middle_up and not ring_up and not pinky_up and thumb_up:
            print "Three"
        elif index_up and middle_up and ring_up and pinky_up and not thumb_up:
            print "Four"
        elif index_up and middle_up and ring_up and pinky_up and thumb_up:
            print "Five"
        elif index_up and middle_up and ring_up and not pinky_up and not thumb_up:
            print "Six"
        elif index_up and middle_up and not ring_up and pinky_up and thumb_up:
            print "Seven"
        elif index_up and not middle_up and ring_up and pinky_up and thumb_up:
            print "Eight"
        elif not index_up and middle_up and ring_up and pinky_up and thumb_up:
            print "Nine"
        elif not index_up and not middle_up and not ring_up and not pinky_up and thumb_up:
            print "Ten"
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
        number(frame)
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
