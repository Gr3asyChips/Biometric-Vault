from time import sleep
from signal import pause	
from gpiozero import Motor, Button, Servo
    
class OldMotorsController:
	def __init__(self, 
		in1: int = 10, # GPIO
		in2: int = 22, # GPIO	
		in3: int = 27, # GPIO
		in4: int = 17, # GPIO
		ena: int = 9, # GPIO
		enb: int = 4, # GPIO		
		door_max: int = 6, # GPIO
		door_min: int = 13, # GPIO
		lock_max: int = 19, # GPIO
		lock_min: int = 26, # GPIO
		
		
	):
	
		self.lock_motor = Motor(
			forward=in1,
			backward=in2,
			enable=ena
		)
		self.door_motor = Motor(
			forward=in3,
			backward=in4,
			enable=enb
		)
		self.door_max = Button(door_max)
		self.door_min = Button(door_min)
		self.lock_max = Button(lock_max)
		self.lock_min = Button(lock_min)		

	def openVault(self):
		# unlock
		self.lock_motor.backward()	
#		self.lock_min.wait_for_press(timeout=1.0)
		sleep(1)		
		self.lock_motor.stop()
		sleep(1)
		# open
		self.door_motor.forward()	
#		self.door_max.wait_for_press(timeout=1.0)
		sleep(1)		
		self.door_motor.stop()
		
	def closeVault(self):
		# close
		self.door_motor.backward()	
#		self.door_min.wait_for_press(timeout=1.0)
		sleep(1)		
		self.door_motor.stop() 
		sleep(1)	
		# lock
		self.lock_motor.forward()	
#		self.lock_max.wait_for_press(timeout=1.0)
		sleep(1)		
		self.lock_motor.stop()	
	

class MotorsController:
	def __init__(self, 
		in1: int = 10, # GPIO
		in2: int = 22, # GPIO	
		servo: int = 5, # GPIO
		ena: int = 9, # GPIO		
		door_max: int = 6, # GPIO
		door_min: int = 13, # GPIO
		
	):	
		self.lock_servo = Servo(servo)
		self.door_motor = Motor(
			forward=in1,
			backward=in2,
			enable=ena
		)
		self.door_max = Button(door_max)
		self.door_min = Button(door_min)
		
	def openVault(self):
		print("Unlocking...")		
		self.lock_servo.min()
		print("Unlocked")
		sleep(0.5)
		self.door_motor.forward()
		print("Opening vault...")
		self.door_max.wait_for_release()
		self.door_motor.stop()
		print("Vault opened")
		
	def closeVault(self):	
		print("Closing vault...")
		self.door_motor.backward()
		self.door_min.wait_for_release()
		self.door_motor.stop()	
		print("Vault closed")
		sleep(0.5)
		print("Locking")
		self.lock_servo.max()
		print("Locked")
		
if __name__ == "__main__":
	motors = MotorsController()
	motors.openVault() # blocking
	sleep(1)
	motors.closeVault() # blocking 
	
	# ~ motors = MotorsController()
	# ~ motors.lock_motor.forward()
	# ~ motors.door_max.wait_for_release()
	# ~ print("F done")
	# ~ motors.lock_motor.backward()
	# ~ motors.door_min.wait_for_press()
	# ~ print("B done")
	# ~ motors.lock_motor.stop()

	
#	motor = Motor(
#		forward=4,
#		backward=17,
#		enable=13
#	)
#	motor.forward()
#	sleep(3)
#	motor.stop()

