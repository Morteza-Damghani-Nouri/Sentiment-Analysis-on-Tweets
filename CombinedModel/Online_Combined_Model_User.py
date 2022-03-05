import tkinter as tk    # This library is used for GUI implementation
from tkinter import *
import pickle
import math
from Commons import dictionary_loader
from Commons import nltk_input_list_generator_online_version
from Commons import comment_smoother
from Commons import unique_words_counter
from Commons import background_image_resize


# This function receives a tweet and prints the tweet and its sentiment class
def sentiment_detector():
    input_tweet = T.get("1.0", "end")
    if input_tweet != "" and input_tweet != " " and input_tweet != " \n" and input_tweet != "\n\n":
        input_positive_dictionary = positive_comments_dictionary
        input_negative_dictionary = negative_comments_dictionary
        number_of_positive_words = total_number_of_positive_dictionary_words
        number_of_negative_words = total_number_of_negative_dictionary_words
        number_of_unique_words = unique_words_amount
        input_classifier = classifier

        lower_input_tweet = input_tweet.lower()
        me_predicted_label = input_classifier.classify(nltk_input_list_generator_online_version(lower_input_tweet))

        new_input_tweet = comment_smoother(lower_input_tweet)
        words_list = new_input_tweet.split(" ")
        final_result = 0
        for word in words_list:
            if word in input_positive_dictionary:
                positive_numerator = input_positive_dictionary[word] + 1
            else:
                positive_numerator = 1

            if word in input_negative_dictionary:
                negative_numerator = input_negative_dictionary[word] + 1
            else:
                negative_numerator = 1

            final_result += math.log10((positive_numerator / (number_of_positive_words + number_of_unique_words)) / (
                        negative_numerator / (number_of_negative_words + number_of_unique_words)))

        if final_result > 0:
            nb_predicted_label = 1
        if final_result == 0:
            nb_predicted_label = 0
        if final_result < 0:
            nb_predicted_label = -1

        if nb_predicted_label == 1 and me_predicted_label == 1:
            final_label = 1
        if nb_predicted_label == -1 and me_predicted_label == -1:
            final_label = -1
        if nb_predicted_label == 1 and me_predicted_label == 0:
            final_label = 0
        if nb_predicted_label == -1 and me_predicted_label == 0:
            final_label = 0
        if nb_predicted_label == -1 and me_predicted_label == 1:
            final_label = -1
        if nb_predicted_label == 1 and me_predicted_label == -1:
            final_label = 1
        if nb_predicted_label == 0 and me_predicted_label == 1:
            final_label = 1
        if nb_predicted_label == 0 and me_predicted_label == -1:
            final_label = -1
        if nb_predicted_label == 0 and me_predicted_label == 0:
            final_label = 0

        if final_label == 1:
            tweets_text_box.config(state=NORMAL)
            tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "positive")
        if final_label == 0:
            tweets_text_box.config(state=NORMAL)
            tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "neutral")
        if final_label == -1:
            tweets_text_box.config(state=NORMAL)
            tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "negative")
        tweets_text_box.insert(END, "================================================================================\n", "separator")
        tweets_text_box.config(state=DISABLED)
        T.delete("1.0", "end")
    else:
        T.delete("1.0", "end")


# This function removes the foreground text in text box
def text_box_foreground_eraser(event):
    T.delete("1.0", "end")


# Main part of the code starts here

# Loading saved model
print("Loading saved models...")
positive_comments_dictionary, negative_comments_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words = dictionary_loader()
model_file = open("E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//MaximumEntropy//MaximumEntropyClassifier", "rb")
classifier = pickle.load(model_file)
model_file.close()
unique_words_amount = unique_words_counter(positive_comments_dictionary, negative_comments_dictionary)

# Loading graphics
window = Tk()
window.title("Sentiment Analyzer")

# Adjusting window size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(str(screen_width) + "x" + str(screen_height))
background_image_resize(screen_width, screen_height)

# Setting GUI background image
img = PhotoImage(file="BackgroundImage_Proper_Size.png")
label = Label(window, image=img, border=0)
label.place(x=0, y=0)

# Creating tweets frame
tweets_frame = tk.Frame(window)
tweets_frame_scrollbar = Scrollbar(tweets_frame)
tweets_text_box = Text(tweets_frame, height=25, width=80, relief=RIDGE, borderwidth=5, yscrollcommand=tweets_frame_scrollbar.set, bg="grey", font="calibry 12")
tweets_frame_scrollbar.pack(side=RIGHT, fill=Y)
tweets_text_box.insert(INSERT, "Recent Analyzed Tweets:\n")
tweets_text_box.config(state=DISABLED)
tweets_text_box.tag_config("positive", foreground="green")
tweets_text_box.tag_config("negative", foreground="red")
tweets_text_box.tag_config("neutral", foreground="blue")
tweets_text_box.tag_config("separator", foreground="black")

# Create text widget and specify size
input_text_box_frame = tk.Frame(window)
T_scrollbar = Scrollbar(input_text_box_frame)
T = Text(input_text_box_frame, height=5, width=70, relief=RIDGE, borderwidth=5, yscrollcommand=T_scrollbar.set, bg="grey", font="calibry 14")
T.insert(INSERT, "Type tweet here...")
T.bind("<Button-1>", text_box_foreground_eraser)
T_scrollbar.config(command=T.yview)
T_scrollbar.pack(side=RIGHT, fill=Y)

# Create button for next text
b1 = Button(window, text ="Analyze Text", command=sentiment_detector, relief=RIDGE, borderwidth=3, font="calibri 12")

# Create an Exit button
b2 = Button(window, text ="Exit", command = window.destroy, relief=RIDGE, borderwidth=3, font="calibri 12")

tweets_frame.pack(pady=(20, 20))
tweets_text_box.pack()
input_text_box_frame.pack(pady=(10, 20))
T.pack()
b1.pack(pady=(0, 10))
b2.pack()
tk.mainloop()








