# -*- coding: utf-8 -*-

import re
import numpy as np

class PageNumbers:


	def extractFeatures(self, pages, pagenums):
		feats=[]
		maxx=0
		for i in range(len(pages)):
			feats.append({})
			if pagenums[i] > maxx:
				maxx=pagenums[i]
		
		first_page_counts=np.zeros(maxx)

		for i in range(len(pages)):
			
			pagenum=pagenums[i]

			text=""
			lines=pages[i]
			for idx, line in enumerate(lines):
				if idx < 5 or idx >= len(lines)-5:
					text+=line.rstrip()

			tokens=re.split("\s+", text.lower())
			seen={}
			for token in tokens:
				if re.match("^[0-9]+$", token) != None:
					number=int(token)
					# e.g., sequence 14 - page num 2 -> first page = 13
					diff=(pagenum-number)+1
					if diff < 0 or diff >= maxx or number in seen:
						continue
					seen[number]=1
					first_page_counts[diff]+=1

		first_page=np.argmax(first_page_counts)
		print first_page_counts
		if first_page_counts[first_page] > 1 and float(first_page_counts[first_page])/np.sum(first_page_counts) > .00:
			print first_page, float(first_page_counts[first_page])/maxx, float(first_page_counts[first_page])/np.sum(first_page_counts), first_page_counts[first_page-5:first_page+5]
			for i in range(len(pages)):
				pagenum=pagenums[i]
				feats[i]["page_numbers:detected"]=1
				if pagenum < first_page:
					feats[i]["page_numbers:before_first_page"]=1


		return feats
