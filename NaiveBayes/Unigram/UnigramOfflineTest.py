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
    input_comment = input_comment.replace("(", "")
    input_comment = input_comment.replace("\n", "")
    return input_comment


# This function receives a list which is sorted by sorted function and produces the output dictionary file
def sorted_dictionary_printer(input_list, output_address, category):
    output_dictionary_file = open(output_address, "wt")
    for word in input_list:
        output_dictionary_file.write(word[0] + " " * (30 - len(word[0])) + str(word[1]) + "\n")
    output_dictionary_file.close()


# This function loads the negative and positive dictionaries
def dictionary_loader():
    print("Loading dictionaries...")
    positive_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Naive Bayes//Unigram//Dictionaries//unigram_positive_dictionary.txt"
    negative_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Naive Bayes//Unigram//Dictionaries//unigram_negative_dictionary.txt"
    # neutral_dictionary_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Naive Bayes//Unigram//Dictionaries//unigram_neutral_dictionary.txt"
    positive_dictionary_file = open(positive_dictionary_address, "rt")
    negative_dictionary_file = open(negative_dictionary_address, "rt")
    # neutral_dictionary_file = open(neutral_dictionary_address, "rt", encoding="utf8")
    positive_dictionary = {}
    negative_dictionary = {}
    neutral_dictionary = {}
    total_number_of_negative_words = 0
    total_number_of_positive_words = 0
    # total_number_of_neutral_words = 0

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
    # while True:
    #     line = neutral_dictionary_file.readline()
    #     if line == "":
    #         break
    #     index = line.find(" ")
    #     line_list = list(line)
    #     i = 0
    #     word = ""
    #     while i < index:
    #         word += line_list[i]
    #         i += 1
    #     i = 1
    #     while i <= 30:
    #         line_list.pop(0)
    #         i += 1
    #     count = ""
    #     i = 0
    #     while i < len(line_list):
    #         count += line_list[i]
    #         i += 1
    #     count = int(count)
    #     neutral_dictionary[word] = count
    #     total_number_of_neutral_words += count


    print("The length of positive tweets dictionary is: " + str(len(positive_dictionary)))
    print("Total number of words in positive words dictionary is: " + str(total_number_of_positive_words))
    print("The length of negative tweets dictionary is: " + str(len(negative_dictionary)))
    print("Total number of words in negative words dictionary is: " + str(total_number_of_negative_words))
    # print("The length of neutral tweets dictionary is: " + str(len(neutral_dictionary)))
    # print("Total number of words in neutral words dictionary is: " + str(total_number_of_neutral_words))
    print("==============================================================================")
    return positive_dictionary, negative_dictionary, total_number_of_positive_words, total_number_of_negative_words



# Main part of the code starts here
positive_comments_dictionary, negative_comments_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words = dictionary_loader()
# Unigram Naive Bayes method implementation
# Negative comments test implementation
print("Processing test files...")
# t = total_number_of_positive_dictionary_words + total_number_of_negative_dictionary_words + total_number_of_neutral_dictionary_words
negative_test_comments_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Train Dataset for Twitter//Dataset//Complete Dataset//Test//negative_test_tweets.txt"
negative_test_comments_file = open(negative_test_comments_file_address, "rt")
negative_result_file = open("negative_result.txt", "wt")
comments_counter = 0
true_categorization = 0
while True:
    comment = negative_test_comments_file.readline().lower()
    if comment == "":
        break


    comment = comment_smoother(comment)
    words_list = comment.split(" ")
    # negative_result = 0
    # positive_result = 0
    final_result = 0
    for word in words_list:
        if word in positive_comments_dictionary:
            positive_numerator = positive_comments_dictionary[word] + 1
        else:
            positive_numerator = 1

        if word in negative_comments_dictionary:
            negative_numerator = negative_comments_dictionary[word] + 1
        else:
            negative_numerator = 1

        final_result += math.log10((positive_numerator / total_number_of_positive_dictionary_words) / (negative_numerator / total_number_of_negative_dictionary_words))






    negative_result_file.write(str(round(final_result, 2)) + "\n")
    comments_counter += 1

negative_comments_precision = round((true_categorization / comments_counter) * 100, 2)
total_negative_comments = comments_counter
negative_test_comments_file.close()
negative_result_file.close()


# Positive comments test implementation
positive_test_comments_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Train Dataset for Twitter//Dataset//Complete Dataset//Test//positive_test_tweets.txt"
positive_test_comments_file = open(positive_test_comments_file_address, "rt")
positive_result_file = open("positive_result.txt", "wt")
comments_counter = 0
true_categorization = 0
while True:
    comment = positive_test_comments_file.readline()
    if comment == "":
        break
    comment = comment_smoother(comment)
    words_list = comment.split(" ")
    # negative_result = 0
    # positive_result = 0
    # neutral_result = 0
    final_result = 0
    for word in words_list:
        if word in positive_comments_dictionary:
            positive_numerator = positive_comments_dictionary[word] + 1
        else:
            positive_numerator = 1

        if word in negative_comments_dictionary:
            negative_numerator = negative_comments_dictionary[word] + 1
        else:
            negative_numerator = 1

        final_result += math.log10((positive_numerator / total_number_of_positive_dictionary_words) / (negative_numerator / total_number_of_negative_dictionary_words))


    positive_result_file.write(str(round(final_result, 2)) + "\n")
    comments_counter += 1

positive_comments_precision = round((true_categorization / comments_counter) * 100, 2)
total_positive_comments = comments_counter
positive_test_comments_file.close()
positive_result_file.close()

# Neutral comments test implementation
neutral_test_comments_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Train Dataset for Twitter//Dataset//Complete Dataset//Test//neutral_test_tweets.txt"
neutral_test_comments_file = open(neutral_test_comments_file_address, "rt")
neutral_result_file = open("neutral_result.txt", "wt")
comments_counter = 0
true_categorization = 0
while True:
    comment = neutral_test_comments_file.readline()
    if comment == "":
        break
    comment = comment_smoother(comment)
    words_list = comment.split(" ")
    # negative_result = 0
    # positive_result = 0
    # neutral_result = 0
    final_result = 0
    for word in words_list:
        if word in positive_comments_dictionary:
            positive_numerator = positive_comments_dictionary[word] + 1
        else:
            positive_numerator = 1

        if word in negative_comments_dictionary:
            negative_numerator = negative_comments_dictionary[word] + 1
        else:
            negative_numerator = 1

        final_result += math.log10((positive_numerator / total_number_of_positive_dictionary_words) / (negative_numerator / total_number_of_negative_dictionary_words))



    neutral_result_file.write(str(round(final_result, 2)) + "\n")
    comments_counter += 1

neutral_comments_precision = round((true_categorization / comments_counter) * 100, 2)
total_neutral_comments = comments_counter
neutral_test_comments_file.close()
neutral_result_file.close()


print("Total number of positive test tweets: " + str(total_positive_comments))
print("Positive test tweets precision: " + str(positive_comments_precision) + " %")
print("==============================================================================")
print("Total number of negative test tweets: " + str(total_negative_comments))
print("Negative test tweets precision: " + str(negative_comments_precision) + " %")
print("==============================================================================")
print("Total number of neutral test tweets: " + str(total_neutral_comments))
print("Neutral test tweets precision: " + str(neutral_comments_precision) + " %")



