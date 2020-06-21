from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, reverse, redirect, get_object_or_404
from . import models
from django.core.exceptions import ObjectDoesNotExist
from . import forms
from django.views.generic import View, FormView, ListView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from second_shop.models import UserItem

class AuthView(FormView):
    template_name = 'shop/auth.html'
    form_class = forms.AuthForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return redirect(reverse('shop_main'))
            else:
                error = "Пользователь не найден"
                form = self.form_class
                return render(request, 'shop/auth.html', {'form': form, 'error': error, 'user': user})


class RegisterView(FormView):
    template_name = 'shop/register.html'
    form_class = forms.RegisterForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = models.UserModel.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            money=data['money']
        )
        user.save()
        return redirect('auth')


class ShopMainView(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'shop/auth_user_shop.html')
        else:
            return render(request, 'shop/base_shop.html')
@login_required(login_url='/auth/')
def auth_out(request):
    logout(request)
    return redirect('shop_main')

class CategoryView(ListView):
    def get(self, request, *args, **kwargs):
        items = models.ItemModel.objects.filter(category=request.GET.get('category'))
        if request.user.is_authenticated:
            return render(request, 'shop/category_auth.html', {'items': items})
        else:
            return render(request, 'shop/category.html', {'items': items})

class ProfileView(LoginRequiredMixin, DetailView):
    model = models.UserModel
    login_url = '/auth/'

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/profile.html')


class AddMoneyView(LoginRequiredMixin, View):
    login_url = '/auth/'

    def get(self, request, *args, **kwargs):
        form = forms.RegisterForm()
        return render(request, 'shop/add_money.html', {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            user.money = int(user.money) + int(request.POST['money'])
            user.save()
        except TypeError:
            form = forms.RegisterForm()
            error = "Надо ввести число"
            return render(request, 'shop/add_money.html', {'form': form, 'error': error})
        return redirect(reverse('profile'))


@login_required(login_url='/auth/')
def delete(requset):
    user = requset.user
    logout(requset)
    user.delete()
    return redirect(reverse('shop_main'))


class ItemView(DetailView):
    model = models.ItemModel


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.template_name = 'shop/auth_item.html'
            return super().get(request, *args, **kwargs)
        else:
            self.template_name = 'shop/item.html'
            return super().get(request, *args, **kwargs)

@login_required(login_url='/auth/')
def add_trash(request):
    user = request.user
    item = models.ItemModel.objects.get(pk=request.GET.get('item_pk'))
    user.trash.add(item)
    user.save()
    return render(request, 'shop/auth_item.html', {'object': item})


class TrashView(LoginRequiredMixin, ListView):
    login_url = '/auth/'

    def get(self, request, *args, **kwargs):
        user = request.user
        items = user.trash.all()
        if items:
            return render(request, 'shop/trash.html', {'items': items})
        else:
            return render(request, 'shop/empty_trash.html')

@login_required(login_url='/auth/')
def buy_item(request):
    user = request.user
    item = models.ItemModel.objects.get(pk=request.GET.get('item_pk'))
    if int(user.money) < int(item.price):
        return render(request, 'shop/no_money.html', {'items': user.trash.all()})
    else:
        user.money = int(user.money) - int(item.price)
        user.trash.remove(item)
        user.save()
        return redirect(reverse('profile'))

@login_required(login_url='/auth/')
def delete_item(request):
    user = request.user
    item = models.ItemModel.objects.get(pk=request.GET.get('item_pk'))
    user.trash.remove(item)
    user.save()
    return redirect(reverse('trash'))


class WriteMessageView(LoginRequiredMixin, View):
    login_url = '/auth/'

    def get(self, request):
        item = UserItem.objects.get(pk=request.GET.get('item_pk'))
        user_to = item.user
        user_from = request.user
        try:
            chat = models.ChatModel.objects.get(user_from=user_from, user_to=user_to)
            if request.user.has_perm('shop.view_chat' + str(chat.pk)):
                return redirect(reverse('chat_view') + f'?chat_pk={chat.pk}')
            else:
                return redirect('profile')
        except ObjectDoesNotExist:
            chat = models.ChatModel.objects.create(user_from=user_from, user_to=user_to, creator=user_from)
            chat_codename = 'view_chat' + str(chat.pk)
            content_type = ContentType.objects.get_for_model(models.ChatModel)
            permission = Permission.objects.create(
                codename=chat_codename,
                name="Can view this chat",
                content_type=content_type
            )
            user_to.user_permissions.add(permission)
            user_from.user_permissions.add(permission)
            return redirect(reverse('chat_view') + f'?chat_pk={chat.pk}')



class OneChatView(LoginRequiredMixin, View):
    login_url = '/auth/'

    def get(self, request):
        chat = models.ChatModel.objects.get(pk=request.GET.get('chat_pk'))
        user = get_object_or_404(models.UserModel, pk=request.user.pk)
        permission = 'shop.view_chat' + str(chat.pk)
        if user.has_perm(permission):
            form = forms.MessageForm()
            messages = models.MessageModel.objects.filter(chat=chat)
            return render(request, 'shop/chat_user1.html', {'form': form, 'messages': messages, 'chat': chat})
        else:
            return redirect('profile')


    def post(self, request):
        chat = models.ChatModel.objects.get(pk=request.GET.get('chat_pk'))
        if request.user.has_perm('shop.view_chat' + str(chat.pk)):
            form = forms.MessageForm(request.POST)
            message = form.save(commit=False)
            message.chat = chat
            message.user = request.user
            message.save()
            return redirect(reverse('chat_view') + f'?chat_pk={chat.pk}')
        else:
            return redirect('profile')


class ChatsView(LoginRequiredMixin, View):
    login_url = '/auth/'

    def get(self, request):
        chats_from_me = request.user.chats_from_me.all()
        chats_to_me = request.user.chats_to_me.all()
        return render(request, 'shop/my_chats.html', {'chats_from_me': chats_from_me, 'chats_to_me': chats_to_me})


@login_required(login_url='/auth/')
def delete_chat(request):
    chat = models.ChatModel.objects.get(pk=request.GET.get('chat_pk'))
    if request.user.has_perm('shop.view_chat' + str(chat.pk)):
        chat.delete()
        return redirect('my_chats')
    else:
        return redirect('profile')