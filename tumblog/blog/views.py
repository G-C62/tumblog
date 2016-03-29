from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.http import Http404 #http에서의 Http404를 임포트 하였습니다
from .models import Category
from .forms import PostEditForm
from .forms import CommentEditForm
from .models import Comment
from django.contrib.auth.decorators import login_required
import requests
from requests_oauthlib import OAuth1
from django.conf import settings

consumer_key = settings.SOCIAL_AUTH_TUMBLR_KEY

consumer_secret = settings.SOCIAL_AUTH_TUMBLR_SECRET


def list_posts(request):
    page = request.GET.get('page',1) # 있으면 페이지 없으면 디폴트 1로
    #object_list = Post.objects.all().order_by('title') #title,created_at등으로 정렬합니다
    object_list = Post.objects.order_by('-created_at')    # objects의 filter를 이용해서 is_published필드의 값이 True인 값만 리스트에 담도록 하였습니다.

    per_page = 3 #6,9로 페이징 갯수를 설정합니다
    pn = Paginator(object_list,per_page )
    try:
        posts = pn.page(page)

    except PageNotAnInteger:
        posts = pn.page(1)

    except EmptyPage:
        posts = pn.page(pn.num_pages)


        #posts = pn.page(pn.num_pages)



    ctx = {
        'posts':posts,
    }
    return render(request, 'post_list.html',ctx)

def view_post(request,pk):

    the_post = Post.objects.get(pk=pk)
    comment_form = CommentEditForm()
    comments = Comment.objects.filter(post=the_post)

    if the_post.is_published == False : #발행이 안된 게시물을 열면 404화면이 뜨도록 하였습니다.
        raise Http404("404 Exeption을 일으키라고 하셔서 요래 일으켰습니다!!!")


    ctx={
        'post':the_post,
        'comment_form' : comment_form,
        'comments' : comments,
        }
    return render(request,'post_view.html',ctx)

@login_required
def create_post(request):
    '''if request.user.is_authenticated() is False:
        raise Exception('로그인을 해야 합니다')'''

    tumblr = request.user.social_auth.filter(provider='tumblr').first()
    if not tumblr:
        raise Exception('tumblr로 먼저 로그인 하세요')
    oauth_key = tumblr.tokens['oauth_token']
    oauth_secret = tumblr.tokens['oauth_token_secret']
    url = 'http://api.tumblr.com/v2/blog/nsw9211/post'
    client = requests.Session()
    client.auth = OAuth1(
        consumer_key,consumer_secret, oauth_key,oauth_secret
    )
    categories = Category.objects.all()
    if request.method=='POST':

        form = PostEditForm(request.POST)
        if form.is_valid(): #return 문이 없으면 None객체를 반

            #category = get_object_or_404(Category, pk = category_pk)
            new_post = form.save(commit = False)
            new_post.user = request.user
            new_post.save()
            _params = {
                'title' : post.title,
                'body' : post.content,
                'type' : 'text'
            }
            client.post(url, data = params)

            return redirect('view_post',pk=new_post.pk)


    elif request.method == 'GET':
        form = PostEditForm()

    ctx={                                           #딕셔너리
            'categories':categories,
            'form':form,
        }


    return render(request, 'edit_post.html',ctx)

@login_required
def create_comment(request,pk): #urls에서 패턴을 그루핑 했기때문에 pk도 필요
    '''if request.user.is_authenticated() is False:
        raise Exception('로그인 고')'''
    post = get_object_or_404(Post,pk=pk,is_published=True)  #발행된 글에만 댓글 달 수 있도록함
    if request.method=="POST":
        form = CommentEditForm(request.POST)    #POST방식으로 전달된 정보를 인자로 전달
        if form.is_valid():
            comment = form.save(commit = False) #모델폼 세이브는 저장한 모델의 인스턴스 객체를 반환함(유저정보와 포스트 정보가 아직 없으므로 저장 허가하지 않음)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('view_post',pk=post.pk) #인자는 '이동할 url의 이름' 과 그루핑한 pk도 전달

    else:
        form = CommentEditForm()


    return redirect('view_post',pk=post.pk)
