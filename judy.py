pi=3.14159

import Leap,sys, thread, time 
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

lastWord = None

def love(frame):
		global lastWord
		for hand in frame.hands:
			TYPE_THUMB=0;
			TYPE_INDEX=TYPE_PROXIMAL=1
			TYPE_MIDDLE=TYPE_INTERMEDIATE=2
			TYPE_RING=TYPE_DISTAL=3
			TYPE_PINKY=4

			angle_to_index=0.0
			angle_to_middle=0.0
			angle_to_ring=0.0
			angle_to_pinky=0.0
			angle_between_thumb=0.0
			projection_on_direction_thumb=0.0

			for finger in hand.fingers:

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

			print "Pitch: " + str(hand.palm_normal.pitch * Leap.RAD_TO_DEG)
			print "Yaw: " + str(hand.palm_normal.yaw * Leap.RAD_TO_DEG)

			if index_up and not middle_up and not ring_up and pinky_up and thumb_up:
				if hand.is_right: 
					if abs(hand.palm_normal.pitch * Leap.RAD_TO_DEG) < 90 and abs(hand.palm_normal.yaw * Leap.RAD_TO_DEG) < 20:
						print "I love you"
						lastWord = "love"
			if index_up and middle_up and ring_up and pinky_up and thumb_up:
				if hand.is_right: 
					if hand.palm_normal.pitch * Leap.RAD_TO_DEG <= 90 and hand.palm_normal.pitch * Leap.RAD_TO_DEG > 20 and abs(hand.palm_normal.yaw * Leap.RAD_TO_DEG) < 40:
						print "five" 

