from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import NewItemForm, EditItemForm
from .models import Category, Item,Cart
from django.http import JsonResponse

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'favorited_by': item.favorited_by.all(),
    })


@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)  # Pass FILES to handle file uploads

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')

# item/views.py

def get_data(request):
    data = Item.objects.values()  # Retrieve all data from the Item model
    data = Item.objects.values().order_by('-stocks')

    # Modify the data to include the image URL
    for item in data:
        item['image_url'] = request.build_absolute_uri(Item.objects.get(id=item['id']).image.url) if item['image'] else None

    return JsonResponse(list(data), safe=False)


@login_required
def add_to_favorite(request, pk):
    item = get_object_or_404(Item, pk=pk)
    user = request.user

    if item.favorited_by.filter(pk=user.pk).exists():
        item.favorited_by.remove(user)
        messages.success(request, 'Removed from favorites.')
    else:
        item.favorited_by.add(user)
        messages.success(request, 'Added to favorites.')

    return redirect('item:detail', pk=pk)

from django.contrib.auth.decorators import login_required

@login_required
def favorite_items(request):
    user = request.user
    favorite_items = user.favorite_items.all()  # Assuming the related_name for favorites in the Item model is 'favorited_by'

    return render(request, 'item/favorite_items.html', {
        'favorite_items': favorite_items,
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item

@api_view(['GET'])
def user_favorite_items_api_view(request, user_id):
    try:
        # Retrieve the user's favorite items based on the user_id
        favorite_items = Item.objects.filter(favorited_by__id=user_id)

        # Construct the response data
        favorite_items_data = [
            {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'image_url': request.build_absolute_uri(item.image.url) if item.image else None,
            }
            for item in favorite_items
        ]

        return Response({'favorite_items': favorite_items_data})

    except Item.DoesNotExist:
        return Response({'error': 'User favorite items not found'}, status=404)
