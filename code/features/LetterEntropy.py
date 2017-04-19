import numpy as np,re
from math import sqrt

class LetterEntropy:

	def __init__(self):
		self.totals=[]
		self.n=0

	def procpage(self, page):
		dist=np.ones(26)
		words=re.split("\s+", page.rstrip())
		for w in words:
			w=w.lower()
			if len(w) > 1:
				init=w[0]
				if re.match("[a-z]", init) != None:
					dist[ord(init)-97]+=1
		# print dist
		return dist

	def extractFeatures(self, pages, pagenums):
		feats=[]
		letterDists=[]

		for i in range(len(pages)):
			feats.append({})
			
		for i in range(len(pages)):

			text=""
			lines=pages[i]
			for idx, line in enumerate(lines):
				text+=line.rstrip()

			dist=self.procpage(text)
			self.totals.append(dist)
			letterDists.append(dist)

		dists=np.array(self.totals)
		self.avgs=np.mean(dists, axis=0)/np.sum(np.mean(dists, axis=0))

		# print self.avgs, dists

		for i in range(len(pages)):

			dist=letterDists[i]

			sigs={}

			prob=dist/np.sum(dist)
			sigs=[]
			for j in range(26):
				z=(prob[j]-self.avgs[j])/sqrt((self.avgs[j] * (1-self.avgs[j])) / dist[j])

				if z > 1.65:
					sigs.append(j)

			feats[i]["letter_entropy:1"]=int(len(sigs) > 0)
			feats[i]["letter_entropy:2"]=int(len(sigs) > 1)


		return feats
