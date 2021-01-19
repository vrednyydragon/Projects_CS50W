from django.shortcuts import render

from . import util

from django import forms
import markdown2
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random

# class for new page form
class NewPageForm(forms.Form):
	title = forms.CharField(label="Title",
							widget=forms.TextInput(attrs={'class': 'form-control col-lg-5', 'placeholder': 'Enter entry title'}))
	content = forms.CharField(label="Content",
								widget=forms.Textarea(attrs={'class': 'form-control col-lg-10', 'rows': 13,
								                             'placeholder': 'The entry content'}))

def index(request):
	''' main page of the encyclopedia wiki'''
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})

def entry_page(request, title):
	''' one page by current title '''
	curr_entry = util.get_entry(title)
	if curr_entry is None:
		context = {
			'message_type': "not exists",
			'page_title': title,
			'page_info': f'doesn\'t exists'}
		return render(request, "encyclopedia/error.html", context)
	else:
		markdown_text = markdown2.markdown(curr_entry)
		context = {
			'page_title': title,
			'page_info': markdown_text}
		return render(request, "encyclopedia/entry.html", context)

def search(request):
	''' get list of existing pages by search request '''
	if request.method == "POST":
		entries_list = []
		search_text = request.POST["q"]
		# print(f'search_text = {search_text}')
		if util.get_entry(search_text) is not None:
			return HttpResponseRedirect(reverse("entry_page", kwargs={'title':search_text}))
		else:
			for entry in util.list_entries():
				if search_text.lower() in entry.lower():
					entries_list.append(entry)
			return render(request, "encyclopedia/index.html",{"entries": entries_list})

def new_page(request):
	''' create new page if not exists'''
	if request.method == "GET":
		new_form = NewPageForm()
		return render(request, "encyclopedia/new_page.html", {'new_page_form': new_form})
	else:
		new_title = request.POST["title"]
		new_content = request.POST["content"]
		if util.get_entry(new_title):
			context = {
				'message_type': "exists",
                'page_title': new_title,
				'page_info': f'already exists'}
			return render(request, "encyclopedia/error.html", context)
		else:
			util.save_entry(new_title, new_content)
			return HttpResponseRedirect(reverse("entry_page", kwargs={'title': new_title}))

def edit_page(request, title):
	''' editting choosen page content '''
	curr_entry = util.get_entry(title)
	if request.method == "GET":
		edit_form = NewPageForm()
		edit_form.fields['title'].widget = forms.HiddenInput()
		edit_form.fields['content'].initial = curr_entry
		return render(request, "encyclopedia/edit_page.html", {'page_title': title,
			'edit_page_form': edit_form})
	elif request.method == "POST":
		new_content = request.POST["content"]
		util.save_entry(title, new_content)
		return HttpResponseRedirect(reverse("entry_page", kwargs={'title': title}))

def random_page(request):
	''' get existing page randomly '''
	random_name = random.choice(util.list_entries())
	return HttpResponseRedirect(reverse("entry_page", kwargs={'title': random_name}))
