def thankyou(frame):
    global lastWord
    for hand in frame.hands:

        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)

                if (swipe.state != Leap.Gesture.STATE_START):
                    if (90 >= swipe.direction.pitch * Leap.RAD_TO_DEG >= 0 and 30 >= abs(swipe.direction.yaw))) == True:
                        print "Thank You"
