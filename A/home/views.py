from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import News, Category, Comment, NewsLike, NewsDislike, UserReport
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import NewsCreateUpdateForm, CommentCreateForm, CommentReplyForm, NewsSearchForm
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class HomeView(View):
    form_class = NewsSearchForm

    def get(self, request):
        news = News.objects.filter(is_active=True)
        categories = Category.objects.all()
        if request.GET.get('search'):  # News search
            news = news.filter(description__contains=request.GET['search'])  # Field lookups

        return render(request, 'home/home.html', {'news':news, 'categories':categories, 'form':self.form_class})


class NewsDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.news_instance = get_object_or_404(News, pk=kwargs['news_id'])
        self.news_instance.news_see = self.news_instance.news_see+1
        self.news_instance.save()
        self.category_instance = get_object_or_404(Category, slug=kwargs['category_slug'])

        return super().setup(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):  #news_id, category_slug
       # news = get_object_or_404(News, kwargs['news_id'])
        #category = get_object_or_404(Category, slug=category_slug)
        comments = self.news_instance.ncomments.filter(is_reply=False)  #Only original (parent) comments are shown
        can_like = False
        #new1=News.objects.filter(id=kwargs['news_id'])
        #new1.news_see+=new1.news_see
        if request.user.is_authenticated and self.news_instance.user_can_like(request.user):
            can_like = True

        can_dislike = False
        if request.user.is_authenticated and self.news_instance.user_can_dislike(request.user):
            can_dislike = True
        return render(request, 'home/detail.html', {'news':self.news_instance, 'category':self.category_instance,
                                  'comments':comments, 'form':self.form_class, 'reply_form':self.form_class_reply,
                                  'can_like':can_like, 'can_dislike':can_dislike})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.news = self.news_instance
            new_comment.save()

            # گزارش تخلف در صورت نیاز
            '''if new_comment.violation_reported:
                self.report_user_violation(new_comment.user, new_comment.text, new_comment)'''

            messages.success(request, 'کامنت شما با موفقیت ارسال شد', 'success')
            return redirect('home:news_detail', self.news_instance.id, self.category_instance.slug)

    '''def report_user_violation(self, reported_user, comment_text, comment_instance):
        # افزایش تعداد تخلف برای کاربر
        #user = User.objects.get(id=user_id)
        user_report, created = UserReport.objects.get_or_create(
            admin_user = request.user,
            violating_user = reported_user,
            comment = comment_instance,
            report_text = f"تخلف برای کاربر گزارش شده است{reported_user.username} با کامنت: {comment_text}"
        )
        user_report.number_violation += 1
        user_report.save()

        # اگر تعداد تخلف به سه تا رسید، کاربر را deactivate کنید
        if user_report.number_violation >= 3:
            reported_user.is_active = False
            reported_user.save()
            messages.error(self.request,
                           f'حساب کاربری {reported_user.username} به دلیل تعداد تخلف‌های بیش از حد غیرفعال شد.')

        # نمایش اطلاعات کامنت متخلف به کاربر
        messages.info(self.request,
                      f'کامنت متخلف از کاربر {reported_user.username} گزارش شد. متن کامنت: {comment_text}')'''





class NewsDeleteView(LoginRequiredMixin, View):
    def get(self, request, news_id):
        news = News.objects.get(pk=news_id)
        if news.register_user.email == request.user.email:   # if news.register_user.is_admin == True:
            news.delete()
            messages.success(request, 'خبر با موفقیت حذف شد', 'success')
        else:
            messages.error(request, 'شما نمی توانید این خبر را حذف کنید', 'danger')
        return redirect('home:home')


