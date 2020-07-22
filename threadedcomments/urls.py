
from django.contrib import admin
from django.urls import path
from jokes.views import JokeList,joke_detail
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', JokeList.as_view(),name='jokes_list'),
    path('<int:pk>/', joke_detail,name='jokes_detail'),
]
