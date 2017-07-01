from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import EmailPostForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
def post_list(request):
	all_posts = Post.objects.all()
	paginator = Paginator(all_posts, 3)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)

	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request, 'blog/post/list.html', {'page':page, 'posts':posts})



def post_details(request, post):
	post = get_object_or_404(Post, slug=post)
	return render(request, 'blog/post/detail.html', {'post':post})


def post_share(request, post_id):
	#retrive post by id

	post = get_object_or_404(Post, id=post_id)
	sent = False
	if request.method == 'POST':
		#form was submitted
		form = EmailPostForm(request.POST)
		if form.is_valid():
			#form filed passed validation
			cd = form.cleaned_data
			#... send email
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subjet = '{} ({}) recommends you reading "{}"'.format(cd['name'],
				cd['email'], post.title)
			message = 'Read "{}" at{} \n\n{}\'s comments:{}'.format(post.title,
			post_url, cd['name'], cd['comments'])
			send_mail(subjet, message, 'wangshenganlu1990@126.com', [cd['to']])
			sent = True


	else:		
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})






