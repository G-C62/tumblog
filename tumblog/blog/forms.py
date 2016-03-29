from django import forms
from .models import Post
from .models import Comment
class PostEditForm(forms.ModelForm):
    class Meta:

        model = Post
        fields = ['title','category','content','is_published'] #사용할 필드 이름지정
        #fields = '__all__'
class CommentEditForm(forms.ModelForm):
    class Meta: #ModelForm에 필요한 메타정보

        model = Comment
        fields = ['content']
