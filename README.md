# zoom_enhance
**a graphic user interface for creating algorithmic art**

![Zoom Example](example_images/zoom-example.jpg)

## About
Zoom Enhance is a program for creating algorithmic art and losing yourself in the process. Zoom into a unique image as much as you want and save your favorite views. The zoom buttons let you navigate the picture, and will magnify whichever portion you want to see closer. A toggle allows to either display the picture in full color space, or threshold the picture to 8 colors. Different output resolutions from 10x10px to 2560x2560px are supported, with 1080px being the default.

![Thresholding](example_images/thresholding-example.jpg)

## How to Run
**Option A - Quick & Simple (recommended for most users)**
1. Download the file zoom_enhance.exe from [my website](https://fabiandietrich.com/static/code/zoom_enhance.exe) (it is 27MB which is more than Github allows)
2. Run the file (on Windows). To run the program this way, you do not need python or other dependencies installed. Depending on your antivirus software, you might get a warning when trying to run the file. If you don't trust the .exe, you can also run the program by following Option B below
3. Note that when using the program, you need to set an image save folder with the corresponding button before saving an image

**Option B - Custom**
1. Clone the repository
2. Make sure you have the following modules installed:
	- opencv-python
	- pillow
	- numpy
	- tkinter
3. Run zoom_enhance.py (requires Python 3)

## Inspiration
I experimented for a long time writing and using different Python scripts to create algorithmic art. Eventually, I wanted a more intuitive graphic user interface to be able to better direct my program. When creating abstract images based on a seed, the zoom factor can usually be chosen (almost) arbitrarily. As a Bladerunner fan, I remembered the iconic [enhance scene](https://www.youtube.com/watch?v=hHwjceFcF2Q), in which Harrison Ford is able to retrieve visual information from the depths of an endlessly magnified picture.

![Zoom Enhance Start Screen](example_images/start-screen.jpg)

## Credit
Some of the code for image generation is from Nathan Reed's post ['Generating Abstract Images with Random Functions'](http://reedbeta.com/blog/generating-abstract-images-with-random-functions/).
