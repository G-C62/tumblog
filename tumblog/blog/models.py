from django.db import models
from django.conf import settings

class Post(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200 ,verbose_name='글 제목',help_text='글제목은 제목스럽게',)#장황하게 이름을 달아줌(사람을 위한 부가정보)
    category = models.ForeignKey('Category')
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{pk}: {title}'.format(
            pk=self.pk,
            title=self.title
        )

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post {post_pk}: Comment {pk}'.format(
            post_pk=self.post.title,
            pk=self.pk
        )

class Category(models.Model):
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
