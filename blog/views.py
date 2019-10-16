from django.shortcuts import render, get_object_or_404,redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm


#메인 페이지
def post_list(request):
    qs = Post.objects.all()
    post_list=qs.filter(published_date__lte  = timezone.now()).order_by('-published_date')
    ctx= {
        'post_list':post_list
    }
    return render(request,'blog/post_list.html',ctx)

#상세 페이지 
def post_detail(request,post_pk):
    #예를 들어 pk = 100 이다 그럼 그페이지를 찾기이해서
    #post = Post.objects.get(pk = post_pk )  #post_pk⇒인자로 받은값
    post = get_object_or_404(Post, pk = post_pk)
    ctx={
        'post':post
    }
    return render(request,'blog/post_detail.html',ctx)


# 새로운 post 작성 페이지
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False) # 임의저장(아직정장된게 아님)
            post.author = request.user #로그인 유저정보
            post.published_date = timezone.now()
            post.save() # 완전 저장
            return redirect('post_detail', post_pk = post.pk )# 저장후 보여지는 페이지
    else:
        form = PostForm()
    ctx = {
    'form':form
    }
    return render(request,'blog/post_edit.html',ctx)

#form 수정페이지
def post_edit(request,post_pk):
    post = get_object_or_404(Post, pk = post_pk)

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post=form.save(commit=False) # 임의저장(아직정장된게 아님)
            post.author = request.user #로그인 유저정보
            post.published_date = timezone.now()
            post.save() # 완전 저장
            return redirect('post_detail', post_pk = post.pk )# 저장후 보여지는 페이지
    else:
        form = PostForm(instance=post) # post= get_object_or_404(Post, pk = post_pk)
    ctx={
        'form':form
    }
    return render(request,'blog/post_edit.html',ctx)
