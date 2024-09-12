from time import sleep
from gpiozero import RGBLED
    
class LEDController:
	def __init__(self, redPin: int = 23, greenPin: int = 24, bluePin: int= 25):		
		self.led = RGBLED(red=redPin, green=greenPin, blue=bluePin)
		self.turnOff()
		
	def turnOff(self):
		self.led.color = (1, 1, 1) 
		
	def red(self):
		self.led.color = (0, 1, 1) 

	def green(self):
		self.led.color = (1, 0, 1) 
		
	def yellow(self):
		self.led.color = (0, 0, 1) 

	def blue(self):
		self.led.color = (1, 1, 0) 
	
	def turnOnSeq(self):
		self.red()
		sleep(1)
		self.yellow()
		sleep(1)
		self.green()
		sleep(1)    
		self.blue()
		sleep(1)
		self.turnOff()
		
 
if __name__ == "__main__":    
	led = LEDController()
	# ~ led.red()
	# ~ sleep(1)
	# ~ led.yellow()
	# ~ sleep(1)
	# ~ led.green()
	# ~ sleep(1)    
	# ~ led.blue()
	# ~ sleep(1)
	# ~ led.turnOff()
	led.turnOnSeq()
	
	
    
  
