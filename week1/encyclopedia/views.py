from django.shortcuts import render, redirect

from . import util

from django import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "search": SearchForm(),
        "entries": util.list_entries()
    })

def wiki(request, title):
    if(title.lower() == title):
        title = title.capitalize()
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html",{
                      "title" : title})
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "content": util.get_entry(title)
    })

class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia', 'autocomplete':'off'}))
    
def search(request):
    if request.method == 'POST':
        search = SearchForm(request.POST)

        if(search.is_valid()):
            entries = util.list_entries()
            results = []

            query = search.cleaned_data["query"]
            if query in entries:
                return redirect("wiki", title=query)
            
            results = [entry for entry in entries if query.lower() in entry.lower()]

            return render(request, "encyclopedia/search.html", {
                "query" : query,
                "results" : results
            })
    return render(request, "encyclopedia/index.html",{
        "search" : SearchForm()
    })

class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title', 'autocomplete':'off'}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Page content', "maxlength":"2000", "columns":"10"}))

def newpage(request):
    if request.method == 'POST':
        newpage = NewPageForm(request.POST)
        if newpage.is_valid() and newpage.cleaned_data['title'].lower() not in [entry.lower() for entry in util.list_entries()]:
            title = newpage.cleaned_data['title']
            content = newpage.cleaned_data['content']
            util.save_entry(title, content)
            return redirect("wiki", title=title)
        return render(request, "encyclopedia/newpageerror.html", {
            "title" : newpage.cleaned_data['title']
        })
    return render(request, "encyclopedia/newpage.html",{
        "newpage": NewPageForm()
    })

