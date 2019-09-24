# Extract Lecture Slides
From a video lecture, create a PDF of the lecture slides.

### Dependencies
* Python >= 3.5
* img2pdf (`pip install img2pdf`)
* OpenCV2 (`pip install opencv-python`)
* Numpy (`pip install numpy`)

### Usage
`python3 extract.py -h` or `python3 extract.py input.mp4` Script has options to change sensitivity and how often the script checks for a new slide (runs faster), change the parameters in the file's head.
