from django.shortcuts import render
from django.urls import reverse
import markdown2
from . import util
from .forms import SearchForm, PageForm
from django.http import HttpResponse, HttpResponseRedirect
form = SearchForm()
import random
from django.core.files.storage import default_storage


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": form
    })

def entry(request, entry_name):
    """render given entry page"""
    file = util.get_entry(entry_name)
    if file is not None:
        html_file = markdown2.markdown(file)
    else:
        return render(request, "encyclopedia/404.html", status=404)
        #do something else instead of this
    return render(request, "encyclopedia/entry.html",
                  {'title':entry_name, 
                   'body':html_file, "form":form
                  })

def search(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["search"]
            entries = util.list_entries()
            if query in entries:
                return entry(request, query)
            else:
                results = []
                for name in entries:
                    if (query.lower() in name.lower()) or (name.lower() in query.lower()):
                        results.append(name)
                return render(request, "encyclopedia/search_results.html",
                       {
                           "results":results, "form":form
                       })
            
def new_page(request):
    if request.method == "GET":
        page_form = PageForm(request.GET)
        return render(request, "encyclopedia/new_page.html", {
            "form":form, "page_form":page_form
        })
    elif request.method == "POST":
        created_page = PageForm(request.POST)
        title = created_page.data["page_name"]
        body = created_page.data["page_body"]
        error = False
        if title in util.list_entries():
            error = True
        if error == False:
            util.save_entry(title, body)
            return HttpResponseRedirect(reverse("entry_name", args=[title]))
        else:
            return render(request, "encyclopedia/new_page.html", {
                'error':"Page already exists. Please try again.", 
                'form':form, 'page_form':PageForm(initial={'page_name':title, 'page_body':body})
            })
    
def edit_page(request, entry_name):
    if request.method == "GET":
        title = entry_name
        body = util.get_entry(title)
        page_form = PageForm(initial={'page_name':title, 'page_body':body})
        return render(request, "encyclopedia/edit_page.html",
                      {"form":form, "page_form":page_form, "entry_name":title})
    elif request.method == "POST":
        edited_page = PageForm(request.POST)
        title=edited_page.data["page_name"]
        body=edited_page.data["page_body"]
        error = title in util.list_entries() and entry_name != title
        if error == False:
            if entry_name != title:
                util.delete_entry(entry_name)
            util.save_entry(title, body)
            return HttpResponseRedirect(reverse("entry_name", args=[title]))
        else:
            return render(request, "encyclopedia/edit_page.html", {
                'error':"Please enter a valid name.", 
                'form':form, 'page_form':PageForm(initial={'page_name':title, 'page_body':body, 
                }),'entry_name':entry_name})
            
        #after one attempt it just lets you put in 
        #names that it shouldn't
        #i think it works now
       
        

def random_page(request):
    entries = util.list_entries()
    num_entries = len(entries)
    ind = random.randrange(num_entries)
    title = entries[ind]
    return HttpResponseRedirect(reverse("entry_name", args=[title]))
    
        

        
        
    

            




    

