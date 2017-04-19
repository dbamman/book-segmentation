# -*- coding: utf-8 -*-

import re

class WordCounter:

	def __init__(self):
		self.valid={}
		self.valid["my"]=1
		self.valid["to"]=1
		self.valid["wife"]=1
		self.valid["dedicated"]=1
		self.valid["dedication"]=1
		self.valid["father"]=1
		self.valid["mother"]=1
		self.valid["husband"]=1
		self.valid["finis"]=1
		self.valid["fin"]=1
		self.valid["son"]=1
		self.valid["daughter"]=1
		self.valid["index"]=1
		self.valid["appendix"]=1
		self.valid["appendices"]=1
		self.valid["illustrations"]=1
		self.valid["preface"]=1
		self.valid["reader"]=1
		self.valid["life"]=1
		self.valid["period"]=1
		self.valid["letters"]=1
		self.valid["price"]=1
		self.valid["published"]=1
		self.valid["volume"]=1
		self.valid["cents"]=1
		self.valid["pages"]=1
		self.valid["contents"]=1
		self.valid["page"]=1
		self.valid["section"]=1
		self.valid["chap"]=1
		self.valid["frontispiece"]=1
		self.valid["drawing"]=1
		self.valid["copyright"]=1
		self.valid["preface"]=1
		self.valid["library"]=1
		self.valid["printers"]=1
		self.valid["university"]=1
		self.valid["square"]=1
		self.valid["published"]=1
		self.valid["press"]=1
		self.valid["copyrighted"]=1
		self.valid["letters"]=1

		self.valid["errata"]=1
		self.valid["subscribers"]=1
		self.valid["notes"]=1
		self.valid["glossary"]=1
		self.valid["dramatis"]=1
		self.valid["personae"]=1
		self.valid["notice"]=1
		self.valid["reader"]=1
		self.valid["foreword"]=1
		self.valid["erratum"]=1
		self.valid["editor"]=1
		self.valid["publisher"]=1

		self.valid["preface"]=1
		self.valid["contents"]=1
		self.valid["advertisement"]=1
		self.valid["index"]=1
		self.valid["epilogue"]=1
		self.valid["chapter"]=1
		self.valid["introduction"]=1
		self.valid["intro"]=1
		self.valid["dedication"]=1
		self.valid["published"]=1
		self.valid["publisher"]=1
		self.valid["advertisements"]=1
		self.valid["author"]=1
		self.valid["copyright"]=1
		self.valid["printed"]=1
		self.valid["$"]=1
		self.valid["£"]=1
		self.valid["dedicatory"]=1
		self.valid["price"]=1
		self.valid["illustrations"]=1
		self.valid["prefatory"]=1
		self.valid["appendix"]=1
		self.valid["mr"]=1
		self.valid["mrs"]=1
		self.valid["miss"]=1
		self.valid["dr"]=1
		self.valid["rev"]=1
		self.valid["esq"]=1
		self.valid["efq"]=1
		self.valid["hon"]=1
		self.valid["list"]=1
		self.valid["ditto"]=1
		self.valid["lady"]=1
		self.valid["lord"]=1


	def extractFeatures(self, pages, pagenums):
		feats=[]
		for i in range(len(pages)):
			feats.append({})

		for i in range(len(pages)):
			num_numbers=0
			num_words=0

			text=""
			lines=pages[i]
			for idx, line in enumerate(lines):
				if idx <= 5:
					newtext=line.lower().rstrip()
					newtext=re.sub("[^a-z0-9$£ ]", "", newtext)
					tokens=re.split("\s+", newtext)
					for token in tokens:
						if token in self.valid:
							feats[i]["wordcounter:header_%s" % token]=1

				text+=line.rstrip()

			# since we're just checking for membership in the dict above, strip out all non alphanums
			newtext=text.lower().rstrip()
			newtext=re.sub("[^a-z0-9$£ ]", "", newtext)
			tokens=re.split("\s+", newtext)

			for token in tokens:
				if re.match("[0-9]+", token) != None:
					num_numbers+=1
				if re.match("\w+", token) != None:
					num_words+=1

				if token in self.valid:
					feats[i]["wordcounter:%s" % token]=1

			if len(tokens) < 5:
				feats[i]["wordcounter:_blank_page"]=1

			if num_words < 5:
				feats[i]["wordcounter:_words_under_5"]=1

			feats[i]["wordcounter:_num_words"]=num_words
			feats[i]["wordcounter:_num_numbers"]=num_numbers


			if num_words > 0:
				wordRatio= float(num_words)/len(tokens)
				feats[i]['wordcounter:_wordRatio']=float("%.3f" % wordRatio)
				numRatio=float("%.3f" % (float(num_numbers)/len(tokens)))
				feats[i]['wordcounter:_numRatio']=numRatio
				countSmoother=5
				feats[i]['wordcounter:_wordNumRatio']=float("%.3f" % ((float(num_words) + countSmoother)/ (float(num_numbers) + countSmoother)))

		return feats
