from wb_api import WbApi
from config import wb_api
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont

wb = WbApi(wb_api)

stock = {
    2022752346005: "🍄🍄🍄Мухомор ежовик гребенчатый🍄🍄🍄",
    2022751900000: "🍄🍄🍄Ежовик гребенчатый🍄🍄🍄",
    2012916817014: "👕👕👕Кигуруми пикачу👕👕👕",
    2012917331014: "👕👕👕Кигуруми тигр))👕👕👕",
}


def beautiful_order_messages_status12(message):
    final_message = []
    all_orders = message["orders"]
    for order in all_orders:
        order_id = int(order["orderId"].strip())
        price = int(order["convertedPrice"] / 100)
        adress = order["officeAddress"]
        name = stock[int(order["barcode"])]
        barcode = wb.order_stickers([order_id])["data"][0]["sticker"]["wbStickerId"] 
        date = order["dateCreated"][:18]
        mes = f"{name}\nШк товара:{barcode} \nЦена: {price}рублей\nДата: {date}\nАдрес: {adress}\n\n"
        final_message.append(mes)
    return "".join(final_message)


def beautiful_new_order_messages(message):
    final_message = []
    all_orders = message["orders"]
    for order in all_orders:
        price = int(order["convertedPrice"] / 100)
        adress = order["officeAddress"]
        name = stock[int(order["barcode"])]
        date = order["dateCreated"][:18]
        mes = f"{name}\nЦена: {price}рублей\nДата: {date}\nАдрес: {adress}\n\n"
        final_message.append(mes)
    return "".join(final_message)


def supply_beautyfier(supply_id):
    pages = convert_from_path("images/supply_barcode.pdf", 500)
    for page in pages:
        page.save(f"images/supply_barcode.jpg", "JPEG")

    im = Image.open("images/supply_barcode.jpg")
    im_crop = im.crop((0, 0, 1142, 570))
    im_crop.save("images/supply_barcode.jpg", quality=500)

    img = Image.open("images/list.jpg")
    watermark = Image.open("images/supply_barcode.jpg")
    img.paste(watermark, (650, 100))
    img.save("images/img_with_watermark.jpg")

    image = Image.open("images/img_with_watermark.jpg")
    font = ImageFont.truetype("font/arialmt.ttf", size=110)
    draw_text = ImageDraw.Draw(image)
    draw_text.text(
        (570, 720),
        f"Поставка {supply_id}",
        font=font,
        fill="#000000",
    )
    image.save("images/img_with_watermark.jpg")


def orders_beautyfier():
    pages = convert_from_path("images/order_stickers.pdf", 300)
    for i, page in enumerate(pages):
        page.save(f"images/stickers{i}.jpg", "JPEG")

    img = Image.open("images/list.jpg")
    lenght = 100
    width = 100
    k = 0
    for i in range(0, len(pages)):

        watermark = Image.open(f"images/stickers{i}.jpg")
        img.paste(watermark, (lenght + k * 500, width))
        k += 1
        if i != 0 and (i - 3) % 4 == 0:
            k = 0
            width += 400

    img.save("images/img_orders.jpg")


# if __name__ == '__main__':
    # message = {'orders': [{'userInfo': {'fio': '', 'email': '', 'phone': 0}, 'dateCreated': '2022-06-07T05:55:52.206988Z', 'orderUID': '9853398062268261_974de54b8f7e4f448d42bc43468f1995', 'officeAddress': 'г. Петропавловск-Камчатский (Камчатский край), ул. Лукашевского, 19', 'deliveryAddress': '', 'rid': '103902496811', 'orderId': '321189906', 'barcode': '2022751900000', 'barcodes': ['2022751900000'], 'scOfficesNames': [], 'deliveryAddressDetails': {'province': '', 'area': '', 'city': '', 'street': '', 'home': '', 'flat': '', 'entrance': '', 'longitude': 0, 'latitude': 0}, 'chrtId': 116811130, 'pid': 11337, 'wbWhId': 124100, 'userStatus': 4, 'storeId': 75851, 'totalPrice': 90100, 'convertedPrice': 90100, 'deliveryType': 1, 'currencyCode': 643, 'status': 0}, {'userInfo': {'fio': '', 'email': '', 'phone': 0}, 'dateCreated': '2022-06-07T05:55:52.206988Z', 'orderUID': '9853398062268261_974de54b8f7e4f448d42bc43468f1995', 'officeAddress': 'г. Петропавловск-Камчатский (Камчатский край), ул. Лукашевского, 19', 'deliveryAddress': '', 'rid': '103902496811', 'orderId': '321189906', 'barcode': '2022751900000', 'barcodes': ['2022751900000'], 'scOfficesNames': [], 'deliveryAddressDetails': {'province': '', 'area': '', 'city': '', 'street': '', 'home': '', 'flat': '', 'entrance': '', 'longitude': 0, 'latitude': 0}, 'chrtId': 116811130, 'pid': 11337, 'wbWhId': 124100, 'userStatus': 4, 'storeId': 75851, 'totalPrice': 90100, 'convertedPrice': 90100, 'deliveryType': 1, 'currencyCode': 643, 'status': 0}], 'total': 1}
    # print(beautiful_order_messages(message))
    # orders_beautyfier()
