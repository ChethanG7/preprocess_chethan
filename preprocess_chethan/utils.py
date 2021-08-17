import re
import os
import sys

import pandas as pd
import numpy as np
import spacy 
from spacy.lang.en.stop_words import STOP_WORDS
from bs4 import BeautifulSoup
import unicodedata
from textblob import TextBlob

nlp = spacy.load('en_core_web_sm')


def _get_wordcounts(x):
	length = len(str(x).split())
	return length

def _get_charcounts(x):
	char_length = len(''. join(s for s in x.split()))
	return char_length

def _get_avg_wordlength(x):
	count = _get_charcounts(x)/_get_wordcounts(x)
	return count

def _get_stopwords_count(x):
	stop_count = len([s for s in x.split() if s in stopwords])
	return stop_count

def _get_hashtag_count(x):
	hash_count = len([h for h in x.split() if h.startswith('#')])
	return hash_count

def _get_mention_count(x):
	mention_count = len([h for h in x.split() if h.startswith('@')])
	return mention_count

def _get_digit_count(x):
	digit_count = len([n for n in x.split() if n.isdigit()])
	return digit_count

def _get_uppercase_count(x):
	uppercase_count = len([n for n in x.split() if n.isupper()])
	return uppercase_count

def _get_cont_exp(x):
	contractions = { 
	"ain't": "am not",
	"aren't": "are not",
	"can't": "cannot",
	"can't've": "cannot have",
	"'cause": "because",
	"could've": "could have",
	"couldn't": "could not",
	"couldn't've": "could not have",
	"didn't": "did not",
	"doesn't": "does not",
	"don't": "do not",
	"hadn't": "had not",
	"hadn't've": "had not have",
	"hasn't": "has not",
	"haven't": "have not",
	"he'd": "he would",
	"he'd've": "he would have",
	"he'll": "he will",
	"he'll've": "he will have",
	"he's": "he is",
	"how'd": "how did",
	"how'd'y": "how do you",
	"how'll": "how will",
	"how's": "how does",
	"i'd": "i would",
	"i'd've": "i would have",
	"i'll": "i will",
	"i'll've": "i will have",
	"i'm": "i am",
	"i've": "i have",
	"isn't": "is not",
	"it'd": "it would",
	"it'd've": "it would have",
	"it'll": "it will",
	"it'll've": "it will have",
	"it's": "it is",
	"let's": "let us",
	"ma'am": "madam",
	"mayn't": "may not",
	"might've": "might have",
	"mightn't": "might not",
	"mightn't've": "might not have",
	"must've": "must have",
	"mustn't": "must not",
	"mustn't've": "must not have",
	"needn't": "need not",
	"needn't've": "need not have",
	"o'clock": "of the clock",
	"oughtn't": "ought not",
	"oughtn't've": "ought not have",
	"shan't": "shall not",
	"sha'n't": "shall not",
	"shan't've": "shall not have",
	"she'd": "she would",
	"she'd've": "she would have",
	"she'll": "she will",
	"she'll've": "she will have",
	"she's": "she is",
	"should've": "should have",
	"shouldn't": "should not",
	"shouldn't've": "should not have",
	"so've": "so have",
	"so's": "so is",
	"that'd": "that would",
	"that'd've": "that would have",
	"that's": "that is",
	"there'd": "there would",
	"there'd've": "there would have",
	"there's": "there is",
	"they'd": "they would",
	"they'd've": "they would have",
	"they'll": "they will",
	"they'll've": "they will have",
	"they're": "they are",
	"they've": "they have",
	"to've": "to have",
	"wasn't": "was not",
	" u ": " you ",
	" ur ": " your ",
	" n ": " and ",
	"won't": "would not",
	'dis': 'this',
	'bak': 'back',
	'brng': 'bring'}

	if type(x) is str:
		for w in contractions:
			v = contractions[w]
			x = x.replace(w,v)
		return x
	else:
		return x 


def _get_emails(x):
	emails = re.findall(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)',x)
	emails_count = len(emails)

	return emails_count,emails

def _remove_emails(x):
	return re.sub(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)',"",x)

def _get_urls(x):
	url_flags = re.findall(r'(http|https|ftp|ssh)://([\\w_-]+(?:(?:\\.[\\w_-]+)+))([\\w.,@?^=%&:/~+#-]*[\\w@?^=%&/~+#-])?', x)
	url_count = len(url_flags)

	return url_count,url_flags

def _remove_urls(x):
	return re.sub(r'(http|https|ftp|ssh)://([\\w_-]+(?:(?:\\.[\\w_-]+)+))([\\w.,@?^=%&:/~+#-]*[\\w@?^=%&/~+#-])?','', x)

def _remove_rt(x):
	return re.sub(r'\brt\b','',x).strip()

def _remove_special_chars(x):
	x = re.sub(r'[^\w+ ]','',x)
	x = ' '.join(x.split()) #to remove multiple spaces
	return x

def _remove_html_tags(x):
	return BeautifulSoup(x,'lxml').get_text().strip()

def _remove_accented_chars(x):
	x = unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode('utf-8')

def _remove_stopwords(x):
	return  ' '.join([s for s in x.split() if s not in stopwords])

def _make_base_form(x):
	x = str(x)
	x_list =[]
	doc = nlp(x)
	
	for t in doc:
		lemma = t.lemma_
		if lemma=='be' or lemma== '-PRON-':
			lemma=t.text

		x_list.append(lemma)
	return ' '.join(x_list)

def _remove_common_words(x,n=20):
	text = x.split()
	word_freq = pd.Series(text).value_counts()
	fre = word_freq[:n]

	x = ' '.join([t for t in x.split() if t not in fre])
	return x

def _remove_rare_words(x,n=20):
	text = x.split()
	word_freq = pd.Series(text).value_counts()
	less_freq = word_freq.tail(n)

	x = ' '.join([t for t in x.split() if t not in less_freq])
	return x

def _spelling_correction(x):
	x = TextBlob(x).correct()
	return x

