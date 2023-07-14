from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html",{
                      "title" : title})
    return render(request, "encyclopedia/wiki.html", {
        "title": title.capitalize(),
        "content": util.get_entry(title)
    })

def search(request, query):
    result = util.get_entry(query)
    if result is None:
        results = [entry for entry in util.list_entries() if query in entry]
        return render(request, "encyclopedia/search.html",{
            "query": query,
            "results": results
        })
    return render(request, "encyclopedia/wiki.html",{
        "title": query.capitalize(),
        "content": util.get_entry(query)
    })

