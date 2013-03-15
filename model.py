import re
import settings

class article:
    def __init__(self):
        self.authors = []
        self.title = ""
        self.description = ""
        self.link = ""
    def setModel(self,authors, title, description, link):
        self.authors = authors
        self.title = title
        self.description = description
        self.link = link
    def printPaper(self):
        print "Authors: "
        for a in self.authors:
            print "\t"+a
        print "Title: " + self.title
        print ""
        print "Description:\n" + self.description
        print "Link: " + self.link
        print '\n*******************************\n\n'
    def printToFile(self,result):
        result.write("Authors: ")
        fstring = ""
        for a in self.authors:
            result.write(fstring.encode("utf-8"))
            result.write(a.encode("utf-8"))
            fstring=", "
        string = "\nTitle: " + self.title + "\n"
        result.write(string.encode("utf-8"))
        result.write("\n")
        string = "Abstract:\n" + self.description
        result.write(string.encode("utf-8"))
        result.write("Link: " + self.link)
        result.write('\n***********************\n\n')

    def checkerAuthors(self,element):
        for author in self.authors:
            for dt in element:
                if re.search(dt,author):
                    return 1
        return 0

    def checkerKeyWords(self,element):
        for dt in element:
            if re.search(dt,self.title) or re.search(dt,self.description):
                return 1
        return 0

    def checker(self,key_authors, key_words):
        if self.checkerAuthors(key_authors):
            return 1
        elif self.checkerKeyWords(key_words):
            return 2
        return 0