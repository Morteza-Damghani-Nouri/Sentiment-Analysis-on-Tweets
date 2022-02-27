import math
from Commons import comment_smoother
from Commons import dictionary_loader
from Commons import unique_words_counter


# Main part of the code starts here
positive_comments_dictionary, negative_comments_dictionary, total_number_of_positive_dictionary_words, total_number_of_negative_dictionary_words = dictionary_loader()
# Unigram Naive Bayes method implementation
# Negative comments test implementation
negative_test_comments_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//negative_test.txt"
negative_test_comments_file = open(negative_test_comments_file_address, "rt", encoding="utf8")
comments_counter = 0
true_categorization = 0
number_of_unique_words = unique_words_counter(positive_comments_dictionary, negative_comments_dictionary)
while True:
    comment = negative_test_comments_file.readline().lower()
    if comment == "":
        break


    comment = comment_smoother(comment)
    words_list = comment.split(" ")
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

        final_result += math.log10((positive_numerator / (total_number_of_positive_dictionary_words + number_of_unique_words)) / (negative_numerator / (total_number_of_negative_dictionary_words + number_of_unique_words)))

    if final_result < 0:
        true_categorization += 1
    comments_counter += 1

negative_comments_precision = round((true_categorization / comments_counter) * 100, 2)
total_negative_comments = comments_counter
negative_test_comments_file.close()

# Positive comments test implementation
positive_test_comments_file_address = "E://MortezaDamghaniNouri//Computer Engineering//Semesters//9//Computer Engineering Final Project//Final Decision Files//Dataset//Test//positive_test.txt"
positive_test_comments_file = open(positive_test_comments_file_address, "rt", encoding="utf8")
comments_counter = 0
true_categorization = 0
while True:
    comment = positive_test_comments_file.readline()
    if comment == "":
        break
    comment = comment_smoother(comment)
    words_list = comment.split(" ")
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

        final_result += math.log10((positive_numerator / (total_number_of_positive_dictionary_words + number_of_unique_words)) / (negative_numerator / (total_number_of_negative_dictionary_words + number_of_unique_words)))

    if final_result > 0:
        true_categorization += 1
    comments_counter += 1


positive_comments_precision = round((true_categorization / comments_counter) * 100, 2)
total_positive_comments = comments_counter
positive_test_comments_file.close()

print("Total number of positive test tweets: " + str(total_positive_comments))
print("Positive test tweets precision: " + str(positive_comments_precision) + " %")
print("==============================================================================")
print("Total number of negative test tweets: " + str(total_negative_comments))
print("Negative test tweets precision: " + str(negative_comments_precision) + " %")




