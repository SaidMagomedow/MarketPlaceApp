from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here
from django.views.generic import DetailView, View
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .mixins import *
from .forms import OrderForm
from django.db import transaction
from .utils import recalc_cart




# Этот класс позволяет выводить список категорий на главное страцине использовуя цикл
# Изначально мы берем список наших категорий , добавляем их в JSON формат
# и в функции dispatch в self.model записываем content_type тех моделей которые мы записывали в JSON формат
#  через которые можем определять в какие модели нам зайти
class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'Notebook': Notebook,
        'Smartphones': Smartphone,
        'TV': TV,
        'headphones': Headphones,
        'tablets': Tablet,
        'console': Console,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = "product"
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


class Index(CartMixin, CategoryDetailMixin, View):

    def get(self, request, *args, **kwargs):

        categories = Category.objects.all()
        products = LatestProducts.object.get_products_for_main_page(
            'notebook', 'smartphone', 'tv', 'headphones', 'tablet', 'console'
        )

        context = {
            'category': categories,
            'products': products,
            'cart': self.cart,
        }
        return render(request, 'index.html', context)



# Данная функция позволяет авторизоваться пользователям , она берет 2 переменные username и password ,
# проверяет их через возможности django и если пользоваетель найден , то переходим на главную страницу ,
# если нет то пробуем снова авторизоваться
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Неудалось войти , попробуйте снова')
            return redirect('/login/')
    else:
        return render(request, 'registration/login.html')


# Эта функция предназначена для регистрации пользователя,
def register(request):
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).first():
                messages.info(request, 'Логин существует')
            if User.objects.filter(email=email).first():
                messages.info(request, "Такой Email уже зарегистрирован")
            else:
                user = User.objects.create_user(username=username, first_name=first_name, email=email,
                                                password=password1,
                                                last_name=last_name)
                user.save()
                print('user зарегистрировался')
                return redirect('/login')
        else:
            print('пароли не совпадают')
        return redirect('/')
    else:
        print('user не зарегистрирован')
        return render(request, 'registration/register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def contacts(request):
    return render(request, 'contacts.html')


# не стоит переименовывать данные переменные , так как эти имена необходимы для работы DetailView , посмотрите
# документацию!!
# данный класс позволит выводить все товары сортируя их по категориям , которые пользователь выберет в списке категорий
class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories,

        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)


# Данный класс будет добалять товары в корзину В функции get мы сначала берем модель(ct_model) , slug продукта,
class AddToCart(CartMixin, CategoryDetailMixin, View):
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        if request.user.is_authenticated:
            cart_owner = self.cart.owner
        else:
            cart_owner = request.user.id
        cart_product, created = CartProduct.objects.get_or_create(
            user=cart_owner, cart=self.cart, content_type=content_type, object_id=product.id,
        )
        #        if created:
        self.cart.products.add(cart_product)
        return HttpResponseRedirect('/cart')


# Данный класс позволяет удалить товар из корзины
# Мы берем информацию о товаре , после чего перезаписываем cart_product и удаляем товар из корзины
class DeleteFromCart(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id,

        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('/cart')


class ChangeQTY(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart')


# Этот класс позволит нам оформить заказ пользователя . Изначально мы берем форму (OrderForm) и если она валидна ,
# то записываем в поля из БД , те значения , которые ввел пользователь , после чего мы сохраняем заказ ,
# закрепляем её за данным пользователем , выставив значение in_order = True , сохраняем данную корзину
# за данным пользователем и после чего доавляем этот заказ в список заказов пользователя
class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')
