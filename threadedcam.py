import cv2
import threading 
import time

from button import ButtonHandler

class ThreadedCamera:
    
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.terminate_camera_thread = threading.Event()
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()
    
    def update(self):
        while not self.terminate_camera_thread.is_set():
            if self.capture.isOpened():
               (self.status, self.frame) = self.capture.read()
               cv2.imshow("output", self.frame)
               waitkey(1)

    def shutdown(self):
        self.terminate_camera_thread.set()
        self.capture.release()
        cv2.destroyAllWindows()
        
    def __enter__(self):
		return self

	def __exit__(self, *args, **kwargs):
		self.shutdown()

if __name__ == "__main__":
	btn = ButtonHandler()
	with ThreadedCamera() as camera:
		while True:
			
			
		
