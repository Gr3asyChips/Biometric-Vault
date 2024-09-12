#Broken
import cv2
import pathlib
from time import sleep
# ~ import pandas as pd
import os
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
# ~ from tqdm import tqdm
from types import MethodType
from threading import Thread, Event
from collections import deque
from signal import pause

"""
Credit:
- https://stackoverflow.com/questions/58592291/how-to-capture-multiple-camera-streams-with-opencv
- https://kean-chan.medium.com/real-time-facial-recognition-with-pytorch-facenet-ca3f6a510816
"""

class FacialRecognitionModule:
	def __init__(self):
		super().__init__()
		pathlib.Path("images/db/user").mkdir(parents=True, exist_ok=True)
		self.img_dir = str(pathlib.Path("images").resolve())
		
		self.online = False
		self.turnOn = False
		self.capture = None
		self.is_fc_rec = False  
		self.threshold = 0.5
		
		self.load_network_stream()
		self.fc_rec_thread = Thread(target=self.fc_rec, args=())
		self.fc_rec_thread.daemon = True
		self.fc_rec_thread.start()
		
	def load_network_stream(self):
		"""Verifies stream link and open new stream if valid"""

		def load_network_stream_thread():
			if self.verify_network_stream():
				self.capture = cv2.VideoCapture(0)
				self.online = True
				print("capture set")
		self.load_stream_thread = Thread(target=load_network_stream_thread, args=())
		self.load_stream_thread.daemon = True
		self.load_stream_thread.start()
        
	def verify_network_stream(self):
		"""Attempts to receive a frame from given link"""

		cap = cv2.VideoCapture(0)
		if not cap.isOpened():
			return False
		cap.release()
		return True
	
	def take_photo(self):
		if not self.turnOn:
			status, frame = self.capture.read()
			cv2.imwrite(f"{self.img_dir}/db/user/user.jpg", frame)
			print("Face registered successfully.")
	
	def fc_rec(self):
		try:
			"""Reads frame, resizes, and converts image to pixmap"""	
			
			def encode(img):		
				res = resnet(torch.Tensor(img))
				return res	
				
			def detect_box(self, img, save_path=None):
				# Detect faces
				batch_boxes, batch_probs, batch_points = self.detect(img, landmarks=True)
				# Select faces
				if not self.keep_all:
					batch_boxes, batch_probs, batch_points = self.select_boxes(
						batch_boxes, batch_probs, batch_points, img, method=self.selection_method
					)
				# Extract faces
				faces = self.extract(img, batch_boxes, save_path)
				return batch_boxes, faces
			
			resnet = InceptionResnetV1(pretrained='casia-webface').eval()
			
			mtcnn = MTCNN(
				image_size=224, keep_all=True, thresholds=[0.4, 0.5, 0.5], min_face_size=60
			)
			mtcnn.detect_box = MethodType(detect_box, mtcnn)		
			
			saved_pictures = "./images/db/user/"
			all_people_faces = {}
			
			while True:
				if self.turnOn:
					print("Encoding Features")
					for file in os.listdir(saved_pictures):
						person_face, _ = os.path.splitext(file)
						img = cv2.imread(f'{saved_pictures}/{person_face}.jpg')
						cropped = mtcnn(img)
						if cropped is not None:
							all_people_faces[person_face] = encode(cropped)[0, :]
						print(f"{person_face} encoded")				
					print("Detecting face...")
					
					while self.turnOn:
						status, frame = self.capture.read()
						if not status: # BUG: /dev/video0 disappears
							break
						batch_boxes, cropped_images = mtcnn.detect_box(frame)
						# ~ print("read frame")
						if cropped_images is not None:
							for box, cropped in zip(batch_boxes, cropped_images):
								x, y, x2, y2 = [int(x) for x in box]
								img_embedding = encode(cropped.unsqueeze(0))
								detect_dict = {}
								for k, v in all_people_faces.items():
									detect_dict[k] = (v - img_embedding).norm().item()
								min_key = min(detect_dict, key=detect_dict.get)
								print(detect_dict[min_key], str(self.is_fc_rec))

								if detect_dict[min_key] >= self.threshold:
									min_key = 'Undetected'
									self.is_fc_rec = False
								else:
									self.is_fc_rec = True
								
								# ~ cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
								# ~ cv2.putText(
								  # ~ frame, min_key, (x + 5, y + 10), 
								   # ~ cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
		except Exception:
			raise(Exception)
	def set_frame(self):
		if not self.online:
			sleep(1)
			return

		if self.deque and self.online:
			# Grab latest frame
			frame = self.deque[-1]
			cv2.imshow("output", frame)
			cv2.waitKey(1)
	
	def start(self, threshold: float = 0.5):
		try:
			if threshold < 0:
				raise ValueError
			self.threshold = threshold
			self.turnOn = True
			self.is_fc_rec = False
			
		except ValueError:
			print("Invalid threshold. Value must be a non-negative number.")
			
	
	def stop(self):
		self.turnOn = False        
            
if __name__ == "__main__":
	fr =  FacialRecognitionModule()
	while True:
		fr.start()
		while not fr.is_fc_rec:	
			sleep(0.5)
			# print(".")
			pass
		fr.stop()
		for i in range(5):
			print(str(i))
			sleep(1)

		

	
	
		
	
