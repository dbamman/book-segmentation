import sys,re
import zipfile
import numpy as np
from scipy.stats import spearmanr
from math import sqrt
from random import shuffle

class Alphabetical:


	def extractFeatures(self, pages, pagenums):
		
		feats=[]
		for i in range(len(pages)):
			feats.append({})


		for i in range(len(pages)):

			text=""
			lines=pages[i]

			lineidx=[]
			alllines=[]
			sortlines=[]
			j=0
			for idx, line in enumerate(lines):
				if re.search("\w", line) != None:
					lineidx.append(j)
					j+=1
					alllines.append(line)
					text+="%s\t%s\n" % (idx, line)

			srt=[]
			for k,v in sorted(enumerate(alllines), key=lambda x:x[1]):
				sortlines.append(k)
				srt.append("%s\t%s" % (k,v))

				# print k
			# print lineidx, sortlines
			(spearman, pval)=spearmanr(lineidx, sortlines)

			if pval < 0.01 and spearman > 0:
				#print i, spearman, pval
				# print text
				feats[i]["alphabetical:spearman"]=spearman
				# print lineidx, sortlines
				# print '\n'.join(srt)

		return feats
