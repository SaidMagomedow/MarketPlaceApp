from django.db import models


# Данная функция позволит посчитать общую цену товаров добавленных в категории
# Берем products с отношением многие ко многим и считаем сумму final_price всех товаров добавленых в корзину
# Если нет товаров в корзине то final_price будет равен None , изза этого может что то сломаться
# поэтому делаем проверку , если он пуст то будет равен 0 , а если нет то будет равен самому себе
# Эта функция будет вызываться лишь в AddToCart для того что бы при каждом добавлении товара в корзину , обновлялись и цена и кол-во товаров
def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.total_products = cart_data['id__count']
    cart.save()
