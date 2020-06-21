from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.views.generic import View, ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from shop.models import UserModel, ChatModel, MessageModel
from shop.forms import MessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class SecondShopView(View):
    def get(self, request):
        items = models.UserItem.objects.all()
        if request.user.is_authenticated:
            return render(request, 'second_shop/second_shop_auth.html', {'items': items})
        else:
            return render(request, 'second_shop/second_shop_base.html', {'items': items})

class AddItemView(LoginRequiredMixin, View):
    login_url = '/auth/'

    def get(self, request):
        form = forms.UserItem()
        return render(request, 'second_shop/add_item.html', {'form': form})

    def post(self, request):
        user = request.user
        form = forms.UserItem(request.POST, request.FILES)
        try:
            item = form.save(commit=False)
            item.user = user
            item.save()
            return redirect(reverse('second_shop'))
        except Exception:
            return self.get(request)


class ItemView(DetailView):
    model = models.UserItem
    context_object_name = 'item'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.template_name = 'second_shop/auth_item.html'
            return super().get(request, *args, **kwargs)
        else:
            self.template_name = 'second_shop/item.html'
            return super().get(request, *args, **kwargs)


class MyItemsView(LoginRequiredMixin, ListView):
    login_url = '/auth/'

    paginate_by = 5
    template_name = 'second_shop/my_items.html'

    def get(self, request, *args, **kwargs):
        self.user = request.user
        self.queryset = self.user.my_items.all()
        return super().get(request, *args, **kwargs)

@login_required(login_url='/auth/')
def delete_item(request):
    item = models.UserItem.objects.get(pk=request.GET.get('item_pk'))
    item.delete()
    return redirect(reverse('my_items'))

class ChangeItemView(LoginRequiredMixin, View):
    login_url = '/auth/'

    def get(self, request):
        item = models.UserItem.objects.get(pk=request.GET.get('item_pk'))
        form = forms.UserItem(instance=item)
        return render(request, 'second_shop/change_myitem.html', {'form': form, 'item': item})

    def post(self, request):
        item = models.UserItem.objects.get(pk=request.GET.get('item_pk'))
        item.title = request.POST['title']
        item.description = request.POST['description']
        item.price = request.POST['price']
        item.category = request.POST['category']
        try:
            item.image = request.FILES['image']
        except KeyError:
            pass
        item.save()
        return redirect('my_items')

class SearchView(View):

    def get(self, request):
        form = forms.SearchForm()
        return render(request, 'second_shop/search.html', {'form': form})

    def post(self, request):
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            items = models.UserItem.objects.filter(title__icontains=f'{data["title"]}')
            if request.user.is_authenticated:
                return render(request, 'second_shop/second_shop_auth.html', {'items': items})
            else:
                return render(request, 'second_shop/second_shop_base.html', {'items': items})