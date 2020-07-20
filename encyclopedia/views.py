from django.shortcuts import render
from django.http import HttpResponse

from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "title": "All Pages",
        "entries": util.list_entries()
    })

def entryTest(request, name):
    if name not in util.list_entries():
        return render(request, "encyclopedia/page.html", {
            "title": "Error: Page Not Found"
        })
    return render(request, "encyclopedia/page.html", {
        "content": markdown2.markdown(util.get_entry(name)),
    })


def search(request):
    if request.method == "POST":
        query = request.POST.get('search')
        entry_list = util.list_entries()
        possible_results = []
        if query in entry_list:
            return render(request, "encyclopedia/page.html", {
                "content": markdown2.markdown(util.get_entry(query)),
            })
        for entry in entry_list:
            if query in entry:
                possible_results.append(entry)
        if possible_results == []:
            return render(request, "encyclopedia/page.html", {
                "title": "Not Found: No entry for your query"
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "title": "Not Found: No entry for your query",
                "entries": possible_results,
            })

def create(request):
    return render(request, "encyclopedia/create.html", {
        "title": "Create New Page",
    })

def createR(request):
    mt = request.POST.get('marktitle')
    mc = request.POST.get('mrkdwn')
    entry_list = util.list_entries()
    
    if mt in entry_list:
        return render(request, "encyclopedia/page.html", {
            "title": "Page Already Existed",
        })
    else:
        util.save_entry(mt, mc)
        return render(request, "encyclopedia/page.html", {
            "title": mt,
            "content": mc,
        })

def randomPage(request):
    name = random.choice(util.list_entries())
    return render(request, "encyclopedia/page.html", {
        "content": markdown2.markdown(util.get_entry(name)),
    })

def edit(request, title):
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title)
    })

def editPage(request):
    #if request.method == "POST":
    title = request.POST.get('title')
    markDown = markdown2.markdown(request.POST.get('mrkdwn'))
    util.save_entry(title, markDown)
    return render(request, "encyclopedia/page.html", {
        "content": markdown2.markdown(util.get_entry(title))
    })
