from django.shortcuts import render, redirect

from . import util

from django import forms

from random import choice

from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "search": SearchForm(),
        "entries": util.list_entries()
    })

def wiki(request, title):
    markdowner = Markdown()
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html",{
                      "title" : title})
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "content": markdowner.convert(util.get_entry(title))
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

def random(request):
    entries = util.list_entries()
    if entries:
        return redirect("wiki", title=choice(entries))
    return redirect("index")

class EditPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title', 'autocomplete':'off'}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Page content', "maxlength":"2000", "columns":"10"}))

def editpage(request, title):
    content = util.get_entry(title)

    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data['title'], form.cleaned_data['content'])
            return redirect("wiki", title=title)
    else:
        form = EditPageForm(initial={'title': title, 'content': content})

    return render(request, "encyclopedia/editpage.html", {
        "title": title,
        "editpage": form
    })