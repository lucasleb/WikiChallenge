from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
from . import util
import re
from django import forms

class NewSearch(forms.Form):
    search = forms.CharField(label='Search')



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
                  



