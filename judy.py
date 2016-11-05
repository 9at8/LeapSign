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

			if index_up and not middle_up and not ring_up and pinky_up and thumb_up:
				print "I love you"
				lastWord = "love"

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