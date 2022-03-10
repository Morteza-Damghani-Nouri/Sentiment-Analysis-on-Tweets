import tweepy
import pickle
import math
import tkinter as tk    # This library is used for GUI implementation
from tkinter import *
from Commons import twitter_authenticator
from Commons import dictionary_loader
from Commons import nltk_input_list_generator_online_version
from Commons import comment_smoother
from Commons import unique_words_counter
from Commons import background_image_resize


# This function receives a tweet and prints the tweet and its sentiment class
def sentiment_detector(input_tweet):
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
            tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "positive")
        if final_label == 0:
            tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "neutral")
        if final_label == -1:
            tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "negative")
        tweets_text_box.insert(END, "================================================================================\n", "separator")


# This function receives new tweets and new trend topics by twitter API and shows them on tweet box and trend topics box
def tweet_box_refresher():
    T.config(state=NORMAL)
    tweets_text_box.config(state=NORMAL)
    T.delete("1.0", "end")
    tweets_text_box.delete("1.0", "end")

    # fetching the top 50 trends topics in Washington
    print("Receiving trend topics...")
    trends = api.get_place_trends(id=woeid)
    trend_topics_names = []
    for value in trends:
        for trend in value['trends']:
            trend_topics_names.append(trend['name'])
    print("Receiving tweets...")
    received_tweets = []
    i = 0
    while i < 4:
        results = tweepy.Cursor(api.search_tweets, q=trend_topics_names[i], tweet_mode="extended").items(10)
        for result in results:
            if result.lang == "en":
                received_tweets.append(result.full_text)
        i += 1
    print("New tweets received")
    T.insert(INSERT, "Top 10 Trend Twitter Topics:\n", "trend_topics")
    for i in range(10):
        if i != 9:
            T.insert(END, str(i + 1) + ")  " + trend_topics_names[i] + "\n", "topics")
        else:
            T.insert(END, str(i + 1) + ") " + trend_topics_names[i] + "\n", "topics")
    T.config(state=DISABLED)
    tweets_text_box.insert(INSERT, "Recent Analyzed Tweets:\n")
    for tweet in received_tweets:
        sentiment_detector(tweet)
    tweets_text_box.config(state=DISABLED)


# Main part of the code starts here
# Twitter Authentication
api = twitter_authenticator()

# Loading saved model
print("Loading saved models...")
positive_comments_dictionary, negative_comments_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words = dictionary_loader()
model_file = open("E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//MaximumEntropy//MaximumEntropyClassifier", "rb")
classifier = pickle.load(model_file)
model_file.close()

# WOEID of Washington
woeid = 2514815

# Storing received tweets in a file
my_dataset = open("My Dataset.txt", "at", encoding="utf8")
my_dataset.write("==============================================================================\nNEW TWEETS:\n")

# fetching the top 50 trends topics in Washington
print("Receiving trend topics...")
trends = api.get_place_trends(id=woeid)
trend_topics_names = []
for value in trends:
    for trend in value['trends']:
        trend_topics_names.append(trend['name'])
print("Receiving tweets...")
received_tweets = []
i = 0
while i < 4:
    results = tweepy.Cursor(api.search_tweets, q=trend_topics_names[i], tweet_mode = "extended").items(10)
    for result in results:
       if result.lang == "en":
        received_tweets.append(result.full_text)
        my_dataset.write(result.full_text + "\n")
        my_dataset.write("==============================================================================\n")
    i += 1
unique_words_amount = unique_words_counter(positive_comments_dictionary, negative_comments_dictionary)


# Loading graphics
window = Tk()
window.title("Twitter Sentiment Analyzer")

# Adjusting window size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(str(screen_width) + "x" + str(screen_height))
background_image_resize(screen_width, screen_height, "Background_Image.png", "Background_Image_Resized.png")

# Setting GUI background image
img = PhotoImage(file="Background_Image_Resized.png")
label = Label(window, image=img, border=0)
label.place(x=0, y=0)

# Creating tweets frame
tweets_frame = tk.Frame(window)
tweets_frame_scrollbar = Scrollbar(tweets_frame)
tweets_text_box = Text(tweets_frame, height=25, width=80, relief=RIDGE, borderwidth=5, yscrollcommand=tweets_frame_scrollbar.set, bg="grey", font="calibry 12")
tweets_frame_scrollbar.pack(side=RIGHT, fill=Y)
tweets_text_box.insert(INSERT, "Recent Analyzed Tweets:\n")
tweets_text_box.tag_config("positive", foreground="green")
tweets_text_box.tag_config("negative", foreground="red")
tweets_text_box.tag_config("neutral", foreground="blue")
tweets_text_box.tag_config("separator", foreground="black")

# Creating text widget and specify size
input_text_box_frame = tk.Frame(window)
T_scrollbar = Scrollbar(input_text_box_frame)
T = Text(input_text_box_frame, height=5, width=70, relief=RIDGE, borderwidth=5, yscrollcommand=T_scrollbar.set, bg="grey", font="calibry 12")
T_scrollbar.config(command=T.yview)
T_scrollbar.pack(side=RIGHT, fill=Y)
T.tag_config("trend_topics", foreground="red")
T.tag_config("topics", foreground="orange")

# Creating button for analyzing input tweet
background_image_resize(50, 50, "Twitter_Icon.png", "Twitter_Icon_Resized.png")
icon = PhotoImage(file="Twitter_Icon_Resized.png")
b1 = Button(window, text ="Receive New Tweets", relief=RIDGE, borderwidth=3, font="calibri 12", image=icon, compound=LEFT, bg="white", command=tweet_box_refresher)

# Creating an Exit button
b2 = Button(window, text ="Exit", command = window.destroy, relief=RIDGE, borderwidth=3, font="calibri 12", bg="white")

# Showing received data in GUI
T.insert(INSERT, "Top 10 Trend Twitter Topics:\n", "trend_topics")
for i in range(10):
    if i != 9:
        T.insert(END, str(i + 1) + ")  " + trend_topics_names[i] + "\n", "topics")
    else:
        T.insert(END, str(i + 1) + ") " + trend_topics_names[i] + "\n", "topics")
T.config(state=DISABLED)
for tweet in received_tweets:
    sentiment_detector(tweet)
my_dataset.close()
tweets_text_box.config(state=DISABLED)
tweets_frame.pack(pady=(20, 20))
tweets_text_box.pack()
input_text_box_frame.pack(pady=(10, 20))
T.pack()
b1.pack(pady=(0, 10))
b2.pack()
tk.mainloop()










