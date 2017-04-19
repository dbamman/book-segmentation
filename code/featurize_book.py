import re,sys,os,zipfile

from features import WordCounter
from features import NgramCounter
from features import PositionFeatures
from features import LIS
from features import Roman
from features import LetterEntropy
from features import Alphabetical
from features import PageSequence
from features import TextTiling

vocab={}

def readVocab(filename):
    file=open(filename)
    for line in file:
        cols=line.rstrip().split(" : ")
        term=cols[0]
        val=int(cols[1])
        # print term, val
        vocab[term]=val

    file.close()

def convertToIds(feats):
    idfeats={}
    for i in feats:
        idfeats[i]={}
        for key in feats[i]:
            if feats[i][key] == 0:
                continue
            if key in vocab:
                idfeats[i][vocab[key]]=feats[i][key]
    return idfeats
class book:


    def __init__(self, zippath):
        self.zippath = zippath
        parts=zippath.split("/")
        try:
            self.idd="%s.%s" % (parts[parts.index("pairtree_root")-1], parts[-2])
        except:
            pass
        self.pages = self.createPageFeatures()
        self.pages=convertToIds(self.pages)

    def write(self, outfile):

        out=open(outfile, "w")

        for page, pagefeatures in sorted(self.pages.iteritems()):
            out.write("%s\t%s\t%s\n" % (self.idd, page, " ".join(["=".join([str(key), str(val)]) for key, val in pagefeatures.items()])))

        out.write("\n")
        out.close()


    def getbook(self, zippath):
        zf = zipfile.ZipFile(zippath, 'r')
        return zf.namelist()
        # for filename in zf.namelist():
            # data = zf.read(filename)

    def getpagewithnum(self, zippath, pg):
        zf = zipfile.ZipFile(zippath, 'r')
        return zf.open(pg)

  
    def createPageFeatures(self):
        """
        Creates a dictionary where the keys are pages in the format of ints
        and the values are dictionaries (with features as key)
        """
        # "Processing:\t%s" % self.zippath

        pageFeatures = {}
        pages = self.getbook(self.zippath)

        newline_textpages=[]

        for i in range(len(pages)):
            text = self.getpagewithnum(self.zippath, pages[i]).read()
            textlines=text.splitlines()
            newline_textpages.append(textlines)

        pagenums=[]
        reverse_pagenums={}
        for i in range(len(pages)):  
            page = pages[i]
            pagestring = re.sub(".txt", "", page)
            pagenum = int(pagestring[-4:])
            pagenums.append(int(pagenum))
            reverse_pagenums[int(pagenum)]=i
            pageFeatures[int(pagenum)]={}

        featurizer=PageSequence.PageSequence()
        feats=featurizer.extractFeatures(newline_textpages, pagenums)
        for i in range(len(feats)):
            pageFeatures[pagenums[i]].update(feats[i])

        featurizer=WordCounter.WordCounter()
        feats=featurizer.extractFeatures(newline_textpages, pagenums)
        for i in range(len(feats)):
            pageFeatures[pagenums[i]].update(feats[i])

        featurizer=Alphabetical.Alphabetical()
        feats=featurizer.extractFeatures(newline_textpages, pagenums)
        for i in range(len(feats)):
            pageFeatures[pagenums[i]].update(feats[i])

        featurizer=PositionFeatures.PositionFeatures()
        feats=featurizer.extractFeatures(newline_textpages, pagenums)
        for i in range(len(feats)):
            pageFeatures[pagenums[i]].update(feats[i])

        featurizer=LIS.LIS()
        feats=featurizer.extractFeatures(newline_textpages, pagenums)
        for i in range(len(feats)):
            pageFeatures[pagenums[i]].update(feats[i])

        featurizer=Roman.Roman()
        feats=featurizer.extractFeatures(newline_textpages, pagenums)
        for i in range(len(feats)):
            pageFeatures[pagenums[i]].update(feats[i])

        featurizer=LetterEntropy.LetterEntropy()
        feats=featurizer.extractFeatures(newline_textpages, pagenums)
        for i in range(len(feats)):
            pageFeatures[pagenums[i]].update(feats[i])

        # meta feature (add last)
        featurizer=TextTiling.TextTiling()
        feats=featurizer.extractFeatures(newline_textpages, pagenums)
        # already resolved to pagenums
        for i in feats:
            pageFeatures[i].update(feats[i])


        windowFeats={}
        window=3

        # create features for page index i based on features for previous/following pages
        # the pageFeatures dict refers to the true page numbers
        for i in pageFeatures:
            
            windowFeats[i]={}

            for j in range(1,window+1):
                comp=i-j
                if comp not in pageFeatures:
                    continue
                compfeats=pageFeatures[comp]
                for key in compfeats:
                    windowFeats[i]["prev_%s_%s" % (j, key)]=compfeats[key]

                comp=i+j
                if comp not in pageFeatures:
                    continue
                compfeats=pageFeatures[comp]
                for key in compfeats:
                    windowFeats[i]["foll_%s_%s" % (j, key)]=compfeats[key]
                 
        for i in pageFeatures:
            pageFeatures[i].update(windowFeats[i])

        return pageFeatures

if __name__ == "__main__":


    # file mapping vocab to ids
    vocabFile=sys.argv[1]

    # path to zip file containing book
    zippath=sys.argv[2]

    readVocab(vocabFile)
    book=book(zippath)

    # write file to folder containing zip file
    containing=os.path.abspath(os.path.join(zippath, os.pardir))
    outfile="%s/%s" % (containing, "features.txt")
    book.write(outfile)
