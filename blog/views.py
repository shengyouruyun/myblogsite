from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import EmailPostForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag 
from django.db.models import Count
def post_list(request, tag_slug=None):
	all_posts = Post.objects.all()
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		all_posts = all_posts.filter(tags__in=[tag])
	paginator = Paginator(all_posts, 3)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)

	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request, 'blog/post/list.html', {'page':page, 'posts':posts,'tag':tag})



def post_details(request, post):
	post = get_object_or_404(Post, slug=post)
	#list of activate comments for this post
	# List of similar posts
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
	comments = post.comments.filter(active=True)
	new_comment = None
	if request.method == 'POST':
		# a COMMENT WAS POSTED
		params = request.POST
		comment_form = CommentForm(params)
		if comment_form.is_valid():
			#create comment object but not save to db
			new_comment = comment_form.save(commit=False)
			#assige current post to the comment
			new_comment.post = post
			#save comment to the database
			new_comment.save()
	else:
		comment_form = CommentForm()
	return render(request, 'blog/post/detail.html',
					 {'post':post, 'comments':comments,
					  'comment_form':comment_form, 
					  'new_comment':new_comment,
					  'similar_posts': similar_posts})


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






