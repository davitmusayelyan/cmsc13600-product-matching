from core import *
import datetime

import array
import binascii
import random
import string

#words, two-words and n-grams of words
def find_ngrams(string, n):
	words = word_split(string)
	grams = []
	for w in words: 
		grams = grams + list(zip(*[w[i:] for i in range(n)]))
	return words+grams

#Jaccard Similarity
def tokenize(st):
    return set(st.lower().split())

#Jaccardian with words and n-grams
def jaccard_ngram(a,b, n):
	table = str.maketrans('', '', string.punctuation)
	Ta = set(find_ngrams(a.translate(table), n))
	Tb = set(find_ngrams(b.translate(table), n))
	return len(Ta.intersection(Tb))/len(Ta.union(Tb))

def jaccard(a, b):
	Ta = tokenize(a)
	Tb = tokenize(b)
	return len(Ta.intersection(Tb))/len(Ta.union(Tb))

#Splitting words
def word_split(title):
	table = str.maketrans('', '', string.punctuation)
	words = title.translate(table).split()
	return words

def price_split(title):
	words = title.split()
	return words[0]

#building the index
def build_index(collection):
	start = datetime.datetime.now()

	index = {}

	for t in collection:
		substrings=word_split(t["title"].lower())
		for s in substrings:
			if s not in index:
				index[s] = []

			index[s].append((t["id"], t["title"], t["price"]))
	print('build_index() elapsed time: ', (datetime.datetime.now()-start).total_seconds())

	return index


def find_index(query, index):

	query_grams = word_split(query)

	ids = []
	for g in query_grams:   #for each substring
		try:
			print
			ids.extend(index[g])
		except KeyError:
			continue

	return ids

def best_match(pairs, n, string, price):

	pairs = set(pairs)
	pairs = list(pairs)
	
	#filter out too different prices
	filtered_price = filter(lambda pair: abs(price - float(price_split(pair[2]))) <= 100 or price == 0, pairs)
	filtered_price = list(filtered_price)
	if len(filtered_price)==0:
		filtered_price = pairs

	#filter out too non-similar titles
	filtered_jacc = filter(lambda pair: jaccard(string, pair[1]) >= 0.30, filtered_price)
	filtered_jacc = list(filtered_jacc)
	if len(filtered_jacc)==0:
		filtered_jacc = pairs

	#sort based on jaccardian string similarity
	sorted_jacc = sorted(filtered_jacc, key = lambda pair: jaccard(string, pair[1]), reverse=True)
	
	#sort most similar ones (according to jaccardian) based on words and n-grams
	sorted_jacc_ngram = sorted(sorted_jacc[:15], key = lambda pair: jaccard_ngram(string, pair[1], 3), reverse=True)
	match = sorted_jacc_ngram[0]
	
	return match[0]

def match():
	my_matching = []
	amazon = amazon_catalog()
	google = google_catalog()
	index = build_index(google)

	for a in amazon:
		pairs = find_index(a["title"].lower(), index)
		if pairs != []:
			google_match = best_match(pairs, 100, a["title"].lower(), float(price_split(a["price"])))
			if google_match != None:
				my_matching.append((a["id"], google_match))

	return my_matching