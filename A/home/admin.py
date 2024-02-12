from django.contrib import admin
from .models import News, Category, Comment, NewsLike, NewsDislike, UserReport

# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ( 'news_group', 'is_active', 'news_updated', 'news_title')
    search_fields = ('news_title',)
    list_filter = ('news_updated', 'is_active')
    raw_id_fields = ()
admin.site.register(News, NewsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sel', 'subslug', 'slug')
    search_fields = ('name',)
    list_filter = ('subslug',)
    #prepopulated_fields = {'slug': ('description',)}
admin.site.register(Category, CategoryAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'created', 'is_reply')
    raw_id_fields = ('user', 'news', 'reply')


@admin.register(NewsLike)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'news')
    raw_id_fields = ('user', 'news')
#admin.site.register(NewsLikeDislike)


@admin.register(NewsDislike)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'news')
    raw_id_fields = ('user', 'news')

@admin.register(UserReport)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('admin_user', 'violating_user', 'report_text', 'created', 'number_violation', 'comment')
    raw_id_fields = ('admin_user', 'violating_user', 'comment')

#admin.site.register(UserReport, ReportAdmin)