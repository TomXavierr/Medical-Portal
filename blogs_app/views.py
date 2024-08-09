from django.shortcuts import render, redirect
from blogs_app.models import Category, BlogPost
from django.contrib.auth.decorators import login_required

# Create your views here.
def blog_view(request,id):
    blog = BlogPost.objects.get(id=id)
  
    
    return render(request, 'blog.html', locals())

def list_by_category(request, id):
    category = Category.objects.get(id=id)
    category = category.name
    blogs = BlogPost.objects.filter(category=id, is_draft=False)
    categories = Category.objects.all()
    
    print(blogs)
    
    return render(request, 'blogs_list.html', locals())

def my_blogs(request):
    category = 'My Writings'
    blogs = BlogPost.objects.filter(author=request.user)
    categories = Category.objects.all()
    
    print(blogs)
    
    return render(request, 'my_blogs.html', locals())

# @login_required
def create_blog_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        summary = request.POST['summary']
        content = request.POST['content']
        is_draft = 'is_draft' in request.POST
        image = request.FILES.get('image')

        if title and category and summary and content and image:
            blog = BlogPost.objects.create(
                title=title,
                category=Category.objects.get(id=category),
                summary=summary,
                content=content,
                is_draft=is_draft,
                image=image,
                author=request.user  
            )
            blog.save()
            
        return redirect('my_blogs')
    else:
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'create_blog.html', context)