import telebot
from config import bot_token, wb_api
import markups
from wb_api import WbApi
# import json
import beauty


bot = telebot.TeleBot(token = bot_token)
wb = WbApi(wb_api)

@bot.message_handler(commands='start')
def starts(message):
    bot.send_message(message.chat.id, 'Тут вы можете оформить поставочку: ', reply_markup=markups.menu())


@bot.callback_query_handler(func=lambda call: True)
def callbacks(callback):
    if callback.data == 'new_orders':
        new_orders = wb.get_orders(status=0)
        if new_orders['orders']:
            message = beauty.beautiful_new_order_messages(new_orders)
            bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=message, reply_markup=markups.new_order_menu())
        else:
            bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text='Нет новых заказов', reply_markup=markups.menu())


    if callback.data == 'active_supplies':
        active_supply = wb.active_supplies()['supplies'][0]['supplyId']
        bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=f'Активные поставки: {active_supply}', reply_markup=markups.make_new_supply())

    if callback.data == 'show_orders_st1':
        orders = wb.get_orders(status=1)
        if orders['orders']:
            message = beauty.beautiful_order_messages_status12(orders)
            bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=message, reply_markup=markups.make_new_supply())
        else:
            bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text='Нет заказов на сборке', reply_markup=markups.menu())

    if callback.data == 'new_supply':
        try:
            wb.new_supply()['error']
            bot.edit_message_text(f'Уже есть активная поставка', callback.from_user.id, callback.message.message_id, reply_markup=markups.make_new_supply())
        except KeyError:    
            supply = wb.new_supply()['supplyId']
            bot.edit_message_text(f'Код новой поставки {supply}', callback.from_user.id, callback.message.message_id, reply_markup=markups.make_new_supply())

    if callback.data == 'supplies':
        bot.edit_message_text('Меню поставочек хуй знает зачем оно нужно', callback.from_user.id, callback.message.message_id, reply_markup=markups.supplies_menu())

    if callback.data == 'set_order_st1':
        status = wb.set_new_orders_status1()
        if status == True:
            bot.edit_message_text('Товары успешно добавлены на сборку!', callback.from_user.id, callback.message.message_id, reply_markup=markups.menu())
        elif status == 'Нет новых заказов':
            bot.edit_message_text('Новых заказов нет', callback.from_user.id, callback.message.message_id, reply_markup=markups.menu())
        else: 
            bot.edit_message_text('Упс, какая-то ошибка', callback.from_user.id, callback.message.message_id, reply_markup=markups.menu())

    if callback.data == 'put_orders_in_supply':
        try:
            supply_id =  wb.active_supplies()['supplies'][0]['supplyId']
        except IndexError:
            bot.edit_message_text('Нет активной поставки, создайте поставку', callback.from_user.id, callback.message.message_id, reply_markup=markups.menu())
            supply_id = 0
        print(supply_id)
        if supply_id:
            orders = wb.get_orders(status=1)['orders']
            order_list = []
            print(orders)
            for i in range(0, len(orders)):
                order_list.append(orders[i]['orderId'])
            print(order_list)
            if order_list:
                print(wb.put_orders_in_supply(supply_id, order_list))
                bot.edit_message_text('Товар успешно ', callback.from_user.id, callback.message.message_id, reply_markup=markups.print_menu())
            else:
                bot.edit_message_text('Нет товаров на сборке', callback.from_user.id, callback.message.message_id, reply_markup=markups.menu())
        else:
            bot.edit_message_text('Нет активной поставки, создайте поставку', callback.from_user.id, callback.message.message_id, reply_markup=markups.menu())
            

    if callback.data == 'stickers_barcode':
        try:
            supply_id = wb.active_supplies()['supplies'][0]['supplyId']
            print(supply_id)
            orders = wb.supply_orders(supply_id)['orders']
            order_list = []
            for order in orders:
                order_list.append(int(order['orderId']))
            print(orders)
            print(order_list)
            if orders:
                print(wb.order_stickers_pdf(order_list))
                beauty.orders_beautyfier()
                bot.edit_message_text('Наклейте на ебаные посылочки', callback.from_user.id, callback.message.message_id, reply_markup=markups.print_sticker_menu())
                bot.send_document(callback.from_user.id, document=open('images/img_orders.jpg', 'rb'))
                for order in order_list:
                    print(wb.set_order_status(order, 2))
            else: 
                bot.edit_message_text('В поставке нет заказов', callback.from_user.id, callback.message.message_id, reply_markup=markups.menu())

        except IndexError:
            bot.edit_message_text('Нет активной поставки, создайте поставку', callback.from_user.id, callback.message.message_id, reply_markup=markups.menu())
            
    if callback.data == 'supply_barcode':
        try:
            supply_id = wb.active_supplies()['supplies'][0]['supplyId']
            wb.supply_barcode(supply_id)
            beauty.supply_beautyfier(supply_id)
            bot.edit_message_text('Вот ваш ебаный баркод поставки', callback.from_user.id, callback.message.message_id, reply_markup=markups.print_supply_menu())
            bot.send_document(callback.from_user.id, document=open('images/img_with_watermark.jpg', 'rb'))

        except IndexError:
            bot.edit_message_text('Нет активной поставки, создайте поставку', callback.from_user.id, callback.message.message_id, reply_markup=markups.menu())
        

    if callback.data == 'back':
        bot.edit_message_text('yes we are working here', callback.from_user.id, callback.message.message_id, reply_markup=markups.menu())

bot.polling(non_stop=True)