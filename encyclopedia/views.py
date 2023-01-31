from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
from . import util
import re
from django import forms
import random
from django.core.files.base import ContentFile
from ast import *





def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearch(),
    })

def entry(request, title):
    entry = util.get_entry(title)
    print(entry)

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

def random_page(request):
    numberPages = len(util.list_entries())
    indexPage = random.randrange(numberPages)
    page = util.list_entries()[indexPage]
    return HttpResponseRedirect(reverse('encyclopedia:entry', args=({page})))  



class NewPage(forms.Form):
    title =  forms.CharField(widget=forms.TextInput)
    content = forms.CharField(widget=forms.Textarea)

                  
def new_page(request):
    if request.method == 'POST':
        newpage = NewPage(request.POST)
        if newpage.is_valid():
            title = newpage.cleaned_data["title"]
            if util.get_entry(title) == None:
                content = newpage.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('encyclopedia:entry', args=({title})))
            else:
                return render(request, "encyclopedia/new_page.html",{
                "newPage": NewPage(),
                "pagealreadyExisting": title,
                })

        else:
            return render(request, "encyclopedia/new_page.html",{
            "newPage": NewPage(),
            })
    else:        
        return render(request, "encyclopedia/new_page.html",{
            "newPage": NewPage(),

            })
    

class EditPage(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def edit_page(request, title):
    entry = util.get_entry(title)
    
    if request.method == 'POST':
        page = EditPage(request.POST)
        if page.is_valid():
            content = page.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('encyclopedia:entry', args=({title})))
        else:
            return HttpResponseRedirect(reverse('encyclopedia:edit_page', args=({title})))

    else:
        print(title)
        initial_dict = {
            "content": entry,
            }
        editPage = EditPage(initial = initial_dict)
       
        return render(request, "encyclopedia/edit_page.html", {
            'editContent': editPage,
            "title": title,
        })

