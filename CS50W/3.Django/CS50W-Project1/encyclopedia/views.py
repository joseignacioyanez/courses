from django.shortcuts import render, redirect
from django.core.files import File

from random import randrange

from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entryShow(request, entryName):
    # Check if Entry exists
    entrySearched = util.get_entry(entryName)
    if not entrySearched:
        return render(request, "encyclopedia/error.html")

    else:

        markdowner = Markdown()
        entryHTML = markdowner.convert(entrySearched)

        return render(request, "encyclopedia/entry.html", {
            # Render Markdown entry
            "entryName":entryName,
            "entryHTML":entryHTML
        })

def search(request):
    # Check if request has parameters
    query = request.GET.get('q')
    if not query:
        return render(request, "encyclopedia/search.html", {
            "noQuery":True
        })    
    
    entries = [x for x in util.list_entries()]

    # Exact match
    if query in entries:
        return redirect("entryShow", entryName=query)
    else:
        matches = [entry for entry in entries if f"{query.lower()}" in entry.lower()]

        return render(request, "encyclopedia/search.html", {
            "matches":matches
        })

def newPage(request):
    if request.method == "POST":
        # Check if name is OK
        try:
            newEntryName = request.POST.get('entryTitle').lower()
            entries = [x.lower() for x in util.list_entries()]
        except Exception as e:
            return render(request, "encyclopedia/error.html")
        
        if newEntryName in entries:
            return render(request, "encyclopedia/newPage.html", {
                "entryMarkdown": request.POST.get('entryMarkdown'),
                "error":True
            })
        # Save and Redirect 
        util.save_entry(request.POST.get('entryTitle'), request.POST.get('entryMarkdown'))
        
        return redirect("entryShow", entryName=newEntryName)
    else:
        return render(request, "encyclopedia/newPage.html")

def editPage(request, entryName):
    if request.method == "POST":
        # Save and Redirect 
        util.save_entry(request.POST.get('entryTitle'), request.POST.get('entryMarkdown'))
        
        return redirect("entryShow", entryName=request.POST.get('entryTitle'))
    else:
        entrySearched = util.get_entry(entryName)
        if not entrySearched:
            return render(request, "encyclopedia/error.html")

        entryMarkdown = util.get_entry(entryName)
        entryTitle = entryName
        return render(request, "encyclopedia/editPage.html", {
            "entryTitle" : entryTitle,
            "entryMarkdown": entryMarkdown
        })

def random(request):

    entries = util.list_entries()

    randomIndex = randrange(len(entries)-1)

    return redirect("entryShow", entryName=entries[randomIndex])