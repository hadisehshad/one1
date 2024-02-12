from django.urls import path
from .import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('index_page/', views.IndexView.as_view(), name='index_page'),
    path('index2_page/', views.IndexPageView.as_view(), name='index2_page'),
    path('news/<int:news_id>/<slug:category_slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/delete/<int:news_id>/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('news/update/<int:news_id>/<slug:category_slug>/', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/create', views.NewsCreateView.as_view(), name='news_create'),
    path('reply/<int:news_id>/<slug:category_slug>/<int:comment_id>/', views.NewsAddReplyView.as_view(), name='add_reply'),
    path('like/<int:news_id>/<slug:category_slug>/', views.NewsLikeView.as_view(), name='news_like'),
    path('dislike/<int:news_id>/<slug:category_slug>/', views.NewsDislikeView.as_view(), name='news_dislike'),

]