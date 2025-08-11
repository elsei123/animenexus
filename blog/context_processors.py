from .models import Category


def categories(request):
    return {"all_categories": Category.objects.order_by("name")}
