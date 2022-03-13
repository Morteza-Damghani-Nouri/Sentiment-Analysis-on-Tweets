import tweepy
import pickle
import tkinter as tk    # This library is used for GUI implementation
from tkinter import *
from Commons import twitter_authenticator
from Commons import dictionary_loader
from Commons import unique_words_counter
from Commons import background_image_resize
from Commons import create_model
from Commons import model_dictionary_generator
from Commons import nb_predictor
from Commons import me_predictor
from Commons import fcnn_predictor
from Commons import nb_predictor_online_version
from Commons import me_predictor_online_version
from Commons import fcnn_predictor_online_version
from Commons import data_loader_online_version
from Commons import precision_calculator


# This function returns the final classification of combined model
def twitter_final_predictor(input_tweet, input_tweets_text_box):
    if input_tweet != "" and input_tweet != " " and input_tweet != " \n" and input_tweet != "\n\n":
        input_nb_results = nb_predictor_online_version(input_tweet, positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words, number_of_unique_words)
        input_me_results = me_predictor_online_version(input_tweet, me_classifier)
        input_fcnn_results = fcnn_predictor_online_version(data_loader_online_version(input_tweet, fcnn_model_dictionary), fcnn_model)
        final_results = []
        i = 0
        while i < len(input_nb_results):
            if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
                final_results.append(1)
            if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
                final_results.append(-1)
            if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
                final_results.append(0)
            if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
                maximum_positive = max(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
                minimum_positive = min(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= FCNN_NEGATIVE_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(-1)
            if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
                maximum_positive = max(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                minimum_positive = min(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= ME_NEGATIVE_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(-1)
            if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
                maximum_positive = max(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                minimum_positive = min(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= NB_NEGATIVE_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(-1)
            if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
                maximum_positive = max(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
                minimum_positive = min(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= FCNN_NEUTRAL_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
                maximum_positive = max(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                minimum_positive = min(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= ME_NEUTRAL_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
                maximum_positive = max(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                minimum_positive = min(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= NB_NEUTRAL_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
                if best_method_name == "nb":
                    maximum_precision = max(NB_POSITIVE_PRECISION + (best_method_precision / 5), ME_NEGATIVE_PRECISION, FCNN_NEUTRAL_PRECISION)
                    if maximum_precision == (NB_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
                    if maximum_precision == ME_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == FCNN_NEUTRAL_PRECISION:
                        final_results.append(0)
                if best_method_name == "me":
                    maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEGATIVE_PRECISION + (best_method_precision / 5), FCNN_NEUTRAL_PRECISION)
                    if maximum_precision == NB_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == (ME_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
                    if maximum_precision == FCNN_NEUTRAL_PRECISION:
                        final_results.append(0)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEGATIVE_PRECISION, FCNN_NEUTRAL_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == ME_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == (FCNN_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
            if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
                if best_method_name == "nb":
                    maximum_precision = max(NB_NEGATIVE_PRECISION + (best_method_precision / 5), ME_POSITIVE_PRECISION, FCNN_NEUTRAL_PRECISION)
                    if maximum_precision == (NB_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
                    if maximum_precision == ME_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == FCNN_NEUTRAL_PRECISION:
                        final_results.append(0)
                if best_method_name == "me":
                    maximum_precision = max(NB_NEGATIVE_PRECISION, ME_POSITIVE_PRECISION + (best_method_precision / 5), FCNN_NEUTRAL_PRECISION)
                    if maximum_precision == NB_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == (ME_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
                    if maximum_precision == FCNN_NEUTRAL_PRECISION:
                        final_results.append(0)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_NEGATIVE_PRECISION, ME_POSITIVE_PRECISION, FCNN_NEUTRAL_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == ME_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == (FCNN_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
            if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
                if best_method_name == "nb":
                    maximum_precision = max(NB_NEGATIVE_PRECISION + (best_method_precision / 5), ME_NEUTRAL_PRECISION, FCNN_POSITIVE_PRECISION)
                    if maximum_precision == (NB_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
                    if maximum_precision == ME_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == FCNN_POSITIVE_PRECISION:
                        final_results.append(1)
                if best_method_name == "me":
                    maximum_precision = max(NB_NEGATIVE_PRECISION, ME_NEUTRAL_PRECISION + (best_method_precision / 5), FCNN_POSITIVE_PRECISION)
                    if maximum_precision == NB_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == (ME_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
                    if maximum_precision == FCNN_POSITIVE_PRECISION:
                        final_results.append(1)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_NEGATIVE_PRECISION, ME_NEUTRAL_PRECISION, FCNN_POSITIVE_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == ME_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == (FCNN_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
            if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
                if best_method_name == "nb":
                    maximum_precision = max(NB_POSITIVE_PRECISION + (best_method_precision / 5), ME_NEUTRAL_PRECISION, FCNN_NEGATIVE_PRECISION)
                    if maximum_precision == (NB_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
                    if maximum_precision == ME_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == FCNN_NEGATIVE_PRECISION:
                        final_results.append(-1)
                if best_method_name == "me":
                    maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEUTRAL_PRECISION + (best_method_precision / 5), FCNN_NEGATIVE_PRECISION)
                    if maximum_precision == NB_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == (ME_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
                    if maximum_precision == FCNN_NEGATIVE_PRECISION:
                        final_results.append(-1)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEUTRAL_PRECISION, FCNN_NEGATIVE_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == ME_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == (FCNN_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
            if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
                if best_method_name == "nb":
                    maximum_precision = max(NB_NEUTRAL_PRECISION + (best_method_precision / 5), ME_POSITIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                    if maximum_precision == (NB_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
                    if maximum_precision == ME_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == FCNN_NEGATIVE_PRECISION:
                        final_results.append(-1)
                if best_method_name == "me":
                    maximum_precision = max(NB_NEUTRAL_PRECISION, ME_POSITIVE_PRECISION + (best_method_precision / 5), FCNN_NEGATIVE_PRECISION)
                    if maximum_precision == NB_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == (ME_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
                    if maximum_precision == FCNN_NEGATIVE_PRECISION:
                        final_results.append(-1)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_NEUTRAL_PRECISION, ME_POSITIVE_PRECISION, FCNN_NEGATIVE_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == ME_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == (FCNN_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
            if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
                if best_method_name == "nb":
                    maximum_precision = max(NB_NEUTRAL_PRECISION + (best_method_precision / 5), ME_NEGATIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                    if maximum_precision == (NB_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
                    if maximum_precision == ME_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == FCNN_POSITIVE_PRECISION:
                        final_results.append(1)
                if best_method_name == "me":
                    maximum_precision = max(NB_NEUTRAL_PRECISION, ME_NEGATIVE_PRECISION + (best_method_precision / 5), FCNN_POSITIVE_PRECISION)
                    if maximum_precision == NB_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == (ME_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
                    if maximum_precision == FCNN_POSITIVE_PRECISION:
                        final_results.append(1)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_NEUTRAL_PRECISION, ME_NEGATIVE_PRECISION, FCNN_POSITIVE_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == ME_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == (FCNN_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
            if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
                maximum_negative = max(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
                minimum_negative = min(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= FCNN_POSITIVE_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(1)
            if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
                maximum_negative = max(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                minimum_negative = min(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= ME_POSITIVE_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(1)
            if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
                maximum_negative = max(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                minimum_negative = min(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= NB_POSITIVE_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(1)
            if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
                maximum_neutral = max(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                minimum_neutral = min(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= NB_POSITIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(1)
            if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
                maximum_neutral = max(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                minimum_neutral = min(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= ME_POSITIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(1)
            if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
                maximum_neutral = max(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
                minimum_neutral = min(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= FCNN_POSITIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(1)
            if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
                maximum_negative = max(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                minimum_negative = min(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= NB_NEUTRAL_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
                maximum_negative = max(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                minimum_negative = min(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= ME_NEUTRAL_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
                maximum_negative = max(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
                minimum_negative = min(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= FCNN_NEUTRAL_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
                maximum_neutral = max(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                minimum_neutral = min(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= NB_NEGATIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(-1)
            if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
                maximum_neutral = max(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                minimum_neutral = min(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= ME_NEGATIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(-1)
            if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
                maximum_neutral = max(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
                minimum_neutral = min(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= FCNN_NEGATIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(-1)
            i += 1

        if final_results[0] == 1:
            input_tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "positive")
        if final_results[0] == 0:
            input_tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "neutral")
        if final_results[0] == -1:
            input_tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "negative")
        input_tweets_text_box.insert(END, "================================================================================\n", "separator")


# This function returns the final classification of combined model
def user_final_predictor(input_T, input_tweets_text_box):
    input_tweet = input_T.get("1.0", "end")
    if input_tweet != "" and input_tweet != " " and input_tweet != " \n" and input_tweet != "\n\n" and input_tweet != "Type tweet here...\n":
        input_nb_results = nb_predictor_online_version(input_tweet, positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words, number_of_unique_words)
        input_me_results = me_predictor_online_version(input_tweet, me_classifier)
        input_fcnn_results = fcnn_predictor_online_version(data_loader_online_version(input_tweet, fcnn_model_dictionary), fcnn_model)
        final_results = []
        i = 0
        while i < len(input_nb_results):
            if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
                final_results.append(1)
            if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
                final_results.append(-1)
            if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
                final_results.append(0)
            if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
                maximum_positive = max(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
                minimum_positive = min(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= FCNN_NEGATIVE_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(-1)
            if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
                maximum_positive = max(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                minimum_positive = min(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= ME_NEGATIVE_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(-1)
            if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
                maximum_positive = max(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                minimum_positive = min(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= NB_NEGATIVE_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(-1)
            if input_nb_results[i] == 1 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
                maximum_positive = max(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
                minimum_positive = min(NB_POSITIVE_PRECISION, ME_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= FCNN_NEUTRAL_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
                maximum_positive = max(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                minimum_positive = min(NB_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= ME_NEUTRAL_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == 1:
                maximum_positive = max(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                minimum_positive = min(ME_POSITIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                final_positive_precision = round(maximum_positive + (minimum_positive / 2), 2)
                if final_positive_precision >= NB_NEUTRAL_PRECISION:
                    final_results.append(1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
                if best_method_name == "nb":
                    maximum_precision = max(NB_POSITIVE_PRECISION + (best_method_precision / 5), ME_NEGATIVE_PRECISION, FCNN_NEUTRAL_PRECISION)
                    if maximum_precision == (NB_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
                    if maximum_precision == ME_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == FCNN_NEUTRAL_PRECISION:
                        final_results.append(0)
                if best_method_name == "me":
                    maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEGATIVE_PRECISION + (best_method_precision / 5), FCNN_NEUTRAL_PRECISION)
                    if maximum_precision == NB_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == (ME_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
                    if maximum_precision == FCNN_NEUTRAL_PRECISION:
                        final_results.append(0)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEGATIVE_PRECISION, FCNN_NEUTRAL_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == ME_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == (FCNN_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
            if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
                if best_method_name == "nb":
                    maximum_precision = max(NB_NEGATIVE_PRECISION + (best_method_precision / 5), ME_POSITIVE_PRECISION, FCNN_NEUTRAL_PRECISION)
                    if maximum_precision == (NB_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
                    if maximum_precision == ME_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == FCNN_NEUTRAL_PRECISION:
                        final_results.append(0)
                if best_method_name == "me":
                    maximum_precision = max(NB_NEGATIVE_PRECISION, ME_POSITIVE_PRECISION + (best_method_precision / 5), FCNN_NEUTRAL_PRECISION)
                    if maximum_precision == NB_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == (ME_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
                    if maximum_precision == FCNN_NEUTRAL_PRECISION:
                        final_results.append(0)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_NEGATIVE_PRECISION, ME_POSITIVE_PRECISION, FCNN_NEUTRAL_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == ME_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == (FCNN_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
            if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
                if best_method_name == "nb":
                    maximum_precision = max(NB_NEGATIVE_PRECISION + (best_method_precision / 5), ME_NEUTRAL_PRECISION, FCNN_POSITIVE_PRECISION)
                    if maximum_precision == (NB_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
                    if maximum_precision == ME_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == FCNN_POSITIVE_PRECISION:
                        final_results.append(1)
                if best_method_name == "me":
                    maximum_precision = max(NB_NEGATIVE_PRECISION, ME_NEUTRAL_PRECISION + (best_method_precision / 5), FCNN_POSITIVE_PRECISION)
                    if maximum_precision == NB_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == (ME_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
                    if maximum_precision == FCNN_POSITIVE_PRECISION:
                        final_results.append(1)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_NEGATIVE_PRECISION, ME_NEUTRAL_PRECISION, FCNN_POSITIVE_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == ME_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == (FCNN_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
            if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
                if best_method_name == "nb":
                    maximum_precision = max(NB_POSITIVE_PRECISION + (best_method_precision / 5), ME_NEUTRAL_PRECISION, FCNN_NEGATIVE_PRECISION)
                    if maximum_precision == (NB_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
                    if maximum_precision == ME_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == FCNN_NEGATIVE_PRECISION:
                        final_results.append(-1)
                if best_method_name == "me":
                    maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEUTRAL_PRECISION + (best_method_precision / 5), FCNN_NEGATIVE_PRECISION)
                    if maximum_precision == NB_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == (ME_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
                    if maximum_precision == FCNN_NEGATIVE_PRECISION:
                        final_results.append(-1)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_POSITIVE_PRECISION, ME_NEUTRAL_PRECISION, FCNN_NEGATIVE_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == ME_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == (FCNN_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
            if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
                if best_method_name == "nb":
                    maximum_precision = max(NB_NEUTRAL_PRECISION + (best_method_precision / 5), ME_POSITIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                    if maximum_precision == (NB_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
                    if maximum_precision == ME_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == FCNN_NEGATIVE_PRECISION:
                        final_results.append(-1)
                if best_method_name == "me":
                    maximum_precision = max(NB_NEUTRAL_PRECISION, ME_POSITIVE_PRECISION + (best_method_precision / 5), FCNN_NEGATIVE_PRECISION)
                    if maximum_precision == NB_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == (ME_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
                    if maximum_precision == FCNN_NEGATIVE_PRECISION:
                        final_results.append(-1)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_NEUTRAL_PRECISION, ME_POSITIVE_PRECISION, FCNN_NEGATIVE_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == ME_POSITIVE_PRECISION:
                        final_results.append(1)
                    if maximum_precision == (FCNN_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
            if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
                if best_method_name == "nb":
                    maximum_precision = max(NB_NEUTRAL_PRECISION + (best_method_precision / 5), ME_NEGATIVE_PRECISION, FCNN_POSITIVE_PRECISION)
                    if maximum_precision == (NB_NEUTRAL_PRECISION + (best_method_precision / 5)):
                        final_results.append(0)
                    if maximum_precision == ME_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == FCNN_POSITIVE_PRECISION:
                        final_results.append(1)
                if best_method_name == "me":
                    maximum_precision = max(NB_NEUTRAL_PRECISION, ME_NEGATIVE_PRECISION + (best_method_precision / 5), FCNN_POSITIVE_PRECISION)
                    if maximum_precision == NB_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == (ME_NEGATIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(-1)
                    if maximum_precision == FCNN_POSITIVE_PRECISION:
                        final_results.append(1)
                if best_method_name == "fcnn":
                    maximum_precision = max(NB_NEUTRAL_PRECISION, ME_NEGATIVE_PRECISION, FCNN_POSITIVE_PRECISION + (best_method_precision / 5))
                    if maximum_precision == NB_NEUTRAL_PRECISION:
                        final_results.append(0)
                    if maximum_precision == ME_NEGATIVE_PRECISION:
                        final_results.append(-1)
                    if maximum_precision == (FCNN_POSITIVE_PRECISION + (best_method_precision / 5)):
                        final_results.append(1)
            if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == 1:
                maximum_negative = max(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
                minimum_negative = min(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= FCNN_POSITIVE_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(1)
            if input_nb_results[i] == -1 and input_me_results[i] == 1 and input_fcnn_results[i] == -1:
                maximum_negative = max(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                minimum_negative = min(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= ME_POSITIVE_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(1)
            if input_nb_results[i] == 1 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
                maximum_negative = max(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                minimum_negative = min(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= NB_POSITIVE_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(1)
            if input_nb_results[i] == 1 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
                maximum_neutral = max(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                minimum_neutral = min(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= NB_POSITIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(1)
            if input_nb_results[i] == 0 and input_me_results[i] == 1 and input_fcnn_results[i] == 0:
                maximum_neutral = max(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                minimum_neutral = min(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= ME_POSITIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(1)
            if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == 1:
                maximum_neutral = max(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
                minimum_neutral = min(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= FCNN_POSITIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(1)
            if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == -1:
                maximum_negative = max(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                minimum_negative = min(ME_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= NB_NEUTRAL_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
                maximum_negative = max(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                minimum_negative = min(NB_NEGATIVE_PRECISION, FCNN_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= ME_NEUTRAL_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == -1 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
                maximum_negative = max(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
                minimum_negative = min(NB_NEGATIVE_PRECISION, ME_NEGATIVE_PRECISION)
                final_negative_precision = round(maximum_negative + (minimum_negative / 2), 2)
                if final_negative_precision >= FCNN_NEUTRAL_PRECISION:
                    final_results.append(-1)
                else:
                    final_results.append(0)
            if input_nb_results[i] == -1 and input_me_results[i] == 0 and input_fcnn_results[i] == 0:
                maximum_neutral = max(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                minimum_neutral = min(ME_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= NB_NEGATIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(-1)
            if input_nb_results[i] == 0 and input_me_results[i] == -1 and input_fcnn_results[i] == 0:
                maximum_neutral = max(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                minimum_neutral = min(NB_NEUTRAL_PRECISION, FCNN_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= ME_NEGATIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(-1)
            if input_nb_results[i] == 0 and input_me_results[i] == 0 and input_fcnn_results[i] == -1:
                maximum_neutral = max(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
                minimum_neutral = min(NB_NEUTRAL_PRECISION, ME_NEUTRAL_PRECISION)
                final_neutral_precision = round(maximum_neutral + (minimum_neutral / 2), 2)
                if final_neutral_precision >= FCNN_NEGATIVE_PRECISION:
                    final_results.append(0)
                else:
                    final_results.append(-1)
            i += 1

        if final_results[0] == 1:
            input_tweets_text_box.config(state=NORMAL)
            input_tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "positive")
        if final_results[0] == 0:
            input_tweets_text_box.config(state=NORMAL)
            input_tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "neutral")
        if final_results[0] == -1:
            input_tweets_text_box.config(state=NORMAL)
            input_tweets_text_box.insert(END, input_tweet.rstrip("\n") + "\n", "negative")
        input_tweets_text_box.insert(END, "================================================================================\n", "separator")
        input_tweets_text_box.config(state=DISABLED)
        input_T.delete("1.0", "end")
    else:
        input_T.delete("1.0", "end")


# This function finds the most accurate method among avalaible methods according to precision
def best_method_finder():
    nb_average_precision = (NB_POSITIVE_PRECISION + NB_NEGATIVE_PRECISION + NB_NEUTRAL_PRECISION) / 3
    me_average_precision = (ME_POSITIVE_PRECISION + ME_NEGATIVE_PRECISION + ME_NEUTRAL_PRECISION) / 3
    fcnn_average_precision = (FCNN_POSITIVE_PRECISION + FCNN_NEGATIVE_PRECISION + FCNN_NEUTRAL_PRECISION) / 3
    if nb_average_precision == me_average_precision:
        print("The precision of Naive Bayes method and Maximum Entropy method are equal. Unable to find the best method according to average precision.")
        exit(1)
    if nb_average_precision == fcnn_average_precision:
        print("The precision of Naive Bayes method and Fully Connected Neural Network method are equal. Unable to find the best method according to average precision.")
        exit(1)
    if me_average_precision == fcnn_average_precision:
        print("The precision of Maximum Entropy method and Fully Connected Neural Network method are equal. Unable to find the best method according to average precision.")
        exit(1)
    maximum_precision = max(nb_average_precision, me_average_precision, fcnn_average_precision)
    if maximum_precision == nb_average_precision:
        return maximum_precision, "nb"
    if maximum_precision == me_average_precision:
        return maximum_precision, "me"
    if maximum_precision == fcnn_average_precision:
        return maximum_precision, "fcnn"


# This function removes all the widgets in the main window
def clear_main_window(input_window):
   for widget in input_window.winfo_children():
      widget.pack_forget()


# This function receives new tweets and new trend topics by twitter API and shows them on tweet box and trend topics box
def tweet_box_refresher(input_T, input_tweets_text_box):
    input_T.config(state=NORMAL)
    input_tweets_text_box.config(state=NORMAL)
    input_T.delete("1.0", "end")
    input_tweets_text_box.delete("1.0", "end")

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
    input_T.insert(INSERT, "Top 10 Trend Twitter Topics:\n", "trend_topics")
    for i in range(10):
        if i != 9:
            input_T.insert(END, str(i + 1) + ")  " + trend_topics_names[i] + "\n", "topics")
        else:
            input_T.insert(END, str(i + 1) + ") " + trend_topics_names[i] + "\n", "topics")
    input_T.config(state=DISABLED)
    input_tweets_text_box.insert(INSERT, "Recent Analyzed Tweets:\n")
    for tweet in received_tweets:
        twitter_final_predictor(tweet, input_tweets_text_box)
    input_tweets_text_box.config(state=DISABLED)


# This function is called when twitter_button is pressed and it loads the graphics of twitter page
def twitter_button_handler(input_window):
    # Clearing previous window
    clear_main_window(input_window)

    input_window.title("Twitter Sentiment Analyzer")

    # Setting GUI background image
    background_image_resize(screen_width, screen_height, "Background_Image.png", "Background_Image_Resized.png")
    img = PhotoImage(file="Background_Image_Resized.png")
    label = Label(window, image=img, border=0)
    label.place(x=0, y=0)

    # Creating tweets frame
    tweets_frame = tk.Frame(input_window)
    tweets_frame_scrollbar = Scrollbar(tweets_frame)
    tweets_text_box = Text(tweets_frame, height=25, width=80, relief=RIDGE, borderwidth=5, yscrollcommand=tweets_frame_scrollbar.set, bg="grey", font="calibry 12")
    tweets_frame_scrollbar.pack(side=RIGHT, fill=Y)
    tweets_text_box.insert(INSERT, "Recent Analyzed Tweets:\n")
    tweets_text_box.tag_config("positive", foreground="green")
    tweets_text_box.tag_config("negative", foreground="red")
    tweets_text_box.tag_config("neutral", foreground="blue")
    tweets_text_box.tag_config("separator", foreground="black")

    # Creating text widget and specify size
    input_text_box_frame = tk.Frame(input_window)
    T_scrollbar = Scrollbar(input_text_box_frame)
    T = Text(input_text_box_frame, height=5, width=70, relief=RIDGE, borderwidth=5, yscrollcommand=T_scrollbar.set, bg="grey", font="calibry 12")
    T_scrollbar.config(command=T.yview)
    T_scrollbar.pack(side=RIGHT, fill=Y)
    T.tag_config("trend_topics", foreground="red")
    T.tag_config("topics", foreground="orange")

    # Creating button for analyzing input tweet
    background_image_resize(50, 50, "Twitter_Icon.png", "Twitter_Icon_Resized.png")
    icon = PhotoImage(file="Twitter_Icon_Resized.png")
    b1 = Button(input_window, text="Receive New Tweets", relief=RIDGE, borderwidth=3, font="calibri 12", image=icon, compound=LEFT, bg="white", command=lambda: tweet_box_refresher(T, tweets_text_box), width=200)

    # Creating back button
    back_button = Button(input_window, text="Back", relief=RIDGE, borderwidth=3, font="calibri 12", width=10, bg="white")

    # Creating an Exit button
    b2 = Button(input_window, text="Exit", command=input_window.destroy, relief=RIDGE, borderwidth=3, font="calibri 12", bg="white", width=10)

    # Showing received data in GUI
    T.insert(INSERT, "Top 10 Trend Twitter Topics:\n", "trend_topics")
    for i in range(10):
        if i != 9:
            T.insert(END, str(i + 1) + ")  " + trend_topics_names[i] + "\n", "topics")
        else:
            T.insert(END, str(i + 1) + ") " + trend_topics_names[i] + "\n", "topics")
    T.config(state=DISABLED)
    for tweet in received_tweets:
        twitter_final_predictor(tweet, tweets_text_box)
    tweets_text_box.config(state=DISABLED)
    tweets_frame.pack(pady=(20, 10))
    tweets_text_box.pack()
    input_text_box_frame.pack(pady=(10, 10))
    T.pack()
    b1.pack(pady=(0, 10))
    back_button.pack(pady=(0, 5))
    b2.pack()
    tk.mainloop()


# This function is called when user_button is pressed and it loads the graphics of user page
def user_button_handler(input_window):
    # Clearing previous window
    clear_main_window(input_window)

    input_window.title("User Sentiment Analyzer")

    # Setting GUI background image
    background_image_resize(screen_width, screen_height, "Background_Image.png", "Background_Image_Resized.png")
    img = PhotoImage(file="Background_Image_Resized.png")
    label = Label(input_window, image=img, border=0)
    label.place(x=0, y=0)

    # Creating tweets frame
    tweets_frame = tk.Frame(input_window)
    tweets_frame_scrollbar = Scrollbar(tweets_frame)
    tweets_text_box = Text(tweets_frame, height=25, width=80, relief=RIDGE, borderwidth=5,
                           yscrollcommand=tweets_frame_scrollbar.set, bg="grey", font="calibry 12")
    tweets_frame_scrollbar.pack(side=RIGHT, fill=Y)
    tweets_text_box.insert(INSERT, "Recent Analyzed Tweets:\n")
    tweets_text_box.config(state=DISABLED)
    tweets_text_box.tag_config("positive", foreground="green")
    tweets_text_box.tag_config("negative", foreground="red")
    tweets_text_box.tag_config("neutral", foreground="blue")
    tweets_text_box.tag_config("separator", foreground="black")

    # Creating text widget and specify size
    input_text_box_frame = tk.Frame(input_window)
    T_scrollbar = Scrollbar(input_text_box_frame)
    T = Text(input_text_box_frame, height=5, width=70, relief=RIDGE, borderwidth=5, yscrollcommand=T_scrollbar.set,
             bg="grey", font="calibry 14")
    T_scrollbar.config(command=T.yview)
    T_scrollbar.pack(side=RIGHT, fill=Y)

    # Creating button for analyzing text
    background_image_resize(50, 50, "Analyze_Icon.png", "Analyze_Icon_Resized.png")
    icon = PhotoImage(file="Analyze_Icon_Resized.png")
    b1 = Button(input_window, text="Analyze Text", command=lambda: user_final_predictor(T, tweets_text_box), relief=RIDGE, borderwidth=3, font="calibri 12", image=icon, width=150, bg="white", compound=LEFT)

    # Creating back button
    back_button = Button(input_window, text="Back", relief=RIDGE, borderwidth=3, font="calibri 12", width=10, bg="white")

    # Creating an Exit button
    b2 = Button(input_window, text="Exit", command=input_window.destroy, relief=RIDGE, borderwidth=3, font="calibri 12", width=10, bg="white")

    tweets_frame.pack(pady=(20, 10))
    tweets_text_box.pack()
    input_text_box_frame.pack(pady=(10, 10))
    T.pack()
    b1.pack(pady=(0, 10))
    back_button.pack(pady=(0, 5))
    b2.pack()
    tk.mainloop()


# Main part of the code starts here
# Twitter Authentication
api = twitter_authenticator()

# Loading saved model
print("Loading saved models...")
positive_tweets_dictionary, negative_tweets_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words = dictionary_loader()
me_model_file = open(
    "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//MaximumEntropy//MaximumEntropyClassifier",
    "rb")
me_classifier = pickle.load(me_model_file)
me_model_file.close()
fcnn_model = create_model()
fcnn_model_dictionary = model_dictionary_generator()
fcnn_model.load_weights(
    "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Checkpoints//Main Trained Model//my_checkpoint1")
number_of_unique_words = unique_words_counter(positive_tweets_dictionary, negative_tweets_dictionary)

# Initializing precision variables
# Evaluating the positive test tweets
positive_test_tweets_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//positive_test.txt"
nb_positive_test_results = nb_predictor(positive_test_tweets_file_address, positive_tweets_dictionary,
                                        negative_tweets_dictionary, total_number_of_positive_dictionary_words,
                                        total_number_of_negative_dictionary_words, number_of_unique_words)
me_positive_test_results = me_predictor(positive_test_tweets_file_address, 1, me_classifier)
fcnn_positive_test_tweets_file_address = "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Test_X//positive_test_x_complete.txt"
fcnn_positive_test_results = fcnn_predictor(fcnn_positive_test_tweets_file_address, fcnn_model)

# Evaluating the negative test tweets
negative_test_tweets_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//negative_test.txt"
nb_negative_test_results = nb_predictor(negative_test_tweets_file_address, positive_tweets_dictionary,
                                        negative_tweets_dictionary, total_number_of_positive_dictionary_words,
                                        total_number_of_negative_dictionary_words, number_of_unique_words)
me_negative_test_results = me_predictor(negative_test_tweets_file_address, -1, me_classifier)
fcnn_negative_test_tweets_file_address = "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Test_X//negative_test_x_complete.txt"
fcnn_negative_test_results = fcnn_predictor(fcnn_negative_test_tweets_file_address, fcnn_model)

# Evaluating the neutral test tweets
neutral_test_tweets_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//neutral_test.txt"
nb_neutral_test_results = nb_predictor(neutral_test_tweets_file_address, positive_tweets_dictionary,
                                       negative_tweets_dictionary, total_number_of_positive_dictionary_words,
                                       total_number_of_negative_dictionary_words, number_of_unique_words)
me_neutral_test_results = me_predictor(neutral_test_tweets_file_address, 0, me_classifier)
fcnn_neutral_test_tweets_file_address = "E://MortezaDamghaniNouri//MyCodes//Python Codes//Computer Engineering Final Project//FCNN//Test_X//neutral_test_x_complete.txt"
fcnn_neutral_test_results = fcnn_predictor(fcnn_neutral_test_tweets_file_address, fcnn_model)

NB_POSITIVE_PRECISION = precision_calculator(nb_positive_test_results, 1)
NB_NEGATIVE_PRECISION = precision_calculator(nb_negative_test_results, -1)
NB_NEUTRAL_PRECISION = precision_calculator(nb_neutral_test_results, 0)
ME_POSITIVE_PRECISION = precision_calculator(me_positive_test_results, 1)
ME_NEGATIVE_PRECISION = precision_calculator(me_negative_test_results, -1)
ME_NEUTRAL_PRECISION = precision_calculator(me_neutral_test_results, 0)
FCNN_POSITIVE_PRECISION = precision_calculator(fcnn_positive_test_results, 1)
FCNN_NEGATIVE_PRECISION = precision_calculator(fcnn_negative_test_results, -1)
FCNN_NEUTRAL_PRECISION = precision_calculator(fcnn_neutral_test_results, 0)
best_method_precision, best_method_name = best_method_finder()

# WOEID of Washington
woeid = 2514815

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
twitter_button = Button(window, text ="Receive Tweets From Twitter", relief=RIDGE, borderwidth=3, font="calibri 12", image=twitter_icon, compound=LEFT, bg="white", width=250, height=60, command=lambda: twitter_button_handler(window))

# Creating button for analyzing user tweets
background_image_resize(60, 60, "User_Icon.png", "User_Icon_Resized.png")
user_icon = PhotoImage(file="User_Icon_Resized.png")
user_button = Button(window, text ="Receive Tweets From User", relief=RIDGE, borderwidth=3, font="calibri 12", bg="white", image=user_icon, compound=LEFT, width=250, height=60, command=lambda: user_button_handler(window))

# Creating exit button
exit_button = Button(window, text ="Exit", command = window.destroy, relief=RIDGE, borderwidth=3, font="calibri 12", width=12, bg="white")

twitter_button.pack(pady=(int(screen_height * 0.35), 0))
user_button.pack(pady=(20, 0))
exit_button.pack(pady=(20, 0))
tk.mainloop()




