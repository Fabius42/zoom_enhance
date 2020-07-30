# GENERATIVE VIDEO
# creates zooming video of generative art
# with variable amount of frames and custom seed

import numpy as np, optparse, random, time
from PIL import Image
import subprocess



# function generativeImg
# creates generative art depending on seed
# can be scaled by providing two point tupels in (x,y) format
# (normal values: 0.0, 1.0, max. around -200.0, 300.0)
def generative_img(seed, outputPath, dX, dY, x, y):
	# specify seed
	random.seed(seed)

	# Generate x and y images, with 3D shape so operations will correctly broadcast.
	xArray = np.linspace(x[1], y[1], dX).reshape((1, dX, 1))
	yArray = np.linspace(x[0], y[0], dY).reshape((dY, 1, 1))

	# Adaptor functions for the recursive generator
	# Note: using python's random module because numpy's doesn't handle seeds longer than 32 bits.
	def randColor(): return np.array([random.random(), random.random(), random.random()]).reshape((1, 1, 3))
	def xVar(): return xArray
	def yVar(): return yArray
	def safeDivide(a, b): return np.divide(a, np.maximum(b, 0.001))

	# Recursively build an image using a random function.  Functions are built as a parse tree top-down,
	# with each node chosen randomly from the following list.  The first element in each tuple is the
	# number of required recursive calls and the second element is the function to evaluate the result.
	functions = (
			(0, randColor),
			(0, xVar),
			(0, yVar),
			(1, np.sin),
			(1, np.cos),
			(2, np.add),
			(2, np.subtract),
			(2, np.multiply),
			(2, safeDivide),
		)

	depthMin = 2
	depthMax = 10

	def buildImg(depth = 0):
		funcs = [f for f in functions if
					(f[0] > 0 and depth < depthMax) or
					(f[0] == 0 and depth >= depthMin)]
		nArgs, func = random.choice(funcs)
		args = [buildImg(depth + 1) for n in range(nArgs)]
		return func(*args)

	img = buildImg()

	# Ensure it has the right dimensions
	try:
		img = np.tile(img, (dX / img.shape[0], dY / img.shape[1], 3 / img.shape[2]))
	except:
		TypeError

	# Convert to 8-bit, send to PIL and save
	img8Bit = np.uint8(np.rint(img.clip(0.0, 1.0) * 255.0))
	try:
		Image.fromarray(img8Bit).save(outputPath)
	except:
		TypeError


# function make9Grid
# returns list with 9 x,y tupels (x,y)
# which correspond to an 3x3 grid division
# of the input numbers
def make9Grid(x, y):
    # get total size of grid
    originX = x[0]
    originY = x[1]
    deltaX = y[0] - x[0]
    deltaY = y[1] - x[1]
    newX = deltaX / 3
    newY = deltaY / 3
    # create return list
    xTemp = originX
    yTemp = originY
    retList = []
    for i in range(3):
        xTemp = originX + newX * i
        for j in range(3):
            yTemp = originY + newY * j
            retList.append([(round(xTemp, 16), round(yTemp, 16)), (round(xTemp + newX, 16), round(yTemp + newY, 16))])
    return retList



# function make_zoom_out_coordinates
# returns list with two coordinate tupels
# which are the zoomed out boundary box from
# the inputted x,y coordinates
def make_zoom_out_coordinates(x, y):
	# get dimension of zoomed-out picture
	delta = y[0] - x[0]
	# return zoomed-out coordinates
	return ((x[0] - delta, x[1] - delta), (y[0] +  delta, y[1] + delta))


# function make_move_coordinates
# returns list with 4 coordinate tupels
# 0 = north, 1 = east, 2 = south, 3 = west
def make_move_coordinates(x, y):
	# get dimension of zoomed-out picture
	delta = (y[0] - x[0]) / 3 * 2
	# set coordinates of 4 directions
	north = ((x[0] - delta, x[1]), (y[0] - delta, y[1]))
	east = ((x[0], x[1] + delta), (y[0], y[1] + delta))
	south = ((x[0] + delta, x[1]), (y[0] + delta, y[1]))
	west = ((x[0], x[1] - delta), (y[0], y[1] - delta))
	# return coordinates
	return [north, east, south, west]





"""
# TODO:
# Implement move
# Implement zoom-out
# 1. Add new buttons
#    U
#  L Z R
#	 D
# 2. add functions for the buttons using the new zoom information for image generation
"""

