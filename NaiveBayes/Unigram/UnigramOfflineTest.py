import math

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
    input_comment = input_comment.replace("\"", "")
    input_comment = input_comment.replace("\'", "")
    input_comment = input_comment.replace("(", "")
    input_comment = input_comment.replace("\n", "")
    return input_comment



# This function loads the negative and positive dictionaries
def dictionary_loader():
    print("Loading dictionaries...")
    positive_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Naive Bayes//Unigram//Dictionaries//unigram_positive_dictionary.txt"
    negative_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Naive Bayes//Unigram//Dictionaries//unigram_negative_dictionary.txt"
    neutral_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Naive Bayes//Unigram//Dictionaries//unigram_neutral_dictionary.txt"
    positive_dictionary_file = open(positive_dictionary_address, "rt")
    negative_dictionary_file = open(negative_dictionary_address, "rt")
    neutral_dictionary_file = open(neutral_dictionary_address, "rt")
    positive_dictionary = {}
    negative_dictionary = {}
    neutral_dictionary = {}
    total_number_of_negative_words = 0
    total_number_of_positive_words = 0
    total_number_of_neutral_words = 0

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

    # Loading neutral dictionary
    while True:
        line = neutral_dictionary_file.readline()
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
        neutral_dictionary[word] = count
        total_number_of_neutral_words += count


    print("The length of positive tweets dictionary is: " + str(len(positive_dictionary)))
    print("Total number of words in positive words dictionary is: " + str(total_number_of_positive_words))
    print("The length of negative tweets dictionary is: " + str(len(negative_dictionary)))
    print("Total number of words in negative words dictionary is: " + str(total_number_of_negative_words))
    print("The length of neutral tweets dictionary is: " + str(len(neutral_dictionary)))
    print("Total number of words in neutral words dictionary is: " + str(total_number_of_neutral_words))
    print("==============================================================================")
    return positive_dictionary, negative_dictionary, neutral_dictionary, total_number_of_positive_words, total_number_of_negative_words, total_number_of_neutral_words



# Main part of the code starts here
positive_comments_dictionary, negative_comments_dictionary, neutral_comments_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words, total_number_of_neutral_dictionary_words = dictionary_loader()

# Unigram Naive Bayes method implementation
# Negative comments test implementation
print("Processing comments file...")
negative_test_comments_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Internship//Project//Final Decision Files//Amazon Dataset//Test Data//Negative Test Comments//Negative Test Comments.txt"
negative_test_comments_file = open(negative_test_comments_file_address, "rt", encoding="utf8")
negative_result_file = open("negative_result.txt", "wt")
comments_counter = 0
true_categorization = 0
while True:
    comment = negative_test_comments_file.readline().lower()
    if comment == "":
        break


    comment = comment_smoother(comment)
    words_list = comment.split(" ")
    negative_result = 0
    positive_result = 0
    for word in words_list:
        if word in negative_comments_dictionary:
            negative_result = negative_result + math.log10(negative_comments_dictionary[word] / total_number_of_negative_dictionary_words)
        if word in positive_comments_dictionary:
            positive_result = positive_result + math.log10(positive_comments_dictionary[word] / total_number_of_positive_dictionary_words)
    if negative_result < positive_result:
        negative_result_file.write("Positive\n")
    if positive_result < negative_result:
        negative_result_file.write("Negative\n")
        true_categorization += 1
    if positive_result == negative_result:
        negative_result_file.write("Neutral\n")
    comments_counter += 1

negative_comments_precision = round((true_categorization / comments_counter) * 100, 2)
total_negative_comments = comments_counter
negative_test_comments_file.close()
negative_result_file.close()


# Positive comments test implementation
positive_test_comments_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Internship//Project//Final Decision Files//Amazon Dataset//Test Data//Positive Test Comments//Positive Test Comments.txt"
positive_test_comments_file = open(positive_test_comments_file_address, "rt", encoding="utf8")
positive_result_file = open("positive_result.txt", "wt")
comments_counter = 0
true_categorization = 0
while True:
    comment = positive_test_comments_file.readline()
    if comment == "":
        break
    comment = comment_smoother(comment)
    words_list = comment.split(" ")
    negative_result = 0
    positive_result = 0
    for word in words_list:
        if word in negative_comments_dictionary:
            negative_result = negative_result + math.log10(negative_comments_dictionary[word] / total_number_of_negative_dictionary_words)
        if word in positive_comments_dictionary:
            positive_result = positive_result + math.log10(positive_comments_dictionary[word] / total_number_of_positive_dictionary_words)
    if negative_result < positive_result:
        positive_result_file.write("Positive\n")
        true_categorization += 1
    if positive_result < negative_result:
        positive_result_file.write("Negative\n")
    if positive_result == negative_result:
        positive_result_file.write("Neutral\n")

    comments_counter += 1

positive_comments_precision = round((true_categorization / comments_counter) * 100, 2)
total_positive_comments = comments_counter
positive_test_comments_file.close()
positive_result_file.close()

print("Total number of positive comments: " + str(total_positive_comments))
print("Positive comments precision: " + str(positive_comments_precision) + " %")
print("==============================================================================")
print("Total number of negative comments: " + str(total_negative_comments))
print("Negative comments precision: " + str(negative_comments_precision) + " %")

























