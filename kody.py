import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

lastWord = None


def please(frame):
    global lastWord
    for hand in frame.hands:
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
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
                                        lastWord = "please"
                                        print 'please'
                                        return


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

        # frame = controller.frame()

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
