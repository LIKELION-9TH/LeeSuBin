from django.shortcuts import get_object_or_404, redirect, render, redirect
from django.utils import timezone
from .models import Blog
from django.core.paginator import Paginator
from .form import BlogPost

def home(request):
    blogs= Blog.objects
    #블로그의 모든 글 대상으로:
    blog_list = Blog.objects.all()
    #블로그 객체 n 개를 한 페이지로 자르기:
    paginator = Paginator(blog_list, 2)
    #request된 페이지가 뭔지를 알아내고(request 페이지를 변수에 담고):
    page = request.GET.get('page')
    #request된 페이지를 얻어온 뒤 사전형으로 return 해 줌:
    posts= paginator.get_page(page)
    return render(request, 'home.html', {'blogs':blogs, 'posts':posts })

def detail(request, blog_id):
    details=get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'details':details})

def new(request):
    return render(request, 'new.html')

def create(request):
    blog= Blog()
    blog.title= request.GET['title']
    blog.body=request.GET['body']
    blog.pub_date= timezone.datetime.now()
    blog.save()
    return redirect('/blog/'+str(blog.id))

def blogpost(request):
    #1. 입력된 내용 처리> method: post

    if request.method == 'POST':
        form= BlogPost(request.POST)
        if form.is_valid():
            post= form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')

    #2. 빈 페이지를 띄워주는 기능> method: get
    else:
        form = BlogPost()
        return render(request, 'new.html', {'form': form})

 