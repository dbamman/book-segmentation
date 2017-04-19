import re

class NgramCounter:

		
	def extractFeatures(self, pages, pagenums):
		feats=[]
		for i in range(len(pages)):
			feats.append({})
			
		for i in range(len(pages)):
			
			text=""
			lines=pages[i]
			for line in lines:
				text+=line.rstrip() + " "

			newtext=re.sub("[\\.,;:!\\?\\(\\)\\[\\]\\-]", "", text.lower())

			tokens=re.split("\s+", newtext)

			for token in tokens:
				t = "ngram:ngram_%s" % token.lower()
				if t not in feats[i]:
					feats[i][t]=0
				feats[i][t] += 1

			for j in range(1, len(tokens)):
				t="ngram:bigram_%s_%s" % (tokens[j-1], tokens[j])
				if t not in feats[i]:
					feats[i][t]=0
				feats[i][t] += 1

			# trigrams
			for j in range(2, len(tokens)):
				t="ngram:trigram_%s_%s_%s" % (tokens[j-2], tokens[j-1], tokens[j])
				if t not in feats[i]:
					feats[i][t]=0
				feats[i][t] += 1

		return feats
