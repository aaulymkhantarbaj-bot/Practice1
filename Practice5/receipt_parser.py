import re
import json

with open("/Users/makbuk/Documents/hello_world/practice1/Practice5/raw.txt","r", encoding="utf-8") as file:
    text = file.read()

# ----------------------------
# 1. Извлекаем товары
# ----------------------------
# Товар находится между номером позиции и строкой количества
product_pattern = r"\d+\.\n(.+?)\n\d+,\d+\s+x"
products = re.findall(product_pattern, text, re.DOTALL)

# Очищаем переносы строк внутри длинных названий
products = [p.replace("\n", " ").strip() for p in products]

# ----------------------------
# 2. Извлекаем суммы товаров (последняя строка перед "Стоимость")
# ----------------------------
price_pattern = r"\n([\d\s]+,\d{2})\nСтоимость"
prices_raw = re.findall(price_pattern, text)

# Убираем пробелы из чисел
prices = [float(p.replace(" ", "").replace(",", ".")) for p in prices_raw]

# ----------------------------
# 3. Общая сумма
# ----------------------------
total_calculated = round(sum(prices), 2)

# Сумма из строки "ИТОГО"
total_pattern = r"ИТОГО:\n([\d\s]+,\d{2})"
total_match = re.search(total_pattern, text)

total_receipt = None
if total_match:
    total_receipt = float(total_match.group(1).replace(" ", "").replace(",", "."))

# ----------------------------
# 4. Дата и время
# ----------------------------
datetime_pattern = r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})"
datetime_match = re.search(datetime_pattern, text)

date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None

# ----------------------------
# 5. Метод оплаты
# ----------------------------
payment_pattern = r"(Банковская карта|Наличные)"
payment_match = re.search(payment_pattern, text)

payment_method = payment_match.group(1) if payment_match else None

# ----------------------------
# 6. Формируем структуру
# ----------------------------
data = {
    "products": products,
    "prices": prices,
    "total_calculated": total_calculated,
    "total_receipt": total_receipt,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(data, indent=4, ensure_ascii=False))