import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

lastWord = None

""" KODY'S REFERENCE
Yaw:   -Z on X-Z plane      
Roll:   Y on X-Y plane      
Pitch: -Z on Y-Z plane      
finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
"""
def hi(frame):
    global lastWord
    righthand = False 

    for hand in frame.hands:
        if len(frame.hands)==1:
            if hand.is_right:
                for gesture in frame.gestures():
                    if gesture.type == Leap.Gesture.TYPE_SWIPE:
                        swipe = SwipeGesture(gesture)
                        if (swipe.state != Leap.Gesture.STATE_START):
    #                        print str(swipe.direction.yaw * Leap.RAD_TO_DEG) + " " + str(swipe.direction.roll * Leap.RAD_TO_DEG)
                            righthand = (abs(swipe.direction.yaw * Leap.RAD_TO_DEG -90) <= 30 and abs(swipe.direction.roll * Leap.RAD_TO_DEG -90) <= 30)
    if righthand:
        print "hi "
        lastWord = "hi"


"""
def no(frame):
    global lastWord
    tap = [False,False,False]
    for hand in frame.hands:
        if hand.is_right:
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                    keytap = KeyTapGesture(gesture)
                    print keytap.direction.roll * Leap.RAD_TO_DEG
                    if abs(keytap.direction.roll) * Leap.RAD_TO_DEG >= 150:
                        if abs(keytap.pointable.yaw) * Leap.RAD_TO_DEG <= 45 and abs(keytap.pointable.pitch) * Leap.RAD_TO_DEG <= 45:
                            tap[keytap.pointable.type()]=True;
                            print str(keytap.pointable.type())
    if tap[1] and tap[2] :
        print "no"
        lastWord = "no"
"""


def you(frame):
    global lastWord 
    f = [False,False,False,False,False]
    for hand in frame.hands:
        if hand.is_right and len(frame.hands)==1:
            for finger in hand.fingers:
                if finger.type == 1:
                    for b in range (0,4):
                        bone = finger.bone(b)
                        if bone.type == 3:
#                            print "INDEX: " + str(bone.direction.yaw * Leap.RAD_TO_DEG) + " " + str(bone.direction.pitch * Leap.RAD_TO_DEG)
                            if abs(bone.direction.yaw * Leap.RAD_TO_DEG - 135) < 30 and abs(bone.direction.pitch * Leap.RAD_TO_DEG + 165) < 30:
                                f[1] = True
                elif finger.type != 0:
                    for b in range (0,4):
                        bone = finger.bone(b) 
                        if bone.type == 1:
#                            print str(bone.direction.yaw * Leap.RAD_TO_DEG) + " " + str(bone.direction.pitch * Leap.RAD_TO_DEG)
                            if abs(bone.direction.yaw * Leap.RAD_TO_DEG - 90) < 30 and abs(bone.direction.pitch * Leap.RAD_TO_DEG + 90) < 30:
                                f[finger.type] = True 
    if f[1] and f[2] and f[3] and f[4]:
        print "you"
        lastWord = "you"
                


def what(frame):
    global lastWord
    lhand = False
    rhand = False
    controller = Leap.Controller()
    for hand in frame.hands:
#        print hand.palm_normal
        if abs(hand.palm_normal.roll) * Leap.RAD_TO_DEG > 150:
#            print "\n1"
#            print hand.palm_normal.pitch * Leap.RAD_TO_DEG
            if abs(hand.palm_normal.pitch * Leap.RAD_TO_DEG - 90) < 30:
#                print "\n2"
                if hand.is_left:
                    lhand = True
                if hand.is_right:
                    rhand = True
    if lhand and rhand:
        lastWord = "what"
        print "what"

