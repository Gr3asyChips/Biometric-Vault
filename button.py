from gpiozero import Button
from collections.abc import Callable
from time import sleep
from signal import pause		
	
class ButtonHandler:
	def __init__(self, onHold: Callable[[], None] = lambda: None, onPress: Callable[[], None] = lambda: None):
		Button.was_held = False

		self.btn = Button(12,
			bounce_time=0.01
		)

		def held(btn):
			btn.was_held = True
			onHold()

		def released(btn):
			if not btn.was_held:
				pressed()
			btn.was_held = False

		def pressed():
			onPress()
		
		self.btn.when_held = held
		self.btn.when_released = released
	
	def whenHeld(self, onHold: Callable[[], None]):
		def held(btn):
			btn.was_held = True
			onHold()
		
		self.btn.when_held = held
		
	def whenPressed(self, onPress: Callable[[], None]):
		def released(btn):
			if not btn.was_held:
				pressed()
			btn.was_held = False

		def pressed():
			onPress()
		
		self.btn.when_released = released
	
		
if __name__ == "__main__":
	def wakeUp():
		print("Please scan fingerprint.")
		
	def closeVault():
		print("Closing vault...")
		
	btn = ButtonHandler(
		onHold=lambda:None,
		onPress=wakeUp
	)
	
	sleep(10) # User has opened vault...
	
	btn.whenPressed(lambda:None)
	btn.whenHeld(closeVault)
	
	pause()


	
