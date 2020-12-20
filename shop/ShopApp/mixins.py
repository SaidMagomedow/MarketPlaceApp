from django.contrib.auth.models import AnonymousUser
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from .models import *


# Данный класс позволяет нам исользовальзовать content_type категорий ,
# после чего будем использовать их при выведении на главной странице и в описании товаров
class CategoryDetailMixin(SingleObjectMixin):
    CATEGORY_SLUG2PRODUCT_MODEL = {
        'Notebook': Notebook,
        'Smartphones': Smartphone,
        'TV': TV,
        'headphones': Headphones,
        'tablets': Tablet,
        'console': Console,
        'category': Category
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_SLUG2PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.all()
            context['category_products'] = model.objects.all()
            return context
        else:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.all()
            #            context['slug'] = Category.objects.slug()
            context['ct_model'] = self.model._meta.model_name
            return context


# В этом классе содержится наша корзина и происходит некоторая логика, мы проверяем авторизован ли пользователь ,
# если да и модель Customer еще не заполнена этим пользователем , то заполняем её тем пользователем который
# авторизовался если нет и корзины , то добавляем к этому пользователю новую корзину если пользователь не
# авторизован , то делаем его анонимным , но этот код не несёт особой логики , так как неавторизованный пользователь
# не может добавить товар в корзину
class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
