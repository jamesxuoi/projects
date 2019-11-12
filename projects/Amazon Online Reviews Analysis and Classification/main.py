import argparse
import pickle
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup  
import re
import nltk
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk import sent_tokenize, word_tokenize, pos_tag
import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")


print('Please INPUT your review:')
INPUT_SENTENCE = input()

def cleanText(raw_text, remove_stopwords=False, stemming=False, split_text=False, \
             ):
    '''
    Convert a raw review to a cleaned review
    ''' 
    text = BeautifulSoup(raw_text, 'lxml').get_text()  #remove html
    letters_only = re.sub("[^a-zA-Z]", " ", text)  # remove non-character
    words = letters_only.lower().split() # convert to lower case 
    
    return( " ".join(words))

def round_rate(rate):
	if rate <= 1.5:
		return 1
	elif rate > 1.5 and rate <= 2.5:
		return 2
	elif rate > 2.5 and rate <= 3.5:
		return 3
	elif rate > 3.5 and rate <= 4.5:
		return 4
	else:
		return 5

def sentiment(rate):
	if rate < 2.5:
		return "Negative"
	elif rate >= 2.5 and rate <= 3.5:
		return "Neutral"
	else:
		return "Positive"

if __name__ == '__main__':

	if INPUT_SENTENCE == "":
		print("Please INPUT your sentence!")
	else: 

		model = pickle.load(open('./model/LR-amazon.sav', 'rb'))
		tfidf = pickle.load(open('./model/tfidf.sav', 'rb'))

		da = model.predict_proba(tfidf.transform([cleanText(INPUT_SENTENCE)]))
		hardda = model.predict(tfidf.transform([cleanText(INPUT_SENTENCE)]))
		cc = 0
		for i,so in enumerate(da[0]):
		    cc = cc + ((i+1)*so)
		print("\n ################################################### THE RESULTS ####################################################")
		print("Input sentence: '" + INPUT_SENTENCE +"'")
		print("The probability distribution of predicted rating:")
		print("- 1 star: " + str(round(da[0][0],2)))
		print("- 2 stars: " + str(round(da[0][1],2)))
		print("- 3 stars: " + str(round(da[0][2],2)))
		print("- 4 stars: " + str(round(da[0][3],2)))
		print("- 5 stars: " + str(round(da[0][4],2)))

		print("Hard threshold predicted Rating: " + str(hardda[0]))
		print("Average predicted Rating: " + str(round(cc,2)))

		print("Rounded predicted Rating: " + str(round_rate(round(cc,2))))

		print("Sentiment of review: " + sentiment(cc))

