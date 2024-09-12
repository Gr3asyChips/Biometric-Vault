import cv2
import pathlib

class FacialRegistrationModule:
	def __init__(self):
		super().__init__()
		pathlib.Path("images/db/user").mkdir(parents=True, exist_ok=True)
		self.img_dir = str(pathlib.Path("images").resolve())
		self.is_fc_rec = False
		self.is_fc_stop = False
		
	def start(self, reg_no: int = 5):
		num = 1
		cap = cv2.VideoCapture(0)

		while True:
			ret, img = cap.read()
			cv2.imshow("Frame", img)
			if cv2.waitKey(1) & 0xFF == ord("c"):
				cv2.imwrite(f"{self.img_dir}/db/user/{str(num)}.jpg", img)
				print(f"Capture no.{str(num)} successful!")
				num += 1
			if num==reg_no+1:
				break
		cap.release()
		cv2.destroyAllWindows()

if __name__ == "__main__":
	fr = FacialRegistrationModule()
	fr.start(1)
