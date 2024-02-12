from django.db import models
from accounts.models import User
#from django.urls import reverse
# from django.contrib.auth import get_user_model

# Create your models here.
class Category(models.Model):
    sel = models.ForeignKey('self', on_delete=models.CASCADE, related_name="a", null=True, blank=True)
    subslug = models.BooleanField()
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class News(models.Model):
    category=models
    news_title = models.CharField(max_length=255,verbose_name='عنوان')
    description = models.TextField()
    image = models.ImageField(upload_to='information/%Y/%m/%d/', null=True, blank=True)  # information==news
    register_date = models.DateTimeField(auto_now_add=True)
    news_updated = models.DateTimeField(auto_now=True)
    register_user = models.ForeignKey(User, on_delete=models.CASCADE)
    news_group = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category1',)
    news_see = models.IntegerField(auto_created=True, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-register_date', 'news_title')

    def __str__(self):
        return self.news_title

    def likes_count(self):
        return NewsLike.objects.filter(news=self).count()

    def Dislikes_count(self):
        return NewsDislike.objects.filter(news=self).count()    # return self.ndislikes.count()

    def user_can_like(self, user):   # Disabling the like button in the site view
        user_like = user.ulikes.filter(news=self)
        if user_like.exists():
            return True
        return False

    def user_can_dislike(self, user):   # Disabling the dislike button in the site view
        user_dislike = user.udislikes.filter(news=self)
        if user_dislike.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='ncomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE,
                              related_name='rcomments', null=True, blank=True)  #Because it is not clear whether this text is a comment or a reply, so we leave this field empty first
    is_reply = models.BooleanField(default=False)   #Is this comment an answer or not?
    body = models.TextField(max_length=500, verbose_name='متن کامنت')   #Comment text
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'


class NewsLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulikes')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='nlikes')


    def __str__(self):
        return f'{self.user.name} {self.user.family} - {self.news.news_group.slug}/ {self.news.news_title}'


class NewsDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='udislikes')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='ndislikes')

    def __str__(self):
        return f'{self.user.name} {self.user.family} - {self.news.news_group.slug}/ {self.news.news_title}'

'''class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulikes')  
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='nlikes')  

    class Meta:
        abstract = True    # این یک مدل انتزاعی است


class NewsLike(Like):
    def __str__(self):
        return f'{self.user.name} {self.user.family} - {self.news.news_group.slug}/ {self.news.news_title}'


class NewsDislike(Like):
    def __str__(self):
        return f'{self.user.name} {self.user.family} - {self.news.news_group.slug}/ {self.news.news_title}'   '''


class UserReport(models.Model):
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_reports')
    violating_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='violations')
    report_text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)   # register date
    number_violation = models.IntegerField(default=0)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='viocomment', null=True, blank=True)

