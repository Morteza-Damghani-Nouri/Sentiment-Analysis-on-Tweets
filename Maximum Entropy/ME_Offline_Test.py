import pickle   # This library is used to load the trained model from disk
import math

ENGLISH_CHARS = ["a", "b", "c",  "d",  "e",  "f",  "g",  "h",  "i",  "j",  "k",  "l",  "m",  "n",  "o",  "p",  "q",  "r",  "s",  "t",  "u",  "v",  "w",  "x",  "y",  "z",  "A",  "B",  "C",  "D",  "E",  "F",  "G",  "H",  "I",  "J",  "K",  "L",  "M",  "N",  "O",  "P",  "Q",  "R",  "S",  "T",  "U",  "V",  "W",  "X",  "Y",  "Z", "'", "\""]
# This function converts the input list to dictionary format which is accepted in NLTK library
def list_to_dict_converter(input_word_list):
    output_dict = {}
    for word in input_word_list:
        output_dict[word] = True
    return output_dict

# This function removes redundant characters of an input comment
def comment_smoother(input_comment):
    input_comment = input_comment.replace(".", "")
    input_comment = input_comment.replace("-", "")
    input_comment = input_comment.replace(";", "")
    input_comment = input_comment.replace("[", "")
    input_comment = input_comment.replace("]", "")
    input_comment = input_comment.replace(":", "")
    input_comment = input_comment.replace("*", "")
    input_comment = input_comment.replace("!", "")
    input_comment = input_comment.replace("?", "")
    input_comment = input_comment.replace(",", "")
    input_comment = input_comment.replace(")", "")
    input_comment = input_comment.replace("(", "")
    input_comment = input_comment.replace("\n", "")
    return input_comment


# This function removes the redundant last characters of words like ?? in that?? and removes numbers and the name of seasons
def smoother_function(input_word):
    if input_word.find("0") != -1 or input_word.find("1") != -1 or input_word.find("2") != -1 or input_word.find("3") != -1 or input_word.find("4") != -1 or input_word.find("5") != -1 or input_word.find("6") != -1 or input_word.find("7") != -1 or input_word.find("8") != -1 or input_word.find("9") != -1:
        return "."
    if input_word == "january" or input_word == "february" or input_word == "march" or input_word == "april" or input_word == "may" or input_word == "june" or input_word == "july" or input_word == "august" or input_word == "september" or input_word == "october" or input_word == "november" or input_word == "december":
        return "."
    if input_word.find("/") != -1 or input_word.find("\\") != -1:
        return "."
    input_word_list = list(input_word)
    while len(input_word_list) != 0 and (input_word_list[len(input_word_list) - 1] == "." or input_word_list[len(input_word_list) - 1] == "-" or input_word_list[len(input_word_list) - 1] == ";" or input_word_list[len(input_word_list) - 1] == "[" or input_word_list[len(input_word_list) - 1] == "]" or input_word_list[len(input_word_list) - 1] == ":" or input_word_list[len(input_word_list) - 1] == "*" or input_word_list[len(input_word_list) - 1] == "!" or input_word_list[len(input_word_list) - 1] == "?" or input_word_list[len(input_word_list) - 1] == "," or input_word_list[len(input_word_list) - 1] == ")" or input_word_list[len(input_word_list) - 1] == "\"" or input_word_list[len(input_word_list) - 1] == "\'"):
        input_word_list.pop(len(input_word_list) - 1)
    while len(input_word_list) != 0 and (input_word_list[0] == "(" or input_word_list[0] == "-" or input_word_list[0] == "*" or input_word_list[0] == "\'" or input_word_list[0] == "\"" or input_word_list[0] == "." or input_word_list[0] == "?" or input_word_list[0] == "[" or input_word_list[0] == "]" or input_word_list[0] == "!"):
        input_word_list.pop(0)


    output_word = ""
    for char in input_word_list:
        if char not in ENGLISH_CHARS:
            return "."
        output_word += char
    if output_word.find(",") != -1 or output_word.find(".") != -1 or output_word.find("(") != -1 or output_word.find(")") != -1 or output_word.find("!") != -1 or output_word.find("?") != -1 or output_word.find(":") != -1 or output_word.find("+") != -1 or output_word.find("@") != -1 or output_word.find("?") != -1 or output_word.find("]") != -1 or output_word.find("[") != -1 or output_word.find("$") != -1 or output_word.find("{") != -1 or output_word.find("}") != -1 or output_word.find("~") != -1 or output_word.find("|") != -1 or output_word.find("#") != -1 or output_word.find("&") != -1 or output_word.find("%") != -1 or output_word.find("=") != -1 or output_word.find(">") != -1 or output_word.find("<") != -1 or output_word.find("+") != -1 or output_word.find("_") != -1 or output_word.find("^") != -1:
        return "."
    if output_word == "january" or output_word == "february" or output_word == "march" or output_word == "april" or output_word == "may" or output_word == "june" or output_word == "july" or output_word == "august" or output_word == "september" or output_word == "october" or output_word == "november" or output_word == "december":
        return "."
    if output_word != "" and output_word != "\n" and len(output_word) != 1:
        return output_word.replace("\n", "")
    else:
        return "."


