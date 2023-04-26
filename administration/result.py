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

# nltk.download('word_tokenize')

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

import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def FindAcc2(S1, S2):
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
    # elif AccPer - cosine > 20:
    # AccPer = cosine
    else:
        AccPer = max(AccPer, cosine)

    if (not ("not" in S1 and "not" in S2)) and ("not" in S1 or "not" in S2):
        AccPer = 100 - AccPer

    return AccPer
