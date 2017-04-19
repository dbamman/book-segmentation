import re
from math import sqrt
import math

class TextTiling:


	def cosine(self, one, onecount, two, twocount):
		# print one, two
		num=0.
		onesum=0.
		twosum=0.
		for key in one:
			if key in two:
		#		print (two[key]/twocount)
				num+=(one[key]/onecount) * (two[key]/twocount)
			onesum+=(one[key]/onecount) * (one[key]/onecount)

		for key in two:
			twosum+=(two[key]/twocount) * (two[key]/twocount)

		return num/(sqrt(onesum)*sqrt(twosum))

	def extractFeatures(self, pages, pagenums):
		tokfeats={}
		for i in range(len(pages)):
			pagenum=pagenums[i]
			tokfeats[pagenum]={}
			
		for i in range(len(pages)):
			pagenum=pagenums[i]
			text=""
			lines=pages[i]
			for line in lines:
				text+=line.rstrip() + " "

			newtext=re.sub("[\\.,;:!\\?\\(\\)\\[\\]\\-]", "", text.lower())

			tokens=re.split("\s+", newtext)

			for token in tokens:
				t = "%s" % token.lower()
				if t not in tokfeats[pagenum]:
					tokfeats[pagenum][t]=0
				tokfeats[pagenum][t] += 1


		feats={}
		for i in range(len(pages)):
			pagenum=pagenums[i]
			feats[pagenum]={}
		
		ordered=sorted(tokfeats.keys())
		revordered={}
		for i in range(len(ordered)):
			revordered[ordered[i]]=i

		# print ordered
		
		prevToks={}
		prevCount=0
		nextToks={}
		nextCount=0

		# index=ordered[0]
		# for feat in tokfeats[index]:
		# 	if feat not in prevToks:
		# 		prevToks[feat]=0.

		# 	prevToks[feat]+=1
		# 	prevCount+=1

		for i in range(0,len(ordered)):
			index=ordered[i]
			for feat in tokfeats[index]:
				if feat not in nextToks:
					nextToks[feat]=0.

				nextToks[feat]+=1
				nextCount+=1		


		for i in range(0,len(ordered)-1):
			index=ordered[i]
			for feat in tokfeats[index]:

				nextToks[feat]-=1
				nextCount-=1	

				if feat not in prevToks:
					prevToks[feat]=0.

				prevToks[feat]+=1
				prevCount+=1

			cos=self.cosine(prevToks, prevCount, nextToks, nextCount)
			# print cos
			feats[index]["textiling"]=float("%.3f" % (cos))
			feats[index]["textiling:present"]=1

		return feats
