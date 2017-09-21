from django.shortcuts import render, get_object_or_404, redirect
from blog.models import *
import markdown2
from .forms import CommentForm
from django.db.transaction import commit

from django.views.generic import ListView,DetailView
from django.forms.forms import Form
from django.core.paginator import Paginator

# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by  = 3
# def index(request):
#     post_list = Post.objects.all()
#     
#     return render(request,'blog/index.html',{'post_list':post_list})
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    
    def get(self,request,*args,**kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView,self).get(request,*args,**kwargs)
        self.object.increase_read_counts()
        return response
    
    def get_object(self, queryset=None):
         # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView,self).get_object(queryset=None)
        post.body=markdown2.markdown(post.body,extras=
                       ["fenced-code-blocks", 
                        "cuddled-lists",
                        "metadata", 
                        "tables",
                        "spoiler",
                        ],)
        return post
    
    def get_context_data(self,**kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        comment_list_length = len(comment_list_length)
        context.update({
                'form':form,
                'comment_list':comment_list,
                'comment_list_length':comment_list_length
                })
        return context
    
def detail(request,pk):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip  = x_forwarded_for.split(',')[0]
#     else:
#         ip  = request.META.get('REMOTE_ADDR')
#     
#     ip2 = request.get_host()
#     print('ip:',ip)
#     print('ip2:',ip2)
    
    
    post = get_object_or_404(Post,pk=pk)
    post.increase_read_counts()
    post.body=markdown2.markdown(post.body,extras=
                       ["fenced-code-blocks", 
                        "cuddled-lists",
                        "metadata", 
                        "tables",
                        "spoiler",
                        ],)
#     markdown2.markdown(post.body, extras=['fenced-code-blocks'], )
#     post.body = markdown2.markdown(extensions=['codehilite']).convert(markdown_text)

    form = CommentForm()
    comment_list = post.comment_set.all()
    comment_list_length =len(comment_list)
    context = {
        'post':post,
        'form':form,
        'comment_list':comment_list,
        'comment_list_length':comment_list_length
        }
    
    return render(request,'blog/detail.html',context = context)
 
class ArchivesView(IndexView):
    def get_queryset(self):
        return IndexView.get_queryset(self).filter(created_time__year=self.kwargs.get('year'),
                                    created_time__month = self.kwargs.get('month')
                                    ).order_by('-created_time')
    
# def archives(request,year,month):
#     posts = Post.objects.filter(created_time__year=year,
#                                     created_time__month = month
#                                     ).order_by('-created_time')
#     return render(request,'blog/full-width.html',{'posts':posts})

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('catepk')) 
#         posts = Post.objects.filter(category=cate).order_by('-created_time')
        return super(CategoryView, self).get_queryset().filter(category=cate)
# def category(request,catepk):
# #     print('get category...',catepk)
#     cate = get_object_or_404(Category,pk=catepk) 
# #     print(cate.name)
#     posts = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request,'blog/full-width.html',{'posts':posts})
    
    
def post_comment(request,post_pk):
    post = get_object_or_404(Post,pk=post_pk)
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip  = x_forwarded_for.split(',')[0]
#     else:
#         ip  = request.META.get('REMOTE_ADDR')
#     
#     ip2 = request.get_host()
#     print('ip:',ip)
#     print('ip2:',ip2)
    if request.method == 'POST':
        form = CommentForm(request.POST)
    
        if form.is_valid():
            comment = form.save(commit = False)
            post.increase_comment_counts()
            comment.post = post
            comment.save()
            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
#             comment_list_length = len(comment_list)
            context = {
                'post':post,
                'form':form,
                'comment_list':comment_list,
#                 'comment_list_length':comment_list_length
                }
            return render(request,'blog/detail.html',context=context)
    else:
        #不是post请求
        return redirect(post)
            
def about(request):
    return render(request,'blog/about.html')
def contact(request):
    return render(request,'blog/contact.html')      
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    