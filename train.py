import nltk 
import re
import yaml
from nltk.stem import RSLPStemmer

stemmer = RSLPStemmer()
expression = '[!-@[-`{-¿ÆÐÑ×ØÝ-ßä-æëðñö-øý-ÿ]'

#Carrega o Corpus Words
def LoadMemory():
    fileW = open("words.nlp", 'r')
    words = fileW.read()
    fileW.close()
    words = yaml.load(words)
    return words

#Carrega as frases que foram treinadas
def LoadExamples():
    fileE = open("examples.nlp", 'r')
    examples = yaml.load(fileE.read())
    fileE.close()
    return examples

#Salva a corpus words
def SaveMemory(w):
    fileW = open("words.nlp", 'w')
    fileW.write(str(w))
    fileW.close()

#Salva as novas frases treinadas
def SaveExample(example):
    fileE = open("examples.nlp", 'a')
    #yaml.dump(example, fileE)#
    fileE.write(example + "\n")
    fileE.close()

#Massa de dados para exemplo
def Examples():
    training_data = []
    training_data.append({"class":"ntm", "sentence":"bloco acabador ntm gaiola interstand discos guia roletada agua breakout box"})
    training_data.append({"class":"coilplate", "sentence":"coilplate braÇo foguete"})
    training_data.append({"class":"stelmor", "sentence":"stelmor mesa primeira cabeca ventiladores ultima"})
    training_data.append({"class":"produção", "sentence":"enviar qual produção mandar dizer falar quanto"})
    training_data.append({"class":"hoje", "sentence":"agora nesse momento instante da hora hoje hoje"})
    training_data.append({"class":"ontem", "sentence":"dia de ontem ontem"})
        
    Learning(training_data)

#Função responsavel por treinar a frase
def Learning(training_data):
    corpus_words = LoadMemory()
    for data in training_data:
        examples = LoadExamples()
        sentence = data['sentence']
        sentence = re.sub(expression, '', sentence)
        sentence = sentence.lower()
        sentence = sentence.split()
        d = list()
        for c in sentence:
            d.append(stemmer.stem(c))
        sentence = " ".join(d)
        if sentence in examples:
            continue
        SaveExample(sentence)
        sentence = nltk.word_tokenize(sentence)
        class_name = data['class']
        if class_name not in list(corpus_words.keys()):
            corpus_words[class_name] = {}
        for word in sentence:
            if word not in list(corpus_words[class_name].keys()):
                corpus_words[class_name][word] = 1
            else:
                corpus_words[class_name][word] += 1
    
    SaveMemory(corpus_words)
