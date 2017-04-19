### using code and data from https://github.com/tedunderwood/DataMunging

import sys,re,os
from os import listdir
from os.path import isfile, join


class Roman:
	def __init__(self):
		self.romannumerals = set()

		dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

		with open("%s/features/%s" % (dirname, 'romannumerals.txt')) as file:
			filelines = file.readlines()

		for line in filelines:
			line = line.rstrip()
			self.romannumerals.add(line)


	def extractFeatures(self, pages, pagenums):
		feats=[]
		for i in range(len(pages)):
			feats.append({})
			
		for i in range(len(pages)):
			page=pages[i]

			for idx, line in enumerate(page):
				if idx > 4:
					continue

				line = line.strip().lower().split(" ")
				for word in line:
					if word in self.romannumerals:
						feats[i]["roman:header"]=1


			for idx, line in enumerate((reversed(page))):

				if idx > 4:
					continue

				line = line.strip().lower().split(" ")
				for word in line:
					if word in self.romannumerals:
						feats[i]["roman:footer"]=1

		return feats


