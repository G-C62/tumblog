"""tumblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog import views as blog_post
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.conf.urls import include

urlpatterns = [

    url(r'^blog/posts/edit/$', blog_post.create_post,name = 'create_post'),    #name = url이름
    url(r'^blog/(?P<pk>[0-9]+)/create_comment/$',blog_post.create_comment, name = 'create_comment'),
    url(r'^blog/posts/(?P<pk>[0-9]+)/$', blog_post.view_post, name='view_post'),
    url(r'^blog/$',blog_post.list_posts , name='list_posts'),
    url(r'^login/$',login,{'template_name': 'login.html'},name = "login_url"),
    url(r'^logout/$',logout,{'next_page': '/login/'},name = "logout_url"),

    url(r'^admin/', admin.site.urls),
    url('', include('social.apps.django_app.urls', namespace='social')),

]
