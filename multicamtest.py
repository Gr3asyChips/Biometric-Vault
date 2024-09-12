from button import ButtonHandler
from fc_rec import FacialRecognitionModule
from fc_reg import FacialRegistrationModule

from signal import pause
from time import sleep

fcrec = FacialRecognitionModule()
fcreg = FacialRegistrationModule
btn = ButtonHandler()

print("Ready")

# ~ while True:
	# ~ print(fcrec.online)
	# ~ if fcrec.online:
		# ~ btn.whenPressed(fcrec.stop)
	# ~ else:
		# ~ btn.whenPressed(fcrec.start)
	# ~ sleep(1)
	
while True:
	if fcrec.online:
		btn.whenPressed(fcrec.stop)
	else:
		btn.whenPressed(fcrec.start)
	sleep(1)
