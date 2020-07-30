from tkinter import *
from tkinter import ttk, filedialog
from functools import partial
from PIL import ImageTk, Image, ImageDraw, ImageOps
from image_util import generative_img, make9Grid
import cv2
import random
import time
import os


def main():
    # set start variables
    path = ""
    displayPath = ""
    seed = 0.0001
    resolution = 800
    output_resolution = 800
    zoom = ((0,0), (333,333))

    # set state
    writeState("output_path", "output_images")
    writeState("current_seed", "0.0001")
    writeState("output_resolution", "1080")


    # function zoom
    # writes zoom_choice to file, calls zoom_image
    def zoom(counter):
        writeState("zoom_choice", str(counter))
        zoom_image()


    # function zoom_image
    # similar to new_image, but with specified values
    # creates image based on current zoom factor from current seed
    # if gridChange is True, it doesnt zoom in but keeps the current position
    def zoom_image(gridChange=False):
        # retrieve state
        seed = float(readState("current_seed"))
        zoom = getZoom()
        if gridChange:
            zoomSelected = zoom
        else:
            zoomChoice = int(readState("zoom_choice")) # choice of pressed button (0-8)
            zoomGrid = make9Grid(zoom[0], zoom[1]) # make 9 zoom options
            zoomSelected = zoomGrid[zoomChoice]
        # create zoomed image
        generative_img(seed, "temp_images/temp_img.png", resolution, resolution, zoomSelected[0], zoomSelected[1])
        # threshold image
        if threshold_state.get():
            threshold("temp_images/temp_img.png")
        # add grid on top of it
        if grid_state.get():
            drawLineGrid()
        # update image label
        tempImg = Image.open("temp_images/temp_img.png")
        tempImg = ImageTk.PhotoImage(tempImg)
        zoomImg.image = tempImg
        zoomImg.configure(image=tempImg)
        # update zoom factor
        setZoom(zoomSelected)


    # function make_button
    # creates buttons based on letters and numbers
    # returns the created button
    def make_button(button_frame, buttonLetter, buttonNumber, counter):
        button = Button(button_frame, text=buttonLetter+buttonNumber, bg="black", fg="white", font=("Arial", 10), command=partial(zoom, counter))
        if buttonLetter == 'A':
            row = 0
        elif buttonLetter == 'B':
            row = 1
        elif buttonLetter == 'C':
            row = 2
        if buttonNumber == '1':
            column = 0
        elif buttonNumber == '2':
            column = 1
        elif buttonNumber == '3':
            column = 2
        button.grid(row=row, column=column)
        return button


    # function get_directory
    # updates path for image saving and writes it to state
    def get_directory():
        path = filedialog.askdirectory()
        writeState("output_path", path)
        if len(path) > 35:
            displayPath = "..." + path[len(path)-35:len(path)]
        else:
            displayPath = path
        lfile.configure(text="Folder: " + str(displayPath))

    # function resetZoom
    def resetZoom():    
        writeState("zoomX1", "0")
        writeState("zoomX2", "0")
        writeState("zoomY1", "9")
        writeState("zoomY2", "9")

    resetZoom()
    
    # function getZoom
    # reads and returns zoom values
    def getZoom():
        zoomX1 = float(readState("zoomX1"))
        zoomX2 = float(readState("zoomX2"))
        zoomY1 = float(readState("zoomY1"))
        zoomY2 = float(readState("zoomY2"))
        return ((zoomX1, zoomX2), (zoomY1, zoomY2))

    
    # function setZoom
    # writes zoom state based on inputted zoom value
    def setZoom(zoom):
        writeState("zoomX1", str(zoom[0][0]))
        writeState("zoomX2", str(zoom[0][1]))
        writeState("zoomY1", str(zoom[1][0]))
        writeState("zoomY2", str(zoom[1][1]))
    

    # function new_image
    # creates new images with random seed
    def new_image():
        # create and assign new seed
        seed = random.randrange(10000, 1000000) / 10000
        writeState("current_seed", str(seed))
        # reset and get zoom
        resetZoom()
        zoom = getZoom()
        # create random image
        generative_img(seed, "temp_images/temp_img.png", resolution, resolution, zoom[0], zoom[1])

        # if seed is defective and produces one-line images, retry with new seed
        while not check_size():
            # create and assign new seed
            seed = random.randrange(10000, 1000000) / 10000
            writeState("current_seed", str(seed))
            generative_img(seed, "temp_images/temp_img.png", resolution, resolution, zoom[0], zoom[1])

        # threshold image
        if threshold_state.get():
            threshold("temp_images/temp_img.png")
        # add grid on top of it
        if grid_state.get():
            drawLineGrid()
        # update seed label
        lseed.configure(text="Current Seed: " + str(seed))
        # update image label
        tempImg = Image.open("temp_images/temp_img.png")
        tempImg = ImageTk.PhotoImage(tempImg)
        zoomImg.image = tempImg
        zoomImg.configure(image=tempImg)
        
    
    # function check_size
    # returns False if image is smaller than 5 kilobytes
    def check_size():
        size = os.stat("temp_images/temp_img.png").st_size
        if size > 5000:
            return True
        else:
            return False


    # function save_image
    # saves image to specified filepath
    def save_image():
        # create image with target resolution and zoom level and save it
        seed = float(readState("current_seed"))
        path = readState("output_path")
        zoom = getZoom()
        resolution = int(readState("output_resolution"))
        generative_img(seed, path + "/" + str(seed) + ".png", resolution, resolution, zoom[0], zoom[1])
        # threshold image
        if threshold_state.get():
            threshold("temp_images/temp_img.png")


    # function set_resolution
    # writes selected resolution to file
    def set_resolution():
        writeState("output_resolution", str(output_resolution.get()))

    
    # ===== LAYOUT SECTION =====

    # create window with title and size
    window = Tk()
    window.title("zoom_ENHANCE")
    window.geometry('800x900')

    # import image
    tempImg = Image.open("temp_images/start_screen.png")
    tempImg = ImageTk.PhotoImage(tempImg)

    # create frames
    image_frame = Frame(window, width=800, height=800)
    button_frame = Frame(window, width=100, height=100)
    left_frame = Frame(window, width=350, height=100)
    right_frame = Frame(window, width=350, height=100)
    image_frame.grid(row=0, sticky="new")
    button_frame.grid(row=1, sticky="ns")
    left_frame.grid(row=1, sticky="w")
    right_frame.grid(row=1, sticky="e")

    # place image in image frame
    zoomImg = Label(image_frame, image=tempImg)
    zoomImg.place(x=0, y=0)

    # place zoom buttons
    buttonList = [['A', '1'], ['A', '2'], ['A', '3'], ['B', '1'], ['B', '2'], ['B', '3'], ['C', '1'], ['C', '2'], ['C', '3']]
    nameList = ['ba1', 'ba2', 'ba3', 'bb1', 'bb2', 'bb3', 'bc1', 'bc2', 'bc3']
    for i in range(9):
        nameList[i] = make_button(button_frame, buttonList[i][0], buttonList[i][1], i)

    # place new image button and current seed label
    bnew = Button(window, text="New Image", bg="black", fg="white", font=("Arial", 10), command=new_image, pady=3)
    bnew.place(x=274, y=827)
    lseed = Label(window, text="Current Seed: " + str(seed), font=("Arial", 10), pady=1)
    lseed.place(x=218, y=805)

    # place filepath set button, filepath display label, save button
    lfile = Label(window, text="No Image Save Folder Specified", font=("Arial", 10), pady=1)
    lfile.place(x=450, y=805)
    bsave = Button(window, text="Save Image", bg="black", fg="white", font=("Arial", 10), command=save_image, pady=3)
    bsave.place(x=450, y=827)
    bfile = Button(window, text="Set Image Save Folder", font=("Arial", 10), command=get_directory, pady=1)
    bfile.place(x=450, y=858)

    # place dropdown menu
    RESOLUTION_OPTIONS = [
    "10",
    "50",
    "100",
    "400",
    "800",
    "1080",
    "1920",
    "2560"
    ]
    output_resolution = StringVar(window)
    output_resolution.set(RESOLUTION_OPTIONS[5]) # set default value
    dropdown = OptionMenu(window, output_resolution, *RESOLUTION_OPTIONS)
    dropdown.place(x=650, y=827)

    # place resolution set button
    bres = Button(window, text="Set Output Resolution", font=("Arial", 10), command=set_resolution)
    bres.place(x=650, y=858)

    # place grid checkboxes
    grid_state = IntVar()
    grid_state.set(True)
    cbgrid = Checkbutton(window, text="Activate / Deactivate Grid", font=("Arial", 10), variable=grid_state, command=partial(zoom_image, True))
    cbgrid.place(x=10, y=804)
    # place threshold checkboxes
    threshold_state = IntVar()
    threshold_state.set(False)
    cbthresh = Checkbutton(window, text="Image Thresholding", font=("Arial", 10), variable=threshold_state, command=partial(zoom_image, True))
    cbthresh.place(x=10, y=828)

    # open window until user interacts with it / closes it
    window.mainloop()



