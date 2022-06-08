from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def menu():
    button1 = InlineKeyboardButton("Новые заказы", callback_data="new_orders")
    button2 = InlineKeyboardButton("Заказы на сборке", callback_data="show_orders_st1")
    button3 = InlineKeyboardButton("Поставки", callback_data="supplies")
    button4 = InlineKeyboardButton("Шк поставки", callback_data="supply_barcode")
    button5 = InlineKeyboardButton("Шк стикеров", callback_data="stickers_barcode")
    all_buttons = InlineKeyboardMarkup(
        [[button1], [button2], [button3], [button4], [button5]], row_width=1
    )
    return all_buttons


def supplies_menu():
    button1 = InlineKeyboardButton("Активные поставки", callback_data="active_supplies")
    button2 = InlineKeyboardButton("Создать поставку", callback_data="new_supply")
    button3 = InlineKeyboardButton("<<Назад", callback_data="back")
    all_buttons = InlineKeyboardMarkup([[button1], [button2], [button3]], row_width=1)
    return all_buttons


def new_order_menu():
    button2 = InlineKeyboardButton("Отправить на сборку", callback_data="set_order_st1")
    button3 = InlineKeyboardButton("<<Назад", callback_data="back")
    all_buttons = InlineKeyboardMarkup([[button2], [button3]], row_width=1)
    return all_buttons


def make_new_supply():
    button2 = InlineKeyboardButton(
        "Добавить заказы в поставочку", callback_data="put_orders_in_supply"
    )
    button3 = InlineKeyboardButton("<<Назад", callback_data="back")
    all_buttons = InlineKeyboardMarkup([[button2], [button3]], row_width=1)
    return all_buttons


def print_menu():
    button1 = InlineKeyboardButton("Шк стикеров", callback_data="stickers_barcode")
    button2 = InlineKeyboardButton("Шк поставки", callback_data="supply_barcode")
    button3 = InlineKeyboardButton("<<Назад", callback_data="back")
    all_buttons = InlineKeyboardMarkup([[button1], [button2], [button3]], row_width=1)
    return all_buttons


def print_sticker_menu():
    button2 = InlineKeyboardButton("Шк поставки", callback_data="supply_barcode")
    button3 = InlineKeyboardButton("<<Назад", callback_data="back")
    all_buttons = InlineKeyboardMarkup([[button2], [button3]], row_width=1)
    return all_buttons


def print_supply_menu():
    button1 = InlineKeyboardButton("Шк стикеров", callback_data="stickers_barcode")
    button3 = InlineKeyboardButton("<<Назад", callback_data="back")
    all_buttons = InlineKeyboardMarkup([[button1], [button3]], row_width=1)
    return all_buttons
