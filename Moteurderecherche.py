# -*- coding: utf-8 -*-

"""
*******************************************************
/!\THIS PROJECT HAS BEEN CODED FOR FRENCH LANGUAGE USE
*******************************************************
"""

# -----------------------------------------------Importing modules------------------------------------------------------
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize
import string
import math
import os

# -------------------------------------------------Global variables-----------------------------------------------------
folderDocs = "media/documents/"  # folder containing the files
docs = os.listdir(folderDocs)  # variable to list the contents of folderDocs
nbDocs = len(os.listdir(folderDocs))  # variable that lists the number of docs in docs


# -------------------------------------------------Main function--------------------------------------------------------
def load_file(f):
    """
    Loading and opening a file
    """
    file = open(folderDocs + f, encoding="utf-8")  # open the selected file
    res = file.read().lower()  # writing the file to a new variable
    file.close()  # close the file
    return res


def containletter(chaine):
    """
    Returns true if the word string contains a letter
    """
    for c in chaine:  # for each letter in the string
        if c in string.ascii_lowercase:  # Is c this a letter ?
            return True
    return False


def rootword(word):
    """
    Returns the root word (FR : homme --> homm)
    """
    return FrenchStemmer().stem(word)


def chaincleaninglist(chain):
    """
    Cleaning of the string passed in parameter
    """
    res = []
    i = 0
    for word in word_tokenize(chain):  # for each word in the string
        if containletter(word):  # if the word contains only letters
            for c in word:  # for each character in the word
                if c in u"Â«Â»Å‚.â”œ":  # if the character is special
                    word = word[:i] + word[i + 1:]  # it is removed
            if word not in stopwords.words('french'):  # if the word is not a punctuation mark
                res.append(word)  # it is added to the final list
    return res


def listDico(li):
    """
    Function to add the value of the word in a document
    """
    dico = {}
    for mot in li:  # for each word in the list
        if mot not in dico.keys():  # if the word is not in the dictionary keys
            dico[mot] = 1  # the value is set to 1
        else:
            dico[mot] += 1  # otherwise the value is incremented by 1
    return dico


def liststem(li):
    """
    All words in the list are transformed into the root word
    """
    res = []
    for mot in li:  # for each word in the list
        res.append(rootword(mot))  # the root word is added to a final list
    return res


def docdicostem():
    """
    for all the docs files, we will build a big dictionary in which we will have the stem of the word followed by ;
    for each document, the name of the doc and the number of times the word is found in this same doc
    """
    dicodoc = {}
    for file in docs:  # for all files in docs
        openning = load_file(file)  # opening the file
        li = chaincleaninglist(openning)  # cleaning up the file (punctuation, etc.)
        stem = []
        for word in li:  # for each word in this same list
            stem.append(rootword(word))  # add the root to a "stem" list
        dicodoc[file] = listDico(stem)  # we transform the list into a dictionary and add it to dicodoc
    dicodocstem = {}
    for (file, doc) in dicodoc.items():  # for each row, docs in dicodoc items
        for stemMot in doc:  # for each root in the doc
            if stemMot in dicodocstem.keys():  # if the root is in "dicodocstem, we add the missing file to the stem
                dicodocstem[stemMot][file] = doc[stemMot]  # ex: {homm: {doc1.txt : 1, doc5.txt : 1}}
            else:
                dicodocstem[stemMot] = {}  # otherwise we create and add the root + the doc
                dicodocstem[stemMot][file] = doc[stemMot]  # ex: {kabyl: {doc1.txt : 1}}
    return dicodocstem


def nbworddoc():
    """
    Function to get the number of words in the document
    """
    dicondoc = {}
    for file in docs:  # for each file in "docs
        li = word_tokenize(load_file(file))  # create a word list for the given document
        for word in li:  # for each word in the list
            punctuation = [".", ",", ";", ":", "’", "'"]
            if word in punctuation:  # if the word is a punctuation mark
                li.remove(word)  # it is removed from the list
        dicondoc[file] = len(li)  # we count the number of words in the list for a given document
    return dicondoc


def df(dico):
    """
    Function to calculate the frequency of a word in all documents
    """
    for stemMot in dico:  # for each root in "dico"
        dico[stemMot]["df"] = len(dico[stemMot])  # we add to the index for a given word the frequency of the document
    return dico


def tfidf(dico):
    """
    Term (word) frequency calculation function for document frequency
    tfidf = term frequency in document frequency
    """
    ndoc = nbworddoc()
    for stem in dico:  # for each root in "dico"
        for doc in dico[stem]:  # for each file in dico[root]
            if doc != "df":  # if different from df
                # we will calculate the tfidf of each value (docdicostem) for a given word root
                dico[stem][doc] = float(dico[stem][doc]) / float(ndoc[doc])
                dico[stem][doc] *= math.log10(float(nbDocs) / float(dico[stem]["df"]))
                dico[stem][doc] = round(dico[stem][doc], 5)
    return dico


