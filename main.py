from button import ButtonHandler
from fc_rec import FacialRecognitionModule
from fp_rec import FingerprintRecognitionModule
from led import LEDController
from motors import OldMotorsController

from transitions import Machine
from signal import pause
from time import sleep

class Vault(object):
	states = [
		"closed",
		"detecting",
		"opening",
		"opened",
		"closing",
		"registering face",
		"register face?",
		"register fingerprint?",
		"registering fingerprint"
	]
	
	def __init__ (self):
		
		self.btn = ButtonHandler()
		self.fcrec =  FacialRecognitionModule()
		self.fprec =  FingerprintRecognitionModule()
		self.led = LEDController()
		self.motors = OldMotorsController()
		
		self.machine = Machine(
			model=self, 
			states=Vault.states,
			initial="closed"
		)
		
		self.machine.add_transition(
			trigger="wake_up",
			source="closed",
			dest="detecting",
			after="startValidation",
		)
		
		self.machine.add_transition(
			trigger="open_vault",
			source="detecting",
			dest="opening",
			after="openVault"			
		)
		
		self.machine.add_transition(
			trigger="welcome_user",
			source="opening",
			dest="opened",
			after="openedMode"
		)
		
		self.machine.add_transition(
			trigger="switch_to_fc_reg",
			source="opened",
			dest="register face?",
			after="fcMode"
		)
		
		self.machine.add_transition(
			trigger="switch_to_fp_reg",
			source="register face?",
			dest="register fingerprint?",
			after="fpMode"
		)
		
		self.machine.add_transition(
			trigger="switch_to_opened",
			source="register fingerprint?",
			dest="opened",
			after="openedMode"
		)
		
		self.machine.add_transition(
			trigger="start_fc_reg",
			source="register face?",
			dest="registering face",
			after="startFCReg"
		)
		
		self.machine.add_transition(
			trigger="stop_fc_reg",
			source="registering face",
			dest="opened",
			after="openedMode"
		)
		
		self.machine.add_transition(
			trigger="start_fp_reg",
			source="register fingerprint?",
			dest="registering fingerprint",
			after="startFPReg"
		)
		
		self.machine.add_transition(
			trigger="stop_fp_reg",
			source="registering fingerprint",
			dest="opened",
			after="openedMode"
		)
		
		self.machine.add_transition(
			trigger="close_vault",
			source="opened",
			dest="closing",
			after="closeVault"
		)
		
		self.machine.add_transition(
			trigger="to_sleep",
			source="closing",
			dest="closed",
			after="toSleep"	
		)
	
	# Done
	def startValidation(self):
		print("Starting vaildation...")		
		self.led.turnOnSeq()
		self.btn.whenPressed(lambda: None)
		self.btn.whenHeld(lambda: None)
		# High threshold used for debugging
		self.fcrec.start(0.7)
		# ~ while not self.fcrec.is_fc_rec:	
			# ~ sleep(0.5)
		while True:
			if self.fcrec.is_fc_rec:
				if self.fprec.get_fingerprint():
					break
			sleep(0.5)
		self.fcrec.stop()
		self.led.green()
		sleep(1)
		vault.open_vault()
	
	# Done
	def openVault(self):
		print("Opening vault...")
		self.btn.whenPressed(lambda: None)
		self.btn.whenHeld(lambda: None)
		self.motors.openVault()
		vault.welcome_user()
	
	# Done
	def closeVault(self):
		print("Closing vault...")
		self.btn.whenPressed(lambda: None)
		self.btn.whenHeld(lambda: None)
		self.led.turnOff()
		self.motors.closeVault()		
		vault.to_sleep()
	
	# Done
	def toSleep(self):
		print("Sleeping...")
		self.btn.whenPressed(vault.wake_up)
		self.btn.whenHeld(vault.wake_up)
	
	# Done
	def openedMode(self):
		print("Hello user! Press - switch to face registration. Hold - close vault")
		self.led.green()
		self.btn.whenPressed(vault.switch_to_fc_reg)
		self.btn.whenHeld(vault.close_vault)
	# Done
	def fcMode(self):
		print("Register face? Press - no, switch to fingerprint registration. Hold - yes")
		self.led.yellow()
		self.btn.whenPressed(vault.switch_to_fp_reg)
		self.btn.whenHeld(vault.start_fc_reg)
	# Done
	def fpMode(self):
		print("Register fingerprint? Press - no, go to main menu. Hold - yes")
		self.led.blue()
		self.btn.whenPressed(vault.switch_to_opened)
		self.btn.whenHeld(vault.start_fp_reg)
	
	# Done
	def startFCReg(self):
		def takePhoto():
			self.led.turnOff()
			self.fcrec.take_photo()
			print("Face registered successfully.")
			vault.stop_fc_reg()
		def cancel():
			self.led.turnOff()
			print("Cancelled face registration.")
			vault.stop_fc_reg()
		print("Take a photo of your face by pressing the button. Hold to cancel.")
		
		self.btn.whenPressed(takePhoto)
		self.btn.whenHeld(cancel)
	
	# TODO
	def startFPReg(self):
		def cancel():
			self.led.turnOff()
			self.fprec.turnOn = False
			print("Cancelled face registration.")
			vault.stop_fp_reg()
		self.btn.whenPressed(lambda: None)
		self.btn.whenHeld(cancel)
		print("Place finger on the scanner. Hold to cancel.")
		self.led.turnOff()
		self.fprec.register_fingerprint()
		print("Fingerprint registered successfully.")
		vault.stop_fp_reg()		
		
		

if __name__ == "__main__":
	vault = Vault()	
	
	vault.btn.whenPressed(vault.wake_up)
	vault.btn.whenHeld(vault.wake_up)
	
	pause()
	# ~ try:
		# ~ pause()
	# ~ except Exception:
		# ~ vault.led.red()
		# ~ raise(Exception)
	
