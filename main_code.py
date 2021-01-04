import tkinter
import cv2  # Pip install opencv-python
import PIL.Image, PIL.ImageTk # Pip install pillow
from functools import partial
import threading
import imutils
import time

stream = cv2.VideoCapture("clip.mp4")
def play(speed):
    print(f"You clicked on play. Speed is {speed}")

    # Play the video in reverse mode
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read() 
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    canvas.create_text(120, 25, fill="green", font="Times 20 italic bold", text="Decision pending")
    

def pending(decision):
    # 1)Display decision pending image
    frame = cv2.cvtColor(cv2.imread("decision_pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

    # 2)Wait for 1 second
    time.sleep(1)

    # 3)Display sponsor's image
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

    # 4)Wait for 1.5 second
    time.sleep(1.5)
    # 5)Display weather the player is out or not out 
    if decision == 'out':
        decisionImg = "out.png"
    else:
        decisionImg = "not_out.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)


def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")

def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")

# Width and height of our main screen
SET_WIDTH = 650
SET_HEIGHT = 390

# tkinter GUI starts here
window = tkinter.Tk()
window.title("Mayur Third Umpire Decision Review System")
cv_img = cv2.cvtColor(cv2.imread("main_screen.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0,0, anchor=tkinter.NW, image=photo)
canvas.pack()


# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous(FAST)", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous(SLOW)", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next(SLOW) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Next(FAST) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="GIVE OUT", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="GIVE NOT OUT", width=50, command=not_out)
btn.pack()
window.mainloop()