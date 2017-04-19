import sys,re
import segment_from_feature_file
import featurize_book

if __name__ == "__main__":

	zippath=sys.argv[1]
	modelFolder=re.sub("/$", "", sys.argv[2])

	meanFile="%s/means.txt" % modelFolder
	modelFile="%s/model.ckpt" % modelFolder
	vocabFile="%s/vocab.txt" % modelFolder

	featurize_book.readVocab(vocabFile)
	segment_from_feature_file.readmeans(meanFile)

	book=featurize_book.book(zippath)

	feats, page_index=segment_from_feature_file.convertBookToFeats(book.pages)

	predictions=segment_from_feature_file.predict(feats, page_index, modelFile)
	
	# print the predictions
	for page, pred in predictions:
		print "%s\t%s" % (page, pred)

