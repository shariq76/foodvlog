from django.shortcuts import render, get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage


# Create your views here.
def home(request, c_slug=None):
    c_page = None
    prodt = None

    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        prodt = products.objects.filter(category=c_page, available=True)
    else:
        prodt = products.objects.all().filter(available=True)

    cat = Category.objects.all()
    paginator = Paginator(prodt, 4)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        pro = paginator.page(page)
    except(EmptyPage, InvalidPage):
        pro = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'pr': prodt, 'ct': cat, 'pg': pro})


def prodDetails(request, c_slug, product_slug):
    try:
        prodt = products.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'item.html', {'pr': prodt})


def searching(request):
    prod = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        if query.isspace() == True:
            messages.info(request, 'Please enter a valid keyword')
            return redirect('/')
        else:
            prod = products.objects.all().filter(Q(name__contains=query) | Q(desc__contains=query))
            return render(request, 'search.html', {'qr': query, 'pr': prod})
