from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm


#메인 페이지(발행된 post가 보이는페이지)
def post_list(request):
    queryset = Post.objects.all()
    post_list=queryset.filter(published_date__lte  = timezone.now()).order_by('-published_date')
    ctx= {
        'post_list':post_list
    }
    return render(request,'blog/post_list.html',ctx)


# published_date 발행되기전에 글을 모아두는 곳
@login_required
def post_draft_list(request):
    # published_date 설정이 없는 경우를 필터링해라.
    post_list= Post.objects.filter(published_date__isnull=True).order_by('created_data')
    ctx = {
    'post_list':post_list
    }
    return render(request,'blog/post_draft_list.html',ctx)


#상세 페이지
def post_detail(request,post_pk):
    #예를 들어 pk = 100 이다 그럼 그페이지를 찾기이해서
    #post = Post.objects.get(pk = post_pk )  #post_pk⇒인자로 받은값
    post = get_object_or_404(Post, pk = post_pk)
    ctx={
        'post':post
    }
    return render(request,'blog/post_detail.html',ctx)


# post글 지우기
@login_required
def post_remove(request, post_pk):
    post = get_object_or_404(Post, pk = post_pk )
    post.delete()

    return redirect('post_list')




# 새로운 post 작성 페이지
@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False) # 임의저장(아직정장된게 아님)
            post.author = request.user #로그인 유저정보
            # post.published_date = timezone.now()⇒ 자동으로 발행되지 않기 하기위해 삭제
            post.save() # 완전 저장
            return redirect('post_detail', post_pk = post.pk )# 저장후 보여지는 페이지
    else:
        form = PostForm()
    ctx = {
    'form':form
    }
    return render(request,'blog/post_edit.html',ctx)


#form 수정페이지
@login_required
def post_edit(request,post_pk):
    post = get_object_or_404(Post, pk = post_pk)

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post=form.save(commit=False) # 임의저장(아직정장된게 아님)
            post.author = request.user #로그인 유저정보
            # post.published_date = timezone.now()⇒ 자동으로 발행되지 않기 하기위해 삭제
            post.save() # 완전 저장
            return redirect('post_detail', post_pk = post.pk )# 저장후 보여지는 페이지
    else:
        form = PostForm(instance=post) # post= get_object_or_404(Post, pk = post_pk)
    ctx={
        'form':form
    }
    return render(request,'blog/post_edit.html',ctx)


# 발행되지 않은 post를 발행해주는 기능
@login_required
def post_publish(request, post_pk):
    post = get_object_or_404(Post, pk = post_pk )
    post.publish()
    return redirect('post_detail', post_pk = post.pk )
