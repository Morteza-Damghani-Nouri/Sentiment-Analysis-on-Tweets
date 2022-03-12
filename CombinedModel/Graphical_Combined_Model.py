import tkinter as tk    # This library is used for GUI implementation
from tkinter import *
from Commons import background_image_resize

# Main part of the code starts here
# Loading graphics
window = Tk()
window.title("Sentiment Analyzer")

# Adjusting window size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(str(screen_width) + "x" + str(screen_height))
background_image_resize(screen_width, screen_height, "Background_Image.png", "Background_Image_Resized.png")

# Setting GUI background image
img = PhotoImage(file="Background_Image_Resized.png")
label = Label(window, image=img, border=0)
label.place(x=0, y=0)


# Creating button for analyzing input tweet
background_image_resize(50, 50, "Twitter_Icon.png", "Twitter_Icon_Resized.png")
twitter_icon = PhotoImage(file="Twitter_Icon_Resized.png")
twitter_button = Button(window, text ="Receive Tweets From Twitter", relief=RIDGE, borderwidth=3, font="calibri 12", image=twitter_icon, compound=LEFT, bg="white", width=250, height=60)

# Creating an Exit button
background_image_resize(60, 60, "User_Icon.png", "User_Icon_Resized.png")
user_icon = PhotoImage(file="User_Icon_Resized.png")
user_button = Button(window, text ="Receive Tweets From User", relief=RIDGE, borderwidth=3, font="calibri 12", bg="white", image=user_icon, compound=LEFT, width=250, height=60)

# Creating exit button
exit_button = Button(window, text ="Exit", command = window.destroy, relief=RIDGE, borderwidth=3, font="calibri 12", width=12)


twitter_button.pack(pady=(int(screen_height * 0.35), 0))
user_button.pack(pady=(20, 0))
exit_button.pack(pady=(20, 0))
tk.mainloop()












