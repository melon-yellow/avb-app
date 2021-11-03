
#################################################################################################################################################

import os
import re
import yaml
import nltk
nltk.download('rslp')
from nltk.stem import RSLPStemmer

#################################################################################################################################################

expression = '[!-@[-`{-¿ÆÐÑ×ØÝ-ßä-æëðñö-øý-ÿ]'
stemmer = RSLPStemmer()

#################################################################################################################################################

# Get Actual File Directory
fileDir = os.path.dirname(os.path.abspath(__file__))
wordsPath = os.path.abspath(os.path.join(fileDir, './words.nlp'))

#################################################################################################################################################

#Carrega o Corpus Words
def LoadMemory():
    words = open(wordsPath, 'r').read()
    words = yaml.safe_load(words)
    return words

#Função responsavel por calcular a pontuação por classe
def calculate_class_score(sentence,class_name):
    score = 0
    sentence = re.sub(expression, '', sentence)
    sentence = nltk.word_tokenize(sentence)
    for word in sentence:
        try:
            if stemmer.stem(word.lower()) in corpus_words[class_name]:
                score += corpus_words[class_name][stemmer.stem(word.lower())]
        except: pass
    return score

#Função responsavel por classificar a frase
def classifique(sentence):
    high_class = None
    high_score = 0
    prox = list()
    item = dict()
    for c in list(corpus_words.keys()):
        score = calculate_class_score(sentence, c)
        if score > high_score:
            high_class = c
            high_score = score
        if(score > 0):
            item[c] = score
    return item

memory = LoadMemory()
corpus_words = memory

#################################################################################################################################################
