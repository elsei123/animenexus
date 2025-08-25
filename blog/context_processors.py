from django.core.cache import cache
from .models import Category


def _get_all_categories():
    cats = cache.get("all_categories")
    if cats is None:
        cats = list(Category.objects.order_by("name"))
        cache.set("all_categories", categories, 300)
    return cats


def categories(request):
    cats = _get_all_categories()
    return {"categories": cats, "all_categories": cats}


def all_categories_context(request):
    cats = _get_all_categories()
    return {"all_categories": cats}