# This function generates the needed dictionary
def nltk_input_list_generator(input_address, data_tag, main_list):
    input_file = open(input_address, "rt", encoding="cp850")
    line_counter = 0
    while True:
        comment = input_file.readline().lower()
        if comment == "":
            break

        words_list = comment.split(" ")
        temp_list = []
        for word in words_list:
            if word != "." and word != "," and word != "  " and word != ";" and word != "\"" and word != "\'" and word != "*" and word != "(" and word != ")" and word != "--" and word != "-" and word != "?" and word != "!" and word != "&" and word != ":" and word != "_"\
                    and word != "the" and word != "and" and word != "a" and word != "i" and word != "to" and word != "of" and word != "this" and word != "that" and word != "it"\
                    and word != "in" and word != "for" and word != "you" and word != "with" and word != "on" and word != "at" and word != "an" and word != "we" and word != "he" and word != "she"\
                    and word != "they" and word.find("https") == -1 and word.find("http") == -1:
                new_word = smoother_function(word)
                # print(word)
                if new_word != ".":
                    temp_list.append(new_word)
        main_list.append((list_to_dict_converter(temp_list), data_tag))
        line_counter += 1
        print(str(line_counter))
    input_file.close()
    return main_list

# This function loads the negative and positive dictionaries
def dictionary_loader():
    print("Loading dictionaries...")
    positive_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Naive Bayes//Unigram//Dictionaries//unigram_positive_dictionary.txt"
    negative_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Naive Bayes//Unigram//Dictionaries//unigram_negative_dictionary.txt"
    positive_dictionary_file = open(positive_dictionary_address, "rt")
    negative_dictionary_file = open(negative_dictionary_address, "rt")
    positive_dictionary = {}
    negative_dictionary = {}
    total_number_of_negative_words = 0
    total_number_of_positive_words = 0

    # Loading positive dictionary
    while True:
        line = positive_dictionary_file.readline()
        if line == "":
            break
        index = line.find(" ")
        line_list = list(line)
        i = 0
        word = ""
        while i < index:
            word += line_list[i]
            i += 1
        i = 1
        while i <= 30:
            line_list.pop(0)
            i += 1
        count = ""
        i = 0
        while i < len(line_list):
            count += line_list[i]
            i += 1
        count = int(count)
        positive_dictionary[word] = count
        total_number_of_positive_words += count


    # Loading negative dictionary
    while True:
        line = negative_dictionary_file.readline()
        if line == "":
            break
        index = line.find(" ")
        line_list = list(line)
        i = 0
        word = ""
        while i < index:
            word += line_list[i]
            i += 1
        i = 1
        while i <= 30:
            line_list.pop(0)
            i += 1
        count = ""
        i = 0
        while i < len(line_list):
            count += line_list[i]
            i += 1
        count = int(count)
        negative_dictionary[word] = count
        total_number_of_negative_words += count

    print("The length of positive tweets dictionary is: " + str(len(positive_dictionary)))
    print("Total number of words in positive words dictionary is: " + str(total_number_of_positive_words))
    print("The length of negative tweets dictionary is: " + str(len(negative_dictionary)))
    print("Total number of words in negative words dictionary is: " + str(total_number_of_negative_words))
    # print("The length of neutral tweets dictionary is: " + str(len(neutral_dictionary)))
    # print("Total number of words in neutral words dictionary is: " + str(total_number_of_neutral_words))
    print("==============================================================================")
    return positive_dictionary, negative_dictionary, total_number_of_positive_words, total_number_of_negative_words


