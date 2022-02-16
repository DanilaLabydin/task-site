from django.urls import path, re_path
from .views import *
urlpatterns = [
    path('', ArticlesHome.as_view(), name='home'),
    path('add_article/', add_article, name='add_article'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('article/<slug:article_slug>/', ShowArticle.as_view(), name='article'),
    path('category/<slug:cat_slug>/', ArticleCategory.as_view(), name='category'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('my_article/', my_articles, name='my_articles'),
    path('edit_article/<slug:article_slug>/', edit_article, name='edit_article')

]
#path('category/<int:cat_id>/', show_category, name='category')