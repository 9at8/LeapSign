import Leap,sys, thread, time 
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.Listener):
	finger_names = ['Thumb', 'Index', 'Middle','Ring','Pinky'];
	bone_names = ['Metacarpal', 'Proximal','Intermediate','Distal'];
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END'];

	def on_init(self, controller):
		print "initialized"

	def on_connect(self,controller):
		print "Motion Sensor Connected!"

		controller.enable_gesture(leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(leap.Gesture.TYPE_sWIPE);

	def on_disconnect(self,controller):
		print "Motion Sensor Disconnected"

	def on_exit(self,controller):
		print "Exited"

	def on_frame(self,controller):
		frame = controller.frame()

		print "Frame Id:  " + str(frame.id) \
		+ " Timestamp:  " + str(frame.timestamp) \
		+ " # of Hands  " + str(len(frame.hands)) \
		+ " # of fingers " + str(len(frame.fingers)) \
		+ " # of Tools  " + str(len(frame.tools)) \
		+ " # of GEstures" + str(len(frame.gestures()))
	
		for hand in frame.hands:
			handType = "Left Hand" if hand.is_left else "Right Hand"

			print " Hand ID: " + str (hand.id) + "Palm Position: " + str(hand.palm_position)

			normal = hand.palm_normal
			direction = hand.direction

			print "Pitch: " + str(direction.pitch * leap.RAD_TO_DEG) + "Roll: " + str(normal.roll * leap.RAD_TO_DEG) + "Yaw: " + str(direction.yaw * leap.RAD_TO_DEG) 

			arm = hand.arm
			print "Arm Direction: " + str(arm.direction) + "Wrist Position: " + str(arm.wrist_position) + "Elbow Position: " + str(arm.elbow_position) 

		for finger in hand.fingers:
			print "Type: " + self.finger_names[finger.type()] + "ID: " + str(finger.id) + "Length (mm): " + str(finger.length) + "Width (mm): " + str(finger.width) 
			
			for b in range(0,4):
				bone = finger.bone(b)
				print "Bone: " + self.bone_names[bone.type] + "Start: " + str(bone.prev_joint) + "End: " + str(bone.next_joint) + "Direction: " + str(bone.direction)

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