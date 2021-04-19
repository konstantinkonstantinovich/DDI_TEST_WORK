from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView

from django.views.generic.edit import FormMixin

from django.core.paginator import Paginator
from django.views.generic.list import MultipleObjectMixin
from django.template.loader import render_to_string

from .models import Post, Comment

from .forms import CommentForm


def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(
        request,
        'index.html',
        context={
            'num_visits': num_visits,
        }
    )


class LoginForm(LoginView):
    model = User
    template_name = "registration/login.html"
    success_url = '/Blog/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        messages.add_message(self.request, messages.SUCCESS, 'Authorization success!')
        return HttpResponseRedirect(self.get_success_url())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/Blog/login/')


class RegistrationForm(CreateView):
    model = User
    template_name = "registration/registration.html"
    fields = ['username', 'email', 'password', 'first_name', 'last_name']
    success_url = '/Blog/login/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.cleaned_data['username']
        email = form.cleaned_data['email']
        passw = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        User.objects.create_user(
            username=user,
            email=email,
            password=passw,
            first_name=first_name,
            last_name=last_name,
        )
        messages.add_message(self.request, messages.SUCCESS, 'Registration success!')
        return redirect(self.success_url)


class PostDetailView(MultipleObjectMixin, DetailView):
     model = Post
     paginate_by = 5

     def get_context_data(self, **kwargs):
         post = self.get_object()
         object_list = Comment.objects.filter(post=self.get_object())
         comment_list = Comment.objects.filter(parent=post.pk)
         context = super(PostDetailView, self).get_context_data(object_list=object_list, **kwargs)
         context['obj'] = comment_list
         return context


# def PostDetailView(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     comments = post.comment_set.filter(active=True, parent__isnull=True)
#     paginator = Paginator(comments, 2)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             parent_obj = None
#             try:
#                 parent_id = int(request.POST.get('parent_id'))
#             except:
#                 parent_id = None
#             if parent_id:
#                 parent_obj = Comment.objects.get(id=parent_id)
#                 if parent_obj:
#                     replay_comment = comment_form.save(commit=False)
#                     replay_comment.parent = parent_obj
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post
#             user = request.user
#             new_comment.author = user
#             new_comment.save()
#
#             return redirect('Blog:post-list')
#     else:
#         comment_form = CommentForm()
#     return render(request,
#                   'Blog/post_detail.html',
#                   {'post': post,
#                    'comments': comments,
#                    'comment_form': comment_form,
#                    'page_obj': page_obj })

def CommentCreateFrom(request, post_id, comment_id):
    data = dict()
    post = post_id
    com = comment_id
    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            comment = form.cleaned_data['comment']
            if comment_id == 0:
                Comment.objects.create(
                    author=author,
                    post_id=post_id,
                    comment=comment
                )
            else:
                Comment.objects.create(
                    author=author,
                    post_id=post_id,
                    comment=comment,
                    parent_id=comment_id
                )
            messages.add_message(request, messages.SUCCESS, 'Comment create')
            return redirect('/Blog/post/'+str(post_id)+'/detail/')
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'post': post, 'com': com}
    data['html_form'] = render_to_string(
        template_name='../templates/includes/comment_form.html',
        context=context,
        request=request
    )
    return JsonResponse(data)






class PostListView(ListView):
    model = Post
    paginate_by = 2


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    success_url = '/Blog/'
    fields = ['title', 'content', 'image', 'description']

    def form_valid(self, form):
        user = self.request.user
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        description = form.cleaned_data['description']
        image = form.cleaned_data['image']
        Post.objects.create(author=user,
                            title=title,
                            content=content,
                            description=description,
                            image=image,
        )
        messages.add_message(self.request, messages.SUCCESS, 'Post created!')
        return redirect(self.success_url)


class SearchResultView(ListView):
    model = Post
    template_name = 'Blog/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(title__contains=query)
        return object_list