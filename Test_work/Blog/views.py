from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin

from .models import Post


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
    success_url = '/store/login/'

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


class PostDetailView(DetailView):
    model = Post


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