class NewsUpdateView(LoginRequiredMixin, View):
    form_class = NewsCreateUpdateForm


    def setup(self, request, *args, **kwargs):
        self.news_instance = News.objects.get(pk=kwargs['news_id'])
        self.category_instance = Category.objects.get(slug=kwargs['category_slug'])  # <=======================
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        news = self.news_instance
        if not news.register_user.email == request.user.email:
            messages.error(request, 'شما نمی توانید این خبر را آپدیت کنید', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        news = self.news_instance
        category = self.category_instance
        form = self.form_class(instance=news)
        return render(request, 'home/update.html', {'form':form})

    def post(self, request, *args, **kwargs):
        news = self.news_instance
        category = self.category_instance
        form = self.form_class(request.POST,  request.FILES, instance=news)

        if form.is_valid():

            # ذخیره تصویر در media
            if 'image' in request.FILES:
                image = request.FILES['image']
                file_path = default_storage.save(f'media/information/{image.name}', ContentFile(image.read()))
                news.image = file_path

            form.save()

            messages.success(request, 'خبر با موفقیت بروزرسانی شد', 'success')
            return redirect('home:news_detail', news.id, category.slug)
        return render(request, 'home/update.html', {'form': form})


class NewsCreateView(LoginRequiredMixin, View):
    from_class = NewsCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.from_class()
        return render(request, 'home/create.html', {'form':form})   # 'form1':form1

    def post(self, request, *args, **kwargs):
        form = self.from_class(request.POST)

        if form.is_valid():
            new_info = form.save(commit=False)
            new_info.news_title = form.cleaned_data['news_title']
            new_info.description = form.cleaned_data['description']
            new_info.register_user = form.cleaned_data['register_user']

            # ذخیره تصویر در media
            if 'image' in request.FILES:
                image = request.FILES['image']
                file_path = default_storage.save(f'media/information/{image.name}', ContentFile(image.read()))
                new_info.image = file_path

            new_info.is_active = form.cleaned_data['is_active']
            new_info.user = request.user
            new_info.save()

            messages.success(request, 'یک خبر جدید با موفقیت ایجاد شد', 'success')
            return redirect('home:news_detail', new_info.id, new_info.news_group.slug)
        return render(request, 'home/create.html', {'form': form})


class IndexView(View):
    def get(self, request):
        return render(request, 'home/index.html')


class IndexPageView(View):
    def get(self, request):
        return render(request, 'home/index2.html')


class NewsAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, news_id, category_slug, comment_id):
        news = get_object_or_404(News, pk=news_id)
        category = get_object_or_404(Category, slug=category_slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.news = news
            reply.reply = comment
            reply.is_reply = True    # the comment we are saving is a reply
            reply.save()
            messages.success(request, 'پاسخ شما با موفقیت ارسال شد', 'success')
        return redirect('home:news_detail', news.id, category.slug)


# Like & Dislike for News
'''class NewsLikeView(LoginRequiredMixin, View):
    def get(self, request, news_id, category_slug):
        news = get_object_or_404(News, pk=news_id)
        category = get_object_or_404(Category, slug=category_slug)

        like, created = NewsLike.objects.get_or_create(news=news, user=request.user)
        if not created:
            messages.error(request, 'شما قبلا این خبر را لایک کرده اید.', 'danger')
        else:
            messages.success(request, 'لایک شما ثبت شد.', 'success')

        return redirect('home:news_detail', news.id, category.slug)


class NewsDislikeView(LoginRequiredMixin, View):
    def get(self, request, news_id, category_slug):
        news = get_object_or_404(News, pk=news_id)
        category = get_object_or_404(Category, slug=category_slug)

        dislike, created = NewsDislike.objects.get_or_create(news=news, user=request.user)
        if not created:
            messages.error(request, 'شما قبلا به این خبر نظر منفی داده اید.', 'danger')
        else:
            messages.success(request, 'نظر منفی شما ثبت شد.', 'success')

        return redirect('home:news_detail', news.id, category.slug)'''

# Like & Dislike for News
class NewsLikeView(LoginRequiredMixin, View):
    def get(self, request, news_id, category_slug):
        news = get_object_or_404(News, pk=news_id)
        category = get_object_or_404(Category, slug=category_slug)
        like = NewsLike.objects.filter(news=news, user=request.user)
        if like.exists():
            messages.error(request, 'نظر شما قبلا ثبت شده است.', 'danger')
        else:
            NewsLike.objects.create(news=news, user=request.user)
            messages.success(request, 'لایک شما ثبت شد.', 'success')
        return redirect('home:news_detail', news.id, category.slug)


class NewsDislikeView(LoginRequiredMixin, View):
    def get(self, request, news_id, category_slug):
        news = get_object_or_404(News, pk=news_id)
        category = get_object_or_404(Category, slug=category_slug)
        like = NewsDislike.objects.filter(news=news, user=request.user)
        if like.exists():
            messages.error(request, 'نظر شما قبلا ثبت شده است.', 'danger')
        else:
            NewsDislike.objects.create(news=news, user=request.user)
            messages.success(request, 'نظر شما ثبت شد.', 'success')
        return redirect('home:news_detail', news.id, category.slug)


