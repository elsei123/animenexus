from django.core.cache import cache
from .models import Category

def all_categories_context(request):
    categories = cache.get("all_categories")
    if categories is None:
        categories = list(Category.objects.order_by("name"))
        cache.set("all_categories", categories, 300)  # guarda por 5 minutos
    return {"all_categories": categories}

