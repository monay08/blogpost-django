from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, BlogPost, LoginAttempt
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta


#def home(request):
#    return render(request, 'home.html')

def Likes(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blogdetail', args=[str(pk)]))

MAX_ATTEMPTS = 5  # Maximum allowed attempts
TIMEFRAME = 5  # Time frame in minutes for allowed attempts

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check recent login attempts
        recent_attempts = LoginAttempt.get_recent_attempts(username, minutes=TIMEFRAME)
        
        if recent_attempts >= MAX_ATTEMPTS:
            messages.error(request, "Too many failed login attempts. Please try again later.")
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Log the failed attempt
            LoginAttempt.objects.create(username=username)
            messages.error(request, "Invalid credentials, please try again.")
            return redirect('login')
    return render(request, 'login.html')

class Home(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']
    #ordering = ['-id']
    
class Detail(DetailView):
    model = Post
    template_name = 'detail-view.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(Detail, self).get_context_data(*args, **kwargs)
        
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        context['total_likes'] = total_likes
        context['liked'] = liked
        context['likers'] = stuff.likes.all()
        return context
    
class Create(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create-post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogdetail', kwargs={'pk': self.object.pk})

class AddComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add-comment.html'
    #fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    success_url = reverse_lazy('all')

class Update(UpdateView):
    model = Post
    template_name = 'update-post.html'
    fields = ('title', 'body')

    def get_success_url(self):
        # Redirect to the detail view of the updated post
        return reverse('blogdetail', kwargs={'pk': self.object.pk})
    
class Delete(DeleteView):
    model = Post
    template_name = 'delete-post.html'
    success_url = reverse_lazy('all')

class Featured(ListView):
    model = Post
    template_name = 'featured-blogs.html'
    ordering = ['-post_date']
    #ordering = ['-id']
    