''' def very(frame):
	global lastWord
	for hand in frame.hands:
		TYPE_THUMB=0;
		TYPE_INDEX=TYPE_PROXIMAL=1
		TYPE_MIDDLE=TYPE_INTERMEDIATE=2
		TYPE_RING=TYPE_DISTAL=3
		TYPE_PINKY=4

		tip_ind = Leap.Vector(10000,1000,1000)
		knuck_ind = Leap.Vector(102,204,1283)
		tip_mid = Leap.Vector (123,33,22)
		knuck_mid = Leap.Vector(2,3,15)

		for finger in hand.fingers:

			if finger.type == TYPE_INDEX:
				for i in xrange(4):
					bone = finger.bone(i)
					if bone.type == TYPE_DISTAL:
						tip_ind = bone.direction
					if bone.type == TYPE_PROXIMAL:
						knuck_ind = bone.direction
					
			elif finger.type == TYPE_MIDDLE:
				for i in xrange(4):
					bone = finger.bone(i)
					if bone.type == TYPE_DISTAL:
						tip_mid = bone.direction
					if bone.type == TYPE_PROXIMAL:
						knuck_mid = bone.direction

			TIP_DIS = tip_ind - tip_mid
			KNUCK_DIS = knuck_ind - knuck_mid 

		if (TIP_DIS + KNUCK_DIS <= 0.2 or TIP_DIS + KNUCK_DIS >= -0.2):
			print "very" 
			lastWord = 'very'
''' 
'''
def but(frame):
	global lastWord
	for hand in frame.hands:
		handType = "LeftHand" if hand.is_left else "RightHand"

		leftworks = False
		rightworks = False

		for gesture in frame.gestures():
			if gesture.type == Leap.Gesture.TYPE_SWIPE:
				swipe = SwipeGesture(gesture)
				
				if handType == "LeftHand": 
						if (swipe.state != Leap.Gesture.STATE_START):
							if (swipe.direction.yaw * Leap.RAD_TO_DEG >= 30 and swipe.direction.yaw * Leap.RAD_TO_DEG <= 140 and swipe.direction.roll * Leap.RAD_TO_DEG >= 15 and swipe.direction.roll * Leap.RAD_TO_DEG <=180) == False: 
								print "LEFT yaw: " + str(swipe.direction.yaw * Leap.RAD_TO_DEG)
								print "LEFT roll: " + str(swipe.direction.roll * Leap.RAD_TO_DEG)
								leftworks = True
								print "LEFT OK" 

				elif handType == "RightHand":
						if (swipe.state != Leap.Gesture.STATE_START):
							if (swipe.direction.yaw * Leap.RAD_TO_DEG >= 30 and swipe.direction.yaw * Leap.RAD_TO_DEG <= 140 and swipe.direction.roll * Leap.RAD_TO_DEG >= 15 and swipe.direction.roll * Leap.RAD_TO_DEG <= 180) == True:
								print "RIGHT yaw: " + str(swipe.direction.yaw * Leap.RAD_TO_DEG)
								print "RIGHT ole: " + str(swipe.direction.roll * Leap.RAD_TO_DEG)
								rightworks = True 
								print "RIGHT OK" 

		
		if (rightworks and leftworks) == True: 
			print "but" 
			lastWord = 'but'						
'''
'''
def hello (frame):
	global lastWord 
	for hand in frame.hands: 
		question = 0
		for gesture in frame.gestures():
			if gesture.type == Leap.Gesture.TYPE_SWIPE:
				swipe = SwipeGesture(gesture) 

				if (swipe.state != Leap.Gesture.STATE_START):
					if (swipe.direction.yaw * Leap.RAD_TO_DEG >=5 and swipe.direction.yaw * Leap.RAD_TO_DEG <=70 and swipe.direction.pitch * Leap.RAD_TO_DEG >= 5 and swipe.direction.pitch * Leap.RAD_TO_DEG <=80) == True:
						print "hello"
						lastWord = 'hello'
					

def body (frame): 
	global lastWord 
	for hand in frame.hands: 
		handType = "LeftHand" if hand.is_left else "RightHand"

		wordleft = False 
		wordright = False 

		for gesture in frame.gestures():
			if handType == "LeftHand":
				if gesture.type == Leap.Gesture.TYPE_SWIPE: 
					swipe = SwipeGesture(gesture)
					if (swipe.state != Leap.Gesture.STATE_START):
						print str(swipe.direction.roll * Leap.RAD_TO_DEG) + " " + str(swipe.direction.pitch * Leap.RAD_TO_DEG)
						if (swipe.direction.roll * Leap.RAD_TO_DEG <= -100 and swipe.direction.roll * Leap.RAD_TO_DEG >= -180 and abs(swipe.direction.pitch * Leap.RAD_TO_DEG - 90) < 30 ) == True:
							wordleft = True 
							print "bodyleft" 

			if handType == "RightHand":
				if gesture.type == Leap.Gesture.TYPE_SWIPE: 
					swipe = SwipeGesture(gesture)
					if (swipe.state != Leap.Gesture.STATE_START):
						if (swipe.direction.roll * Leap.RAD_TO_DEG >= 100 and swipe.direction.roll * Leap.RAD_TO_DEG <= 180) == True:
							wordright = True 
							print "bodyright"
			
		if (wordright and wordleft) == True:
			print "body"
			lastWord = "body"
'''
def bye (frame):
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
'''
'''
 if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    #print "Swipe ID: " + str(swipe.id) + " State: " + self.state_names[gesture.state] + " Position: " + str(swipe.position) + " Direction:" + str(swipe.direction) + " Swipe: (mm/s): " + str(swipe.speed)
                    """
'''

class LeapMotionListener(Leap.Listener):
	finger_names = ['Thumb', 'Index', 'Middle','Ring','Pinky'];
	bone_names = ['Metacarpal', 'Proximal','Intermediate','Distal'];
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END'];

	def on_init(self, controller):
		print "initialized"

	def on_connect(self,controller):
		print "Motion Sensor Connected!"

		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self,controller):
		print "Motion Sensor Disconnected"

	def on_exit(self,controller):
		print "Exited"

	'''def on_frame(self,controller):
		frame = controller.frame()
		previous_sign = "something" 
		gesture_hands = []

		#print "Frame Id:  " + str(frame.id) + " Timestamp:  " + str(frame.timestamp) + " # of Hands  " + str(len(frame.hands)) + " # of fingers " + str(len(frame.fingers)) + " # of Tools  " + str(len(frame.tools)) + " # of GEstures" + str(len(frame.gestures())) 
	
		for hand in frame.hands:
			handType = "Left Hand" if hand.is_left else "Right Hand"
			#print " Hand ID: " + str (hand.id) + "Palm Position: " + str(hand.palm_position)

			normal = hand.palm_normal
			direction = hand.direction
			#print "Pitch: " + str(direction.pitch * leap.RAD_TO_DEG) + "Roll: " + str(normal.roll * leap.RAD_TO_DEG) + "Yaw: " + str(direction.yaw * leap.RAD_TO_DEG) 

			arm = hand.arm
			#print "Arm Direction: " + str(arm.direction) + "Wrist Position: " + str(arm.wrist_position) + "Elbow Position: " + str(arm.elbow_position) 

		for finger in hand.fingers:
			print "Type: " + self.finger_names[finger.type()] + "ID: " + str(finger.id) + "Length (mm): " + str(finger.length) + "Width (mm): " + str(finger.width) 
			
			for b in range(0,4):
				bone = finger.bone(b)
				print "Bone: " + self.bone_names[bone.type] + "Start: " + str(bone.prev_joint) + "End: " + str(bone.next_joint) + "Direction: " + str(bone.direction)
		for gesture in frame.gestures():
			if gesture.type == Leap.Gesture.TYPE_CIRCLE:
				circle = CircleGesture(gesture)

			if circle.pointable.direction.angle_to(circle.normal) <= Leap.pi/2:
				clockwiseness = "clockwise"
			else:
				clockwiseness = "counter-clockwise"

			swept_angle = 0
			if circle.state != Leap.Gesture.STATE_START:
				previous = CircleGesture(controller.frame(1).gesture(circle.id))
				swept_angle = (circle.progress - previous.progress) * 2 * LEAP.pi 
		'''

	def on_frame(self, controller):
		global lastWord
		# print lastWord
		frame = controller.frame()

		time.sleep(0.2)

		if lastWord != "love":
			love(frame)

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

if __name__=="__main__":
	main()