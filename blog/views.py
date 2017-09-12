from django.shortcuts import render, get_object_or_404
from blog.models import *
import markdown2

# Create your views here.

def index(request):
    post_list = Post.objects.all()
    
    return render(request,'blog/index.html',{'post_list':post_list})

def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.body=markdown2.markdown(post.body,extras=
                       ["fenced-code-blocks", 
                        "cuddled-lists",
                        "metadata", 
                        "tables",
                        "spoiler",
                        ],)
#     markdown2.markdown(post.body, extras=['fenced-code-blocks'], )
#     post.body = markdown2.markdown(extensions=['codehilite']).convert(markdown_text)
    return render(request,'blog/detail.html',{'post':post})
    
def archives(request,year,month):
    posts = Post.objects.filter(created_time__year=year,
                                    created_time__month = month
                                    ).order_by('-created_time')
    return render(request,'blog/full-width.html',{'posts':posts})


def category(request,catepk):
    print('get category...',catepk)
    cate = get_object_or_404(Category,pk=catepk) 
    print(cate.name)
    posts = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/full-width.html',{'posts':posts})
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    