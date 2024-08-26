from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    if request.method == "POST":
        user_entry = request.POST.get("q")
        if util.get_entry(user_entry) == None:
                entries = util.list_entries()
                for entry in entries:
                    if user_entry.lower() in entry.lower():
                        return render(request, "encyclopedia/search.html", {"entries":entry, "token":1})
                else:
                    return render(request, "encyclopedia/search.html", {"entries":util.list_entries(), "token":2})
        else:
            url = reverse("entry", args=[user_entry])
            return HttpResponseRedirect(url)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_func(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/error.html")
    markdowner = Markdown()
    content = markdowner.convert(entry)

    return render(request, "encyclopedia/entry.html",{"title": title, "content": content})

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title) != None:
            return render(request, "encyclopedia/duplicate.html")
       
        util.save_entry(title, content)
        markdowner = Markdown()
        content = markdowner.convert(content)
        return render(request, "encyclopedia/entry.html", {"title": title, "content":content})

    return render(request, "encyclopedia/create.html")

def edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title": title, "content":content})
def save_entry(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        url = reverse("entry", args=[title])
        return HttpResponseRedirect(url)

