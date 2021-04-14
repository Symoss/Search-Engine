# -*- coding: utf-8 -*-

"""
*******************************************************
/!\THIS PROJECT HAS BEEN CODED FOR FRENCH LANGUAGE USE
*******************************************************
"""

# -----------------------------------------------Importing modules------------------------------------------------------
from django.views.generic import TemplateView, View
import Moteurderecherche as mtr
from django.template.response import TemplateResponse
import os


# -------------------------------------------------Class declaration----------------------------------------------------
class SearchEngineView(TemplateView, View):  # redirige vers la page search.html
    template_name = 'search.html'


class MultiSimView(TemplateView, View):
    template_name = 'sim.html'


# -------------------------------------------------Main function--------------------------------------------------------
def QuerySet():
    """
    Function allowing to obtain for each document, the first two lines
    """
    filedoc = "media/documents/"
    textdoc = {}
    namedoc = [doc for doc in os.listdir("media/documents")]
    for i in range(len(namedoc)):
        file = open(filedoc + namedoc[i], encoding="utf-8")
        twoline = []
        for line in range(2):
            twoline.append(file.readline())
        file.close()
        twoline = ' '.join(twoline).replace("\n", "")
        textdoc[namedoc[i]] = twoline + "..."
    return textdoc


def allsimilarities(request):
    """
    Function to display all similarities in one page
    """
    srh = request.GET['query']
    cos = mtr.simCOS(srh)
    dice = mtr.simDICE(srh)
    jaccard = mtr.simJACCARD(srh)
    return preesimilarities(request, cos, dice, jaccard)


def preesimilarities(request, cos, dice, jaccard):
    """
    Pre function to display all similarities in one page
    """
    licos = []
    lidice = []
    lijaccard = []
    # ----------------------------------------------similarity cos------------------------------------------------------
    for (key, value) in cos.items():
        temp = [key, value]
        licos.append(temp)
    licos = sorted(licos, key=lambda val: val[1], reverse=True)
    # ----------------------------------------------similarity dice-----------------------------------------------------
    for (key, value) in dice.items():
        temp = [key, value]
        lidice.append(temp)
    lidice = sorted(lidice, key=lambda val: val[1], reverse=True)
    # ----------------------------------------------similarity jaccard--------------------------------------------------
    for (key, value) in jaccard.items():
        temp = [key, value]
        lijaccard.append(temp)
    lijaccard = sorted(lijaccard, key=lambda val: val[1], reverse=True)

    # ---------------------------------------------------Responce-------------------------------------------------------
    return TemplateResponse(request, template='sim.html', context={'COS': licos, 'DICE': lidice, 'JACCARD': lijaccard})


def response(request, res):
    """
    Response function for web display
    """
    res = dict(sorted(res.items(), key=lambda item: item[1][0], reverse=True))  # ranking by score from + to -
    return TemplateResponse(request, template='search.html', context={'gab': res})  # answer below the search bar


def SearchPage(request):
    """
    Function for a given similarity for one request

    1) if the similarity is equal to "cos" or "dice" or "jaccard"
    2) we calculate the similarity "cos" or "dice" or "jaccard"
    3) we come to update the list for a poster
        document -> [score]
        "the first two lines"
    4) we return the answer for a given request
    """
    srh = request.GET['query']
    sim = request.GET['queryaff']
    stemsrh = mtr.rootword(srh)
    # ----------------------------------------------similarity cos------------------------------------------------------
    if sim == "cos":
        res = mtr.simCOS(stemsrh)
        lires = {}
        query = QuerySet()
        for doc, score in res.items():
            if doc in query.keys():
                lires.update({doc: [score, query[doc]]})
        return response(request, lires)
    # ----------------------------------------------similarity dice-----------------------------------------------------
    elif sim == "dice":
        res = mtr.simDICE(stemsrh)
        lires = {}
        query = QuerySet()
        for doc, score in res.items():
            if doc in query.keys():
                lires.update({doc: [score, query[doc]]})
        return response(request, lires)
    # ----------------------------------------------similarity jaccard--------------------------------------------------
    elif sim == "jaccard":
        res = mtr.simJACCARD(stemsrh)
        lires = {}
        query = QuerySet()
        for doc, score in res.items():
            if doc in query.keys():
                lires.update({doc: [score, query[doc]]})
        return response(request, lires)

# ----------------------------------------------------------END---------------------------------------------------------
