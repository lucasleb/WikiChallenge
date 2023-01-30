from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
from . import util
import re
from django import forms
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearch(),
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return HttpResponseRedirect(reverse("encyclopedia:not_found"))
    else:
        content = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
        "content": content, "title": title,
        "form": NewSearch(),
        })


class NewSearch(forms.Form):
    search = forms.CharField(label='Search')

def search(request):
    if request.method == 'POST':
        form = NewSearch(request.POST)
        if form.is_valid():
            title = form.cleaned_data["search"]
            result = util.get_entry(title)
            if result == None:
                suggestions = util.list_substring_entries(title)
                return render(request, "encyclopedia/suggestions.html", {
                            "suggestions": suggestions,
                            "search": title,
                            "form": NewSearch(),
                })
            else:
                return HttpResponseRedirect(reverse('encyclopedia:entry', args=({title})))  
    else:
        return HttpResponseRedirect(reverse("encyclopedia:not_found"))

def not_found(request):
    return render(request, "encyclopedia/not_found.html",{
        "form": NewSearch(),
        })



class NewPage(forms.Form):
    title =  forms.CharField(widget=forms.TextInput)
    content = forms.CharField(widget=forms.Textarea)

                  
def new_page(request):
    if request.method == 'POST':
        newpage = NewPage(request.POST)
        if newpage.is_valid():
            titlePage = newpage.cleaned_data["title"]
            content = newpage.cleaned_data["content"]
            util.save_entry(titlePage, content)
            return HttpResponseRedirect(reverse('encyclopedia:entry', args=({titlePage})))

        else:
            return render(request, "encyclopedia/new_page.html",{
            "newPage": NewPage(),
            })
    else:        
        return render(request, "encyclopedia/new_page.html",{
            "newPage": NewPage(),
            })

def random_page(request):
    numberPages = len(util.list_entries())
    indexPage = random.randrange(numberPages)
    page = util.list_entries()[indexPage]
    return HttpResponseRedirect(reverse('encyclopedia:entry', args=({page})))  



