import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.data.path.append('nltk_data')

# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('stopwords')

def FindAcc(S1, S2):
    X = S1.lower()
    Y = S2.lower()

    S1 = re.split(r'[ ,.!;"()]', X)
    S2 = re.split(r'[ ,.!;"()]', Y)

    S1.sort()
    S2.sort()

    Positive = 0
    Negative = 0

    for i in S1:
        if i == "":
            continue

        if i in S2:
            Positive += 1
        else:
            Negative += 1

    Total = Positive + Negative

    AccPer = (Positive * 100) / Total

    X_list = word_tokenize(X)
    Y_list = word_tokenize(Y)

    sw = stopwords.words("english")
    l1 = []
    l2 = []

    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}

    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)

    cosine *= 100

    if min(AccPer, (cosine)) < 40:
        AccPer = min(AccPer, cosine)
    else:
        AccPer = max(AccPer, cosine)
    return AccPer



# Test Cases
# X is Predefined answer
# Y is recorded answer


# Test Case 1
# X = "Python is a high-level, general-purpose, and very popular programming language. Python programming language is being used in web development, Machine Learning applications, along with all cutting-edge technology in Software Industry."
# Y = "Python is serpent animal"
# Accuracy:  13.333333333333334


# Test Case 2
# X = "Python is a high-level, general-purpose, and very popular programming language. Python programming language is being used in web development, Machine Learning applications, along with all cutting-edge technology in Software Industry."
# Y = "Python is high-level programming langauge, used for web development and in AI also."
# Accuracy:  43.333333333333336

# Test case 3
# X = "Prime Minister of India is Modi"
# Y = "Modi is Prime Minister of India"
# Accuracy:  100.0

# Test case 4
# X = "HTML stands for Hypertext Markup Language. It is the most basic language, and simple to learn and modify. It is a combination of both hypertext and markup language. It contains the elements that can change/develop a web page’s look and the displayed contents."
# Y = "HTML stands for Hypertext Markup Language."
# Accuracy:  13.953488372093023

# Test case 5
# X = "HTML stands for Hypertext Markup Language. It is the most basic language, and simple to learn and modify. It is a combination of both hypertext and markup language. It contains the elements that can change/develop a web page’s look and the displayed contents."
# Y = "HTML stands for Hypertext Markup Language. It is simple to learn and modify. It contains the elements that can change/develop a web page’s look and the displayed contents."
# Accuracy:  79.06976744186046

# Test case 6
# X = "Python is a high-level, general-purpose, and very popular programming language. Python programming language is being used in web development, Machine Learning applications, along with all cutting-edge technology in Software Industry."
# Y = "Python is high-level programming langauge, used for web development and in AI along with all cutting-edge technology in Software Industry."
# Accuracy:  66.66666666666667

# Test case 7
# X = "HTML stands for Hypertext Markup Language."
# Y = "HTML stands for Hypertext Markup Language. It is the most basic language, and simple to learn and modify. It is a combination of both hypertext and markup language. It contains the elements that can change/develop a web page’s look and the displayed contents."
# Accuracy:  100.0

# Test Case 8
# X = "Python is high-level programming langauge, used for web development and in AI also."
# Y = "Python is a high-level, general-purpose, and very popular programming language. Python programming language is being used in web development, Machine Learning applications, along with all cutting-edge technology in Software Industry."
# Accuracy:  69.23076923076923

# Test Case 9
# X = "HTML stands for Hypertext Markup Language. It is the most basic language, and simple to learn and modify. It is a combination of both hypertext and markup language. It contains the elements that can change/develop a web page’s look and the displayed contents."
# Y = "HTML (HyperText Markup Language) is the most basic building block of the Web. It defines the meaning and structure of web content. Other technologies besides HTML are generally used to describe a web page's appearance/presentation (CSS) or functionality/behavior (JavaScript)."
# Accuracy:  51.16279069767442