def exportationIndex(I, fichier):
    """
    Function to export the previously created dictionary as a txt file for easier reading
    """
    fil = open(fichier, 'w')  # we open a file in writing
    for stem, dicostem in I.items():
        # we write stem + "tab"
        fil.write(stem + '\t\t')
        for doc, score in dicostem.items():
            # Then the doc and its values (if there is more than one we repeat the operation (including df))
            fil.write(doc + " : " + str(score) + '\t\t')
        # a line break is added for easier reading
        fil.write('\n')
    # close the file
    fil.close()


def index():
    """
    Function to get a console result of the index
    """
    return tfidf(df(docdicostem()))


# ------------------------------------------similarity calculation-----------------------------------------------------
def pre_requete(request):
    """
    Function that for a search, cleans the string and returns the root of the word or words contained in the search
    """
    dicReqStem = {}
    request = chaincleaninglist(request)
    for mot in request:
        racine = rootword(mot)
        if racine in dicReqStem.keys():
            dicReqStem[racine] += 1
        else:
            dicReqStem[racine] = 1
    return dicReqStem


def normeCOS(request):
    """
    the standard here : (v/|q|.|d|\)
    """
    norme = 1
    for (document, valeurdoc) in request.items():
        norme += valeurdoc ** 2
    return math.sqrt(norme)


def simCOS(request):
    """
    Description of the mathematical calculation function :
    sim(q, d) = (q · d)/(v/|q|.|d|\) = somme(qi, di)/(sqrt(sum(qi2)))*(sqrt(sum(vi2))) where i = 1 at v

    qi is the tf-idf weight of term i in the query.
    di is the tf-idf weight of term i in the document. |q| and |d| are the lengths of q and D.
    is the cosine similarity of q and D or, similarly, the cosine of the angle between q and D.
    """
    ldoc = {}
    I = index()
    request = pre_requete(request)
    for stem in request:
        if stem in I.keys():
            for doc in I[stem]:
                if doc in ldoc and doc != 'df':
                    ldoc[doc] += request[stem] * I[stem][doc]
                elif doc != 'df':
                    ldoc[doc] = request[stem] * I[stem][doc]
    for doc in ldoc:
        ldoc[doc] /= normeCOS(request)
    return ldoc


def normeDICE(request):
    """
    the standard here : (|q| + |d|)
    """
    norme = 0
    for (document, valeurdoc) in request.items():
        norme += valeurdoc ** 2
    return norme


def simDICE(request):
    """
    Description of the mathematical calculation function :
    sim(q, d) = 2 . (q . d)/(|q| + |d|) = 2*(somme(qi, di))/((sum(qi2)+sum(vi2))) where i = 1 at v

    qi is the tf-idf weight of term i in the query.
    di is the tf-idf weight of term i in the document. |q| and |d| are the lengths of q and D.
    is the cosine similarity of q and D or, similarly, the cosine of the angle between q and D.
    """
    ldoc = {}
    I = index()
    request = pre_requete(request)
    for stem in request:
        if stem in I.keys():
            for doc in I[stem]:
                if doc in ldoc and doc != 'df':
                    ldoc[doc] += request[stem] * I[stem][doc]
                elif doc != 'df':
                    ldoc[doc] = request[stem] * I[stem][doc]
    for doc in ldoc:
        ldoc[doc] = 2.0 * ldoc[doc] / normeDICE(request)
    return ldoc


def normeJACCARD(request):
    """
    the standard here : (|q| + |d|-(q . d))
    """
    norme = 0
    for (document, valeurdoc) in request.items():
        norme += valeurdoc ** 2
    return norme


def simJACCARD(request):
    """
    Description of the mathematical calculation function :
    sim(q, d) = (q . d)/(|q| + |d|-(q . d)) = (somme(qi, di))/(((sum(qi2)+sum(vi2))-(somme(qi, di))) where i = 1 at v

    qi is the tf-idf weight of term i in the query.
    di is the tf-idf weight of term i in the document. |q| and |d| are the lengths of q and D.
    is the cosine similarity of q and D or, similarly, the cosine of the angle between q and D.
    """
    ldoc = {}
    I = index()
    request = pre_requete(request)
    for stem in request:
        if stem in I.keys():
            for doc in I[stem]:
                if doc in ldoc and doc != 'df':
                    ldoc[doc] += request[stem] * I[stem][doc]
                elif doc != 'df':
                    ldoc[doc] = request[stem] * I[stem][doc]
    for doc in ldoc:
        ldoc[doc] /= (normeJACCARD(request) - ldoc[doc])
    return ldoc

# ----------------------------------------------------------END---------------------------------------------------------
