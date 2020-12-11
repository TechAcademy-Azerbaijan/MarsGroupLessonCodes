import math
from django.db import models
from django.shortcuts import render, redirect
from django.http import Http404, request
from datetime import datetime
from django.db.models import Q
from django.urls.base import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView
)

from stories.models import Author, Category, Contact, Recipe
from stories.forms import (
    ContactForm,
    RecipeForm
)


def test(request):
    users = Author.objects.all()
    searched_name = request.GET.get('search')
    order_by = request.GET.get('order')
    per_count = 3
    print(searched_name)
    page = int(request.GET.get('page', 1))
    if searched_name:
        users = users.filter(Q(first_name__icontains=searched_name) 
        | Q(last_name__icontains=searched_name))
    if order_by:
        users = users.order_by(order_by)

    page_count = math.ceil(users.count()/per_count)
    users = users[(page-1)*per_count:page*per_count]
    page_range = range(1, page_count+1)
    context = {
        'user_list': users,
        'current_page': page,
        'searched_name': searched_name if searched_name else '',
        'page_range': page_range
    }
    return render(request, 'users.html', context)


def user_detail(request, user_id):
    # if user_id > len(users):
    #     raise Http404
    user = []
    # print(request.GET)
    # user = request.GET.get('selected_user', 'Secilmis User yoxdur')
    context = {
        'selected_user': user
    }
    return render(request, 'user_detail.html', context)


def home(request):
    return render(request, 'index.html')


# def recipe_list(request):
#     recipes = Recipe.objects.all()
#     context = {
#         'recipe_list': recipes
#     }
#     return render(request, 'recipes.html', context)


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes.html'
    paginate_by = 2

    def get_queryset(self):
        queryset =  super().get_queryset()
        return queryset.filter(is_published=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'single.html'
    context_object_name = 'article'

    def get_queryset(self):
        queryset =  super().get_queryset()
        return queryset.filter(is_published=True)


class ContactCreateView(CreateView):
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy('stories:home_page')


class CreateRecipeView(CreateView):
    form_class = RecipeForm
    template_name = 'create_recipe.html'
    # success_url = ''

    # def get_success_url(self):
    #     recipe = self.object
    #     return reverse_lazy('stories:recipe_detail', kwargs={ 'slug': recipe.slug }) + '?success_url=isledi'


# def contact(request):
#     form  = ContactForm()
#     if request.method == 'POST':
#         form = ContactForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#             #name = form.cleaned_data['name']
#             #email = form.cleaned_data['email']
#             #subject = form.cleaned_data['subject']
#             #message = form.cleaned_data['message']
#             #contact = Contact(name=name, email=email, subject=subject, message=message)
#             #contact.save()
#     context = {
#         'form': form
#     }
#     return render(request, 'contact.html', context)
