import re
import pymorphy2
import collections
import math

morph = pymorphy2.MorphAnalyzer()

def parseText(text):
    # разбиваем на токены
    tokens = re.findall(r'\w+', text)  # Разбиваем на токены
    # Изнаём количество слов
    tokensCount = len(tokens)

    words = []  # Словарь, куда будут записываться уникальные значимые слова
    for token in tokens:
        # получаем информацию о слове
        word_info = morph.parse(token)[0]
        # отсеивание служебных частей речи
        # отбрасываем предлоги, союзы, частицы и междометия)
        if word_info.tag.POS != 'PREP' \
            and word_info.tag.POS != 'CONJ' \
            and word_info.tag.POS != 'PRCL' \
            and word_info.tag.POS != 'INTJ':

            words.append(word_info.normal_form)

            # приверяем, встречалось ли уже слово
            # if words.get(word_info.normal_form) == None:
            #     #  если не встречалось, добавляем в словарь
            #     words[word_info.normal_form] = 1
            # else:
            #     # если встречалось, инккрементируем количество
            #     words[word_info.normal_form] = words.get(word_info.normal_form) + 1

    return words, tokensCount

def textAnalysis(words):
    return len(words)

def compute_tf(text):
    tf_text = collections.Counter(text)
    for i in tf_text:
        # для каждого слова в tf_text считаем TF путём деления
        # встречаемости слова на общее количество слов в тексте
        tf_text[i] = tf_text[i] / float(len(text))
    # возвращаем объект типа Counter c TF всех слов текста
    return tf_text

def compute_idf(word, corpus):
    # насколько часто слово встречается в текстах
    D = len(corpus)
    sum = 0
    for i in corpus:
        if word in i:
            sum += 1
    idf = math.log10(D/sum)
    return idf

def tf_idf(corpus):
    documents_list = []
    for text in corpus:
        tf_idf_dictionary = {}
        computed_tf = compute_tf(text)
        for word in computed_tf:
            tf_idf_dictionary[word] = computed_tf[word] * compute_idf(word, corpus)
        documents_list.append(tf_idf_dictionary)

    return documents_list
#
# data1 = {'group_name': 'abc', 'song_title': 'cba', 'text': ['a', 'b', 'c', 'a']}
# data2 = {'group_name': 'def', 'song_title': 'fed', 'text': ['a', 'd', 'e', 'c']}
# data = [data1, data2]
#
# corpus = []
# for d in data:
#     corpus.append(d['text'])
# print(corpus)
#
# res = tf_idf(corpus)
# print(res)


