from .models import Category

def category_context(request):
    return {
        'global_categories': Category.objects.all()
    }