"""
def no(controller):
    global lastWord
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
        if lastWord != "no":
            print "no"
            lastWord = "no" 
            return True
        else: return False
"""
"""
def please(frame):
    global lastWord
    op = False
    for hand in frame.hands:
        for gesture in frame.gestures():
            
                circle = CircleGesture(gesture)

                # yaw = -90 roll = 90
                if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2) == False:
                    # print "\n1"
                    if hand.is_right:
                        # print "\n2"
                        # swept_angle = 0
                        if circle.state != Leap.Gesture.STATE_START:
                            # print "\n3"
                            # print " Roll : " + str(hand.palm_normal.roll * Leap.RAD_TO_DEG) + " "
                            # previous = CircleGesture(controller.frame(1).gesture(circle.id))
                            # swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI
                            if hand.palm_normal.roll * Leap.RAD_TO_DEG <= -65 and hand.palm_normal.roll * Leap.RAD_TO_DEG >= -115:
                                # print "\n4"
                                if hand.direction.yaw * Leap.RAD_TO_DEG >= -115 and hand.direction.yaw * Leap.RAD_TO_DEG <= -65:
                                    if circle.progress >= 1.75:
                                        op = True
    if op:
        lastWord = "please"
        print 'please'
"""

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
                                            return True
    return False

def area(frame):
    global lastWord
    op = False
    for hand in frame.hands:
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # yaw = -90 roll = 90
                if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2) == True:
#                    print "\n1"
                    if hand.is_right:
#                        print "\n2"
                        swept_angle = 0
                        if circle.state != Leap.Gesture.STATE_START:
#                            print "\n3"
#                            print " Roll : " + str(hand.palm_normal.roll * Leap.RAD_TO_DEG) + " "
                            #previous = CircleGesture(controller.frame(1).gesture(circle.id))
                            #swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI
                            if abs(hand.palm_normal.roll) * Leap.RAD_TO_DEG <= 45:
#                                print "\n4"
#                                print hand.direction.yaw * Leap.RAD_TO_DEG
                                if abs(hand.direction.yaw) * Leap.RAD_TO_DEG <= 45:
                                    if circle.progress >= 1.75:
#                                        print "\n5"
                                        op = True
    if op:
        lastWord = "area"
        print 'area'

"""
def sorry(frame):
    global lastWord
    controller = Leap.Controller()
    for hand in frame.hands:
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # yaw = -90 roll = 90
                if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2) == True:
                    print "\n1"
                    if hand.is_right:
                        print "\n2"
                        # swept_angle = 0
                        if circle.state != Leap.Gesture.STATE_START:
                            # print "\n3"
                            # print " Roll : " + str(hand.palm_normal.roll * Leap.RAD_TO_DEG) + " "

                            previous = CircleGesture(controller.frame(1).gesture(circle.id))
                            swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI
                            print "Palm: " + str(hand.palm_normal.roll * Leap.RAD_TO_DEG) + " " + str(swept_angle)

                            if hand.palm_normal.roll * Leap.RAD_TO_DEG <= -65 and hand.palm_normal.roll * Leap.RAD_TO_DEG >= -115:
                                # print "\n4"
                                print hand.direction.yaw * Leap.RAD_TO_DEG
                                if hand.direction.yaw * Leap.RAD_TO_DEG >= -115 and hand.direction.yaw * Leap.RAD_TO_DEG <= -65:
                                    if circle.progress >= 1.75:
#                                        lastWord = "sorry"
                                        print 'sorry'
"""

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

def day(frame):
    global lastWord
    lefthand = False
    righthand = False 
    if(frame.hands==2):
        lefthand = True
        righthand = True
    for hand in frame.hands:
        if hand.is_left:
            if (abs(hand.palm_normal.roll * Leap.RAD_TO_DEG) >=150 and hand.direction.roll * Leap.RAD_TO_DEG >=60 and hand.direction.roll * Leap.RAD_TO_DEG<=120)==False:
                lefthand = False
            else:
#                print "LEFT OK"
                lefthand = True
        else:
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    if (swipe.state != Leap.Gesture.STATE_START):
#                        print str(swipe.direction.yaw * Leap.RAD_TO_DEG) + " " + str(swipe.direction.roll * Leap.RAD_TO_DEG)
                        if (swipe.direction.yaw * Leap.RAD_TO_DEG >= 45 and swipe.direction.yaw * Leap.RAD_TO_DEG <= 135 and swipe.direction.roll * Leap.RAD_TO_DEG >= 90 and swipe.direction.roll * Leap.RAD_TO_DEG <= 180) == False:
                            righthand= False
                        else:
#                            print "RIGHT OK"
                            righthand=True
    if(lefthand and righthand):
        print "day "
        lastWord = "day"


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

    # lastWord = ""



    def on_frame(self, controller):
        global lastWord
        # print lastWord
        frame = controller.frame()

        time.sleep(0.2)        

        if lastWord != "please":
            please(frame)

        if lastWord != "house":
            house(frame)

        if lastWord != 'cold':
            cold(frame)

        if lastWord != 'day':
            day(frame)

        if lastWord != 'area':
            area(frame)

        if lastWord != 'what':
            what(frame)

        if lastWord != "you":
            you(frame)

        if lastWord != "hi":
            hi(frame)

        """
        for gesture in frame.gestures():

            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                print "Circle ID: " + str(circle.id) + " Radius: " + str(circle.radius)
        """
        """
        if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
            keytap = KeyTapGesture(gesture)
            print "Key Tap ID: " + str(gesture.id) + " State: " + self.state_names[gesture.state] + " Position: " + str(keytap.position) + "Direction: " + str(keytap.direction)
        """

        #frame = controller.frame()

        """
        print "Frame ID: " + str(frame.id) \
            + " Timestamp: " + str(frame.timestamp) \
            + " # of Hands " + str(len(frame.hands)) \
            + " # of Fingrs " + str(len(frame.fingers)) \
            + " # of Tools " + str(len(frame.tools)) \
            + " # of Gestures " + str(len(frame.gestures()))

            for hand in frame.hands:

            handType = "Left Hand" if hand.is_left else "Right Hand"
            print handType + " Hand ID: " + str(hand.id) + " Palm Position: " + str(hand.palm_position)

            normal = hand.palm_normal

            direction = hand.direction
            print "Pitch: " + str(direction.pitch * Leap.RAD_TO_DEG) + " Roll: " + str(normal.roll * Leap.RAD_TO_DEG) + " Yaw: " + str(direction.yaw * Leap.RAD_TO_DEG)

            arm = hand.arm
            print "Arm Direction: " + str(arm.direction) + " Wrist Position: " + str(arm.wrist_position) + " Elbow Position: " + str(arm.elbow_position)

            for finger in hand.fingers:
                print "Type: " + self.finger_names[finger.type()] + " ID: " + str(finger.id) + " Length (mm): " + str(finger.length) + " Width (mm): " + str(finger.width)

                for b in range(0,4):
                    bone = finger.bone(b)
                    print "Bone: " + self.bone_names[bone.type] + " Start: " + str(bone.prev_joint) + " End: " + str(bone.next_joint) + " Direction: " + str(bone.direction)




            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)

					
                    # yaw = -90 roll = 90
                    if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2)==False:
                        #print "\n1"
                        if hand.is_right:
                            #print "\n2"
                            #swept_angle = 0
                            if circle.state != Leap.Gesture.STATE_START:
                                #print "\n3"
                                #print " Roll : " + str(hand.palm_normal.roll * Leap.RAD_TO_DEG) + " "
                                #previous = CircleGesture(controller.frame(1).gesture(circle.id))
                                #swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI
                                if hand.palm_normal.roll * Leap.RAD_TO_DEG <=-65 and hand.palm_normal.roll * Leap.RAD_TO_DEG >= -115:
                                    #print "\n4"
                                    if hand.direction.yaw * Leap.RAD_TO_DEG >=-115 and hand.direction.yaw * Leap.RAD_TO_DEG <= -65 and lastWord != "please" :
                                        if circle.progress >= 1.75:
                                            print "please"
                                            lastWord = "please"




                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                        clockwiseness = "clockwise"
                    else:
                        clockwiseness = "counter-clockwise"

                    swept_angle = 0
                    if circle.state != Leap.Gesture.STATE_START:
                        previous = CircleGesture(controller.frame(1).gesture(circle.id))
                        swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI
                    #print "Circle ID: " + str(circle.id) + " Progress: " +str(circle.progress) + " Radius: " + str(circle.radius) + "Swept Angle: " + str(swept_angle* Leap.RAD_TO_DEG) + clockwiseness

                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    #print "Swipe ID: " + str(swipe.id) + " State: " + self.state_names[gesture.state] + " Position: " + str(swipe.position) + " Direction:" + str(swipe.direction) + " Swipe: (mm/s): " + str(swipe.speed)
        """


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