# function readState
# reads and returns state for the inputted variable
def readState(varName):
    fileIn = open("state.txt", mode="r")
    for line in fileIn:
        line = line.split(",")
        if line[0] == varName:
            retVal = line[1].strip()
    fileIn.close()
    return retVal


# function writeState
# updates state for the inputted variable
# leaves all other states untouched
def writeState(varName, state):
    # read current state
    fileIn = open("state.txt", mode="r")
    inText = fileIn.read().split("\n")
    fileIn.close()
    # modify selected state
    fileOut = open("state.txt", mode="w")
    outText = ""
    for line in inText:
        if line:
            if varName in line:
                line = line.split(",")
                line = line[0] + "," + state + "\n"
                outText += line
            else:
                outText += line + "\n"
    print(outText, file=fileOut)
    fileOut.close()


# function drawLineGrid
# draws grid of white lines on top of temp image
def drawLineGrid():
    img = Image.open("temp_images/temp_img.png")
    draw = ImageDraw.Draw(img)
    sz = img.size[0]
    draw.line((sz/3, 0, sz/3, sz), fill=(255,255,255), width=1)
    draw.line((2*sz/3, 0, 2*sz/3, sz), fill=(255,255,255), width=1)
    draw.line((0, sz/3, sz, sz/3), fill=(255,255,255), width=1)
    draw.line((0, 2*sz/3, sz, 2*sz/3), fill=(255,255,255), width=1)
    del draw
    img.save("temp_images/temp_img.png", "PNG")


# function threshold
# thresholds image after it has been created
def threshold(path):
    # open image
    img = cv2.imread(path)
    # convert image to posterized version
    img[img >= 128]= 255
    img[img < 128] = 0
    # save result as new image
    cv2.imwrite(path, img)



main()
