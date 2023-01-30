from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
from . import util

from django import forms

class NewSearch(forms.Form):
    search = forms.CharField(label='Search')

def search(request):
    if request.method == 'POST':
        form = NewSearch(request.POST)
        if form.is_valid():
            title = form.cleaned_data["search"]
            entry = util.get_entry(title)
            if entry == None:
                return HttpResponseRedirect(reverse("encyclopedia:not_found"))
            else:
                return HttpResponseRedirect(reverse('encyclopedia:entry', args=({title:entry})))

                

    else:
        return HttpResponseRedirect(reverse("encyclopedia:not_found"))



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
        


def not_found(request):
    return render(request, "encyclopedia/not_found.html",{
        "form": NewSearch(),
        })
                  



