from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


# тут мы берем первые 10 которые мы выведем на главную страницу
class LatestProductsManager(object):

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:10]
            products.extend(model_products)
        return products


class LatestProducts:
    object = LatestProductsManager()


class CategoryManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()


# Эта модель отвечает за категории товаров
class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    objects = CategoryManager()

    def __str__(self):
        return self.name

    # Данная функция перенаправляет на url category_detail и в качестве регулярного выражения бере  slug , который мы задаём
    # при добавлении новых категорий , если будете добавлять новые категории ,  пишите slug с маленькой буквы
    # так как если вставить в качестве регулярного выражения slug с большой буквы будет ошибка

    def get_absolute_url(self):
        return reverse('ShopApp:category_detail', kwargs={'slug': self.slug})


class ProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()


# Это родительский класс для других моделей , которые буду отвечать за товар


class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey('Category', verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name='Наименовиние')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")
    color = models.CharField(max_length=100, verbose_name='Цвет')
    manufacturer = models.CharField(max_length=250, verbose_name='Производитель')
    reviews_in_y = models.IntegerField(verbose_name='Отзывы на Яндекс маркете')

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()


class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы аккумулятора')
    operating_system = models.CharField(max_length=100, verbose_name='Операционная система')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True, verbose_name='Наличие SD карты')
    sd_volume_max = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Максимальный объем встраивамой памяти'
    )
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')
    operating_system = models.CharField(max_length=100, verbose_name='Операционная система')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


# Эта модель отвечает за хранение характеристик наушников


class Headphones(Product):
    MY_CHOICES_WERELESS = (
        ('Проводные', 'Проводные'),
        ('Безпроводные', 'Безпроводные'),
        ('Полупроводные', 'Полупроводные'),
    )
    MY_CHOICES_CONNECTION = (
        ('Bluetooth', 'BL'),
        ('Радиоволны', 'RD'),
        ('ИК-порт', 'IK'),
        ('NFC', 'NC'),
        ('Wi-Fi', 'WF')

    )
    # Вид
    view = models.CharField(max_length=250, verbose_name='Вид')
    wireless = models.CharField(max_length=20, choices=MY_CHOICES_WERELESS, verbose_name="Тип наушников")
    Connection = models.CharField(max_length=30, choices=MY_CHOICES_CONNECTION, verbose_name='Вид соединения')
    microphone = models.BooleanField(default=False, verbose_name='Наличие микрофона')

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


# Эта модель отвечает за хранение характеристик планшета
class Tablet(Product):
    diagonal = models.FloatField(verbose_name='Диагональ экрана')
    type_display = models.CharField(max_length=100, verbose_name='Тип дисплея')
    operating_system = models.CharField(max_length=100, verbose_name='Операционная система')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    sd = models.BooleanField(default=True, verbose_name='Наличие SD карты')
    sd_volume_max = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Максимальный объем встраивамой памяти'
    )
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')
    accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


# Эта модель отвечает за хранение характеристик телевизора
class TV(Product):
    diagonal = models.FloatField(verbose_name='Диагональ экрана')
    type_display = models.CharField(max_length=100, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    sd = models.BooleanField(default=True, verbose_name='Наличие SD карты')
    sd_volume_max = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Максимальный объем встраивамой памяти'
    )
    smartTV = models.BooleanField(default=False, verbose_name='Смарт ТВ')

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Console(Product):
    type = models.CharField(max_length=50, verbose_name='Тип')
    memory = models.IntegerField(verbose_name='Память')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    processes = models.CharField(max_length=255, verbose_name='Процессор')
    video = models.CharField(max_length=255, verbose_name='Графический процессор')

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


# Модель отвечает за добавление товаров в корзину
class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return 'Продукт:{}(для корзины)'.format(Product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


# Модель , которая хранит данные пользователя для осуществления доставки
class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    adress = models.CharField(max_length=250, verbose_name='Адрес')
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return 'Покупатель: {}'.format(self.user)

# Эта модель отвечает за создание корзины
class Cart(models.Model):
    owner = models.ForeignKey(Customer, verbose_name='Владелец', null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField('CartProduct', blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

# Эта модель хранит в себе , то что заказал пользователь
class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders',
                                 on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)
