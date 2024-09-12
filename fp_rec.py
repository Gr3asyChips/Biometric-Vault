#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Originally a Bastian Raschke Example 
Modified by Tim for GPIO LED Control

"""

import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

from time import sleep



# ~ ## Tries to initialize the sensor
# ~ try:
    # ~ f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

    # ~ if ( f.verifyPassword() == False ):
        # ~ raise ValueError('The given fingerprint sensor password is wrong!')

# ~ except Exception as e:
    # ~ print('The fingerprint sensor could not be initialized!')
    # ~ print('Exception message: ' + str(e))
    # ~ exit(1)

# ~ ## Gets some sensor information
# ~ print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

# ~ ## Tries to search the finger and calculate hash
# ~ try:
    # ~ print('Waiting for finger...')

    # ~ ## Wait that finger is read
    # ~ while ( f.readImage() == False ):
        # ~ pass

    # ~ ## Converts read image to characteristics and stores it in charbuffer 1
    # ~ f.convertImage(FINGERPRINT_CHARBUFFER1)

    # ~ ## Searchs template
    # ~ result = f.searchTemplate()

    # ~ positionNumber = result[0]
    # ~ accuracyScore = result[1]

    # ~ if ( positionNumber == -1 ):
        # ~ print('No match found!')
        # ~ exit(0)  

# ~ #This Else statement is only reached when an Index Finger is Detected
    # ~ else:
        # ~ print('Found template at position #' + str(positionNumber))
        # ~ print('The accuracy score is: ' + str(accuracyScore))

# ~ #Because we have reached this else statement we had detected an enrolled finger
# ~ #This means we can now toggle the LED. This is done with the three lines below.
       

    # ~ ## OPTIONAL stuff
    # ~ ##

    # ~ ## Loads the found template to charbuffer 1
    # ~ f.loadTemplate(positionNumber, FINGERPRINT_CHARBUFFER1)

    # ~ ## Downloads the characteristics of template loaded in charbuffer 1
    # ~ characterics = str(f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)).encode('utf-8')

    # ~ ## Hashes characteristics of template
    # ~ print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

# ~ except Exception as e:
    # ~ print('Operation failed!')
    # ~ print('Exception message: ' + str(e))
    # ~ exit(1)
    
class FingerprintRecognitionModule:
	def __init__(self):
		super().__init__()
		self.f = None
		self.turnOn = False
		try:
			self.f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

			if self.f.verifyPassword() == False:
				raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
			print('The fingerprint sensor could not be initialized!')
			print('Exception message: ' + str(e))
		
		# ~ print('Currently used templates: ' + str(self.f.getTemplateCount()) +'/'+ str(self.f.getStorageCapacity()))
		
	
	def get_fingerprint(self):
		if self.f.readImage():
			## Converts read image to characteristics and stores it in charbuffer 1
			self.f.convertImage(FINGERPRINT_CHARBUFFER1)

			## Searchs template
			result = self.f.searchTemplate()

			positionNumber = result[0]
			accuracyScore = result[1]
			
			if positionNumber != -1:
				print('Found template at position #' + str(positionNumber))
				print('The accuracy score is: ' + str(accuracyScore))
				return True
			else:				
				print('No match found!')	
				return False
		else:
			print("No finger found.")	
			return False    
	def register_fingerprint(self):
		# Tries to enroll new finger
		self.turnOn = True
		try:
			print('Waiting for finger...')

			## Wait that finger is read
			while self.f.readImage() == False:
				if not self.turnOn:
					return

			## Converts read image to characteristics and stores it in charbuffer 1
			self.f.convertImage(FINGERPRINT_CHARBUFFER1)

			## Checks if finger is already enrolled
			result = self.f.searchTemplate()
			positionNumber = result[0]

			if ( positionNumber >= 0 ):
				print('Template already exists at position #' + str(positionNumber))
				exit(0)

			print('Remove finger...')
			sleep(2)

			print('Waiting for same finger again...')

			## Wait that finger is read again
			while self.f.readImage() == False:
				if not self.turnOn:
					return


			## Converts read image to characteristics and stores it in charbuffer 2
			self.f.convertImage(FINGERPRINT_CHARBUFFER2)

			## Compares the charbuffers
			if ( self.f.compareCharacteristics() == 0 ):
				raise Exception('Fingers do not match')

			## Creates a template
			self.f.createTemplate()
			self.f.turnOn = False

			## Saves template at new position number
			positionNumber = self.f.storeTemplate()
			print('Finger enrolled successfully!')
			print('New template position #' + str(positionNumber))

		except Exception as e:
			print('Operation failed!')
			print('Exception message: ' + str(e))
		
            
if __name__ == "__main__":
	fp =  FingerprintRecognitionModule()
	fp.register_fingerprint()
	for i in range(5):
			print(str(5-i))
			sleep(1)
	if fp.get_fingerprint():
		print("success")
	else:
		print("fail")
