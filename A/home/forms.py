from django import forms
from .models import News, Comment
from accounts.models import User



class NewsCreateUpdateForm(forms.ModelForm):
    #image1 = forms.ImageField()

    class Meta:
        model = News
        fields = ('news_title', 'description', 'news_group', 'is_active', 'register_user', 'image',)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

# Search
class NewsSearchForm(forms.Form):
    search = forms.CharField(label='جستجو',  widget=forms.TextInput(attrs={'style': 'width:300px;'}))
