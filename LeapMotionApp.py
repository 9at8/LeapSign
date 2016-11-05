import Leap,sys, thread, time 
from Leap import circleGesture,KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.listener):
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
		pass 

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