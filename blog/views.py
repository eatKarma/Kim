from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect

from .models import Post
from .forms import PostForm

# Create your views here.
def post_detail(request, pk):
  photo = get_object_or_404(Post, pk=pk)
  messages = (
    '<p>{pk}번 사진 보여줄게요</p>'.format(pk=photo.pk),
    '<p>주소는 {url}</p>'.format(url=photo.photo.url),
    '<p><img src="{url}" / width=600px></p>'.format(url=photo.photo.url),
    )
  return HttpResponse('\n'.join(messages))

def post_new(request):
  if request.method == "GET":
    form = PostForm()
  elif request.method == "POST":
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      obj = form.save(commit = False)
      obj.author = request.user
      obj.thumbnail = request.FILES['photo']
      obj.save()
      return redirect(post_list(request)) #이거 url함수로 연결해야함

  ctx = {
      'form': form,
  }
  return render(request, 'blog/post_edit.html', ctx)

def post_list(request):
  posts=Post.objects.filter(\
    published_date__lte=timezone.now()\
    ).order_by('published_date')
  return render(request, 'blog/post_list.html', {'posts':posts})