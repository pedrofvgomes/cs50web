from django.shortcuts import render

from . import util

from django import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "search": SearchForm(),
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

class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))
    
def search(request):
    if request.method == 'POST':
        search = SearchForm(request.POST)

        if(search.is_valid()):
            entries = util.list_entries()
            results = []

            query = search.cleaned_data["query"]
            if query in entries:
                return render(request, "encyclopedia/wiki.html",{
                    "title": query.capitalize(),
                    "content" : util.get_entry(query)
                })
            
            results = [entry for entry in entries if query.lower() in entry.lower()]

            return render(request, "encyclopedia/search.html", {
                "query" : query,
                "results" : results
            })
    return render(request, "encyclopedia/index.html",{
        "search" : SearchForm()
    })

def newpage(request):
    return render(request, "encyclopedia/newpage.html")

