from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required

from .forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView
from .utils import *


menu = [{'title': 'home page', 'url_name': 'home'},
        {'title': 'add an article', 'url_name': 'add_article'},
]


class ArticlesHome(DataMixin, ListView):
    model = Article
    template_name = 'articles_feed/index.html'
    context_object_name = 'articles'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


@login_required
def my_articles(request):
    articles = Article.objects.filter(user=request.user).order_by('-time_update')
    context = {'menu': menu,
               'title': 'my_articles',
               'articles': articles,
               'cat_selected': 0}
    return render(request, 'articles_feed/my_articles.html', context=context)


@login_required
@permission_required('articles_feed.change_article', raise_exception=True)
def edit_article(request, article_slug):
    if not request.user.has_perm('articles_feed.add_article'):
        raise PermissionError
    article = get_object_or_404(Article, slug=article_slug)

    if request.method != 'POST':
        form = AddArticleForm(instance=article)

    else:
        form = AddArticleForm(instance=article, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'article': article,
               'form': form,
               'menu': menu,
               'title': 'Добавление статьи'}

    return render(request, 'articles_feed/edit_article.html', context=context)


"""
class AddArticle(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddArticleForm
    template_name = 'articles_feed/new_article.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add article')
        return dict(list(context.items()) + list(c_def.items()))
"""


@login_required
@permission_required('articles_feed.add_article', raise_exception=True)
def add_article(request):
    if not request.user.has_perm('articles_feed.add_article'):
        raise PermissionError
    if request.method != 'POST':
        form = AddArticleForm

    else:
        form = AddArticleForm(data=request.POST)
        if form.is_valid():
            new_article = form.save()
            new_article.user = request.user
            new_article.save()
            return redirect('home')

    context = {'menu': menu,
               'form': form,
               'title': 'add article'}
    return render(request, 'articles_feed/new_article.html', context=context)


def login(request):
    return HttpResponse('Log in')


class ShowArticle(DataMixin, DetailView):
    model = Article
    template_name = 'articles_feed/article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['article'])
        return dict(list(context.items()) + list(c_def.items()))


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')


class ArticleCategory(DataMixin, ListView):
    model = Article
    template_name = 'articles_feed/index.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_queryset(self):
        return Article.objects.filter(cat__slug=self.kwargs['cat_slug'],
                                      is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Category - ' + str(context['articles'][0].cat),
                                      cat_selected=context['articles'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

"""
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'articles_feed/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign in')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(user)
        return redirect('home')
"""


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'articles_feed/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign in')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        user_group = Group.objects.get(name=form.cleaned_data['groups'])
        user.groups.add(user_group)
        login(user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'articles_feed/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='login')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')