# This function counts unique words in both positive and negative dictionaries
def unique_words_counter(input_positive_dictionary, input_negative_dictionary):
    sorted_positive_list = sorted(input_positive_dictionary.items(), key=lambda x: x[1], reverse=True)
    sorted_negative_list = sorted(input_negative_dictionary.items(), key=lambda x: x[1], reverse=True)
    counter = 0
    for word in sorted_positive_list:
        if word[1] == 1:
            counter += 1
    for word in sorted_negative_list:
        if word[1] == 1:
            counter += 1
    return counter


# Main part of the code starts here
# Loading the saved trained model
model_file = open("MaximumEntropyClassifier", "rb")
classifier = pickle.load(model_file)
model_file.close()

# Generating the test list for positive test tweets
positive_test_tweets_address = "C://Users//user//Desktop//New Dataset 3//Test//positive_test.txt"
test_list = nltk_input_list_generator(positive_test_tweets_address, 1, [])
print("The length of test list for positive test tweets is: " + str(len(test_list)))

# Evaluating the model for positive tweets
print("Evaluating the model for positive test tweets...")
true_categorization = 0
total_positive_test_tweets = len(test_list)
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    if main_label == predicted_label:
        true_categorization += 1
print("The precision of the model for positive tweets is: " + str(round((true_categorization / total_positive_test_tweets) * 100, 2)) + " %")

# Generating the test list for negative test tweets
negative_test_tweets_address = "C://Users//user//Desktop//New Dataset 3//Test//negative_test.txt"
test_list = nltk_input_list_generator(negative_test_tweets_address, -1, [])
print("The length of test list for negative test tweets is: " + str(len(test_list)))

# Evaluating the model for negative tweets
print("Evaluating the model for negative test tweets...")
true_categorization = 0
total_negative_test_tweets = len(test_list)
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    print("main_label: " + str(main_label) + "    predicted_label: " + str(predicted_label))
    if main_label == predicted_label:
        true_categorization += 1
print("The precision of the model for negative tweets is: " + str(round((true_categorization / total_negative_test_tweets) * 100, 2)) + " %")

# Generating the test list for neutral test tweets
neutral_test_tweets_address = "C://Users//user//Desktop//New Dataset 3//Test//neutral_test.txt"
test_list = nltk_input_list_generator(neutral_test_tweets_address, 0, [])
print("The length of test list for neutral test tweets is: " + str(len(test_list)))

# Evaluating the model for neutral tweets
print("Evaluating the model for neutral test tweets...")
true_categorization = 0
total_neutral_test_tweets = len(test_list)
for tweet_tuple in test_list:
    tweet_word_dictionary = tweet_tuple[0]
    main_label = tweet_tuple[1]
    predicted_label = classifier.classify(tweet_word_dictionary)
    if main_label == predicted_label:
        true_categorization += 1
print("The precision of the model for neutral tweets is: " + str(round((true_categorization / total_neutral_test_tweets) * 100, 2)) + " %")
