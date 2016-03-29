from django.contrib import admin
from blog.models import Post
from blog.models import Comment
from blog.models import Category

class PostAdmin(admin.ModelAdmin):  #맞춤설정 내용 포함
    list_display = ('id', 'title', 'created_at',)
    list_display_links=('id', 'title',)
    list_filter = ('title',)
    search_fields = ('content',)
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)
