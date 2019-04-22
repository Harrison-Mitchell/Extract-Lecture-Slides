from img2pdf import convert as pdf
import cv2
from os import listdir, remove, mkdir
from shutil import rmtree
from numpy import mean
from numpy import sum as s

THRESHOLD = 50 # Higher = More sentitive
EVERY_SECONDS = 2
IN_LAST_SECONDS = 4 # How many seconds to compare with
NUM_LAST_SECONDS = 1 # how many we've save in the last ^ seconds to avoid saving the frame
# I.E if IN = 5, NUM = 0: If we haven't saved any frames in the last 5 seconds, save this one 

try: rmtree("frames")
except: pass # Cleanup
try: remove("slides.pdf")
except: pass
mkdir("frames")

vidcap = cv2.VideoCapture(input("File: "))
count = 0
triggers = []
success = True
fps = int(vidcap.get(cv2.CAP_PROP_FPS))
width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
threshold = THRESHOLD * (width * height) # Changes compared to size of video frame
__, lastIm = vidcap.read() # Read the first frame

while success: # While we've still got frames
	success, image = vidcap.read()
	if count % (EVERY_SECONDS * fps) == 0: # Only check for a new slide every X seconds
		print('Processing [%d%%]\r'%round(count/length*100), end="") # Print progress
		# If the pixel difference between this and the last frame surpasses our threshold and recency rules
		if abs(s(image - lastIm)) > threshold and sum(triggers[-IN_LAST_SECONDS:]) < NUM_LAST_SECONDS:
			cv2.imwrite('frames/frame%07d.jpg'%count,image) # Save the frame
			triggers.append(1) # And record that we saved it (for recency validation)
		else:
			triggers.append(0)
		lastIm = image
	count += 1

with open("slides.pdf", "wb") as f:
    f.write(pdf(["frames/" + s for s in sorted(listdir("frames/"))]))
