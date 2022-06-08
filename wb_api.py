import json
import requests
import time
import datetime
from rfc3339 import rfc3339
import base64

# from config import wb_api


class WbApi:
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {"Authorization": access_token}

    def _time_(self, day, month, year):
        if int(day) < 10 and int(month) > 9:
            s = f"0{day}/{month}/{year}"
        elif int(day) > 9 and int(month) < 10:
            s = f"{day}/0{month}/{year}"
        elif int(day) < 10 and int(month) < 10:
            s = f"0{day}/0{month}/{year}"
        else:
            s = f"{day}/{month}/{year}"
        unix_time = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
        return unix_time

    def active_supplies(self):
        supplies = requests.get(
            "https://suppliers-api.wildberries.ru/api/v2/supplies?status=ACTIVE",
            headers=self.headers,
        )

        return supplies.json()

    def on_delivery_supplies(self):
        supplies = requests.get(
            "https://suppliers-api.wildberries.ru/api/v2/supplies?status=ON_DELIVERY",
            headers=self.headers,
        )
        return supplies.json()

    def new_supply(self):
        supply = requests.post(
            "https://suppliers-api.wildberries.ru/api/v2/supplies", 
            headers=self.headers
        )
        return supply.json()

    def put_orders_in_supply(self, supply_id, orders_list):
        self.data = {"orders": orders_list}
        request = requests.put(
            f"https://suppliers-api.wildberries.ru/api/v2/supplies/{supply_id}",
            headers=self.headers,
            data=self.data,
        )
        try:
            return request.json()
        except json.decoder.JSONDecodeError:
            return 0

    def close_supply(self, supply_id):
        request = requests.post(
            f"https://suppliers-api.wildberries.ru/api/v2/supplies/{supply_id}/close",
            headers=self.headers,
        )
        return request.json()

    def supply_barcode(self, supply_id):
        request = requests.get(
            f"https://suppliers-api.wildberries.ru/api/v2/supplies/{supply_id}/barcode?type=pdf",
            headers=self.headers,
        )
        with open("images/supply_barcode.pdf", "wb") as f:
            pdf = request.json()["file"]
            f.write(base64.b64decode(pdf))
        return "Barcode: supply_barcode.pdf"

    def supply_orders(self, supply_id):
        request = requests.get(
            f"https://suppliers-api.wildberries.ru/api/v2/supplies/{supply_id}/orders",
            headers=self.headers,
        )
        return request.json()

    def stocks(self, skip=0, take=100, sort="name", order="asc"):
        request = requests.get(
            f"https://suppliers-api.wildberries.ru/api/v2/stocks?skip={skip}&take={take}&sort={sort}&order={order}",
            headers=self.headers,
        )
        return request.json()

    def update_stocks(
        self,
        barcode,
        stock,
        warehouse,
    ):
        self.update_data = [
            {"barcode": barcode, "stock": stock, "warehouseId": warehouse}
        ]
        request = requests.post(
            "https://suppliers-api.wildberries.ru/api/v2/stocks",
            headers=self.headers,
            data=self.update_data,
        )
        return request.json()

    def delete_stocks(self, barcode, warehouse):
        self.delete_data = [{"barcode": barcode, "warehouseId": warehouse}]
        request = requests.delete(
            "https://suppliers-api.wildberries.ru/api/v2/stocks",
            headers=self.headers,
            data=self.delete_data,
        )
        return request.json()

    def warehouses(self):
        request = requests.get(
            f"https://suppliers-api.wildberries.ru/api/v2/warehouses",
            headers=self.headers,
        )
        return request.json()

    def get_orders(
        self,
        date_start=[1, 2, 2022],
        date_end=rfc3339(time.time()),
        status=2,
        take=10,
        skip=0, 
                ):
        self.date_start = rfc3339(
            self._time_(date_start[0], date_start[1], date_start[2])
        )  # date_start передается списком [день, месяц, год] пример [4, 7, 2022]
        if date_end[:9] == rfc3339(time.time())[:9]:
            self.date_end = date_end
        else:
            self.date_end = rfc3339(self._time_(date_end[0], date_end[1], date_end[2]))
        request = requests.get(
            f"https://suppliers-api.wildberries.ru/api/v2/orders?date_start={self.date_start[:11]}00%3A00%3A00-07%3A00&date_end={self.date_end[:11]}00%3A00%3A00-07%3A00&status={status}&take={take}&skip={skip}",
            headers=self.headers,
        )
        return request.json()

    def set_order_status(self, order_id, status):
        self.headers = {
            "Authorization": self.access_token,
            "Content-type": "application/json",
            "accept": "*/*",
        }
        order_data = [{"orderId": f"{order_id}", "status": status}]
        order_data = json.dumps(order_data)
        request = requests.put(
            "https://suppliers-api.wildberries.ru/api/v2/orders",
            headers=self.headers,
            data=order_data,
        )
        return request.json()

    def order_stickers(
        self, order_list
    ):  # возвращает список стикеров в статусе 1 и выше
        data = {"orderIds": order_list, "type": "code128"}  # например[8423848, 6436344]

        request = requests.post(
            "https://suppliers-api.wildberries.ru/api/v2/orders/stickers",
            headers=self.headers,
            data=data,
        )
        return request.json()

    def order_stickers_pdf(
        self, order_list
    ):  # возвращает список стикеров в статусе 1 и выше
        data = {"orderIds": order_list, "type": "code128"}
        request = requests.post(
            "https://suppliers-api.wildberries.ru/api/v2/orders/stickers/pdf",
            headers=self.headers,
            data=data,
        )
        with open("images/order_stickers.pdf", "wb") as f:
            pdf = request.json()["data"]["file"]
            f.write(base64.b64decode(pdf))
        return "Stickers: order_stickers.pdf"

    def set_new_orders_status1(self):
        orders = WbApi.get_orders(self, status=0)["orders"]
        order_list = []
        for i in range(0, len(orders)):
            order_list.append(orders[i]["orderId"])
        if order_list:
            try:
                for order in order_list:
                    print(self.set_order_status(order, status=1))
                return True
            except Exception:
                return False
        else:
            return "Нет новых заказов"

    def get_order_list_status1(self):
        orders = self.get_orders(status=1)["orders"]
        ord_list = []
        for el in orders:
            ord_list.append(el["orderId"])
        return ord_list


# if __name__ == '__main__':
    # wb = WbApi(wb_api)
    # print(wb.order_stickers_pdf([321613700, 321189906, 321166917, 321118118, 315737132, 314252478, 314252469, 313446249, 313423622]))
