

import os
import sys
import re
import json
from datetime import datetime

class ReceiptParser:
    def __init__(self):
        # Қазақстандық чектерге арналған regex үлгілері
        self.patterns = {
            # Баға үлгілері (1 200,00 немесе 308,00)
            'price': r'(\d{1,3}(?:\s\d{3})*|\d+)[.,](\d{2})\b',
            
            # Өнім жолын табу (1. Натрия хлорид...)
            'product_line': r'^(\d+)\.\s*(.+?)(?:\s+\d+[,.]\d{3}\s*x\s*)?$',
            
            # Саны мен бағасы бар жол (2,000 x 154,00)
            'quantity_price': r'(\d+)[,.]\d{3}\s*x\s*(\d{1,3}(?:\s\d{3})*[.,]\d{2})',
            
            # Жалпы сома
            'total': r'ИТОГО:\s*(\d{1,3}(?:\s\d{3})*[.,]\d{2})',
            
            # Төлем тәсілі
            'payment': r'(Банковская карта|Наличные|Карта|Cash|Card)',
            
            # Күн мен уақыт
            'datetime': r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})',
            
            # Дүкен атауы
            'store': r'Филиал\s+(.+)',
            
            # БИН
            'bin': r'БИН\s*(\d+)',
            
            # Чек нөмірі
            'receipt_no': r'Чек\s*№(\d+)',
        }
    
    def parse(self, filename):
        """Чекті өңдеу"""
        try:
            print(f"\n📂 Файл ашылуда: {filename}")
            print(f"📁 Ағымдағы папка: {os.getcwd()}")
            
            # Файлдың бар-жоғын тексеру
            if not os.path.exists(filename):
                print(f"❌ Қате: '{filename}' файлы табылмады!")
                print("\n📋 Ағымдағы папкадағы файлдар:")
                for file in os.listdir('.'):
                    print(f"   - {file}")
                return None
            
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()
            
            print(f"✅ Файл сәтті оқылды! Файл өлшемі: {len(text)} символ")
            
        except Exception as e:
            print(f"❌ Қате: {e}")
            return None
        
        print("🔍 Чекті өңдеу басталды...")
        
        # Барлық деректерді жинау
        products = self._extract_products(text)
        prices = self._extract_prices(text)
        total = self._extract_total(text)
        date_time = self._extract_datetime(text)
        payment = self._extract_payment(text)
        store_info = self._extract_store_info(text)
        
        # Бағалар саны мен өнімдер санын теңестіру
        if len(products) > len(prices):
            products = products[:len(prices)]
        elif len(prices) > len(products):
            prices = prices[:len(products)]
        
        # Нәтижені құрастыру
        result = {
            'store_name': store_info['name'],
            'bin': store_info['bin'],
            'receipt_number': store_info['receipt_no'],
            'datetime': {
                'date': date_time['date'],
                'time': date_time['time']
            },
            'payment_method': payment,
            'items': [],
            'total': total,
            'item_count': len(products),
            'total_calculated': sum(prices) if prices else 0
        }
        
        # Өнімдер мен бағаларды біріктіру
        for i in range(min(len(products), len(prices))):
            result['items'].append({
                'name': products[i],
                'price': prices[i]
            })
        
        # Тексеру: барлық бағалардың қосындысы жалпы сомаға тең бе?
        if result['total_calculated'] > 0:
            difference = abs(result['total_calculated'] - result['total'])
            result['total_match'] = difference < 1.0  # 1 теңгеге дейін айырмашылық болса да болады
            if result['total_match']:
                print("✅ Жалпы сома дұрыс есептелген")
            else:
                print(f"⚠️  Ескерту: Жалпы сома сәйкес келмейді (айырма: {difference:.2f} ₸)")
        
        print(f"✅ {len(products)} өнім табылды")
        return result
    
    def _extract_products(self, text):
        """Өнімдерді табу"""
        products = []
        lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Өнім нөмірі бар жолды табу (1., 2., т.б.)
            if re.match(r'^\d+\.$', line) and i + 1 < len(lines):
                # Келесі жолда өнім атауы бар
                product_line = lines[i + 1].strip()
                if product_line and not re.search(r'\d+[,.]\d{3}\s*x', product_line):
                    # Өнім атауын тазалау
                    product = re.sub(r'\s+', ' ', product_line)
                    products.append(product)
                    i += 2
                else:
                    i += 1
            elif re.match(r'^\d+\.\s+', line):
                # Бір жолда нөмірі мен атауы бар
                product = re.sub(r'^\d+\.\s+', '', line)
                product = re.sub(r'\s+\d+[,.]\d{3}\s*x.*$', '', product)
                product = re.sub(r'\s+', ' ', product).strip()
                if product and len(product) > 2:
                    products.append(product)
                i += 1
            else:
                i += 1
        
        return products
    
    def _extract_prices(self, text):
        """Бағаларды табу және санға айналдыру"""
        prices = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Өнім бағасы бар жолдарды табу (308,00 сияқты жеке тұрған бағалар)
            if re.match(r'^\d{1,3}(?:\s\d{3})*[.,]\d{2}$', line):
                price_str = line.replace(' ', '').replace(',', '.')
                try:
                    price = float(price_str)
                    if 1 <= price <= 1000000:
                        prices.append(price)
                except ValueError:
                    continue
            
            # Саны мен бағасы бар жол (2,000 x 154,00)
            elif 'x' in line:
                match = re.search(r'x\s*(\d{1,3}(?:\s\d{3})*[.,]\d{2})', line)
                if match:
                    price_str = match.group(1).replace(' ', '').replace(',', '.')
                    try:
                        price = float(price_str)
                        if 1 <= price <= 1000000:
                            prices.append(price)
                    except ValueError:
                        continue
        
        return prices
    
    def _extract_total(self, text):
        """Жалпы соманы табу"""
        # ИТОГО деген жолды іздеу
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'ИТОГО' in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if re.match(r'^\d{1,3}(?:\s\d{3})*[.,]\d{2}$', next_line):
                    total_str = next_line.replace(' ', '').replace(',', '.')
                    return float(total_str)
        
        # Немесе regex арқылы іздеу
        total_match = re.search(self.patterns['total'], text)
        if total_match:
            total_str = total_match.group(1).replace(' ', '').replace(',', '.')
            return float(total_str)
        
        return 0
    
    def _extract_datetime(self, text):
        """Күн мен уақытты табу"""
        datetime_match = re.search(self.patterns['datetime'], text)
        if datetime_match:
            return {
                'date': datetime_match.group(1),
                'time': datetime_match.group(2)
            }
        return {'date': None, 'time': None}
    
    def _extract_payment(self, text):
        """Төлем тәсілін табу"""
        payment_match = re.search(self.patterns['payment'], text)
        if payment_match:
            return payment_match.group(1)
        
        if 'Банковская карта' in text:
            return 'Банковская карта'
        return 'Анықталмаған'
    
    def _extract_store_info(self, text):
        """Дүкен ақпаратын табу"""
        store_match = re.search(self.patterns['store'], text)
        bin_match = re.search(self.patterns['bin'], text)
        receipt_match = re.search(self.patterns['receipt_no'], text)
        
        return {
            'name': store_match.group(1).strip() if store_match else 'Анықталмаған',
            'bin': bin_match.group(1) if bin_match else 'Анықталмаған',
            'receipt_no': receipt_match.group(1) if receipt_match else 'Анықталмаған'
        }
    
    def save_to_json(self, data, filename='output.json'):
        """JSON файлға сақтау"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=False)
            print(f"✅ JSON файл сақталды: {filename}")
            print(f"   Файл өлшемі: {os.path.getsize(filename)} байт")
            return True
        except Exception as e:
            print(f"❌ JSON файлды сақтау кезінде қате: {e}")
            return False
    
    def save_to_text(self, data, filename='output.txt'):
        """Мәтіндік файлға сақтау"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self._format_text_output(data))
            print(f"✅ Мәтіндік файл сақталды: {filename}")
            return True
        except Exception as e:
            print(f"❌ Мәтіндік файлды сақтау кезінде қате: {e}")
            return False
    
    def _format_text_output(self, data):
        """Мәтіндік форматта шығару"""
        lines = []
        lines.append("="*70)
        lines.append("ЧЕК ДЕРЕКТЕРІ / RECEIPT DATA")
        lines.append("="*70)
        
        lines.append(f"🏪 Дүкен / Store: {data['store_name']}")
        lines.append(f"🔢 БИН / BIN: {data['bin']}")
        lines.append(f"🧾 Чек № / Receipt No: {data['receipt_number']}")
        lines.append(f"📅 Күні / Date: {data['datetime']['date']}")
        lines.append(f"⏰ Уақыты / Time: {data['datetime']['time']}")
        lines.append(f"💳 Төлем / Payment: {data['payment_method']}")
        
        lines.append("\n" + "-"*70)
        lines.append("🛍️  САТЫП АЛЫНҒАН ӨНІМДЕР / PURCHASED ITEMS:")
        lines.append("-"*70)
        
        if data['items']:
            for i, item in enumerate(data['items'], 1):
                # Өнім атауын қысқарту (50 символға дейін)
                short_name = item['name'][:50] + '...' if len(item['name']) > 50 else item['name']
                lines.append(f"{i:2d}. {short_name:<50} {item['price']:>15,.2f} ₸")
        else:
            lines.append("   Өнімдер табылмады / No items found")
        
        lines.append("-"*70)
        lines.append(f"💰 Жалпы сома (чек бойынша): {data['total']:>43,.2f} ₸")
        lines.append(f"💰 Жалпы сома (есептелген):   {data['total_calculated']:>43,.2f} ₸")
        
        if 'total_match' in data:
            if data['total_match']:
                match_status = "✓ СӘЙКЕС КЕЛЕДІ / MATCHES"
            else:
                match_status = "✗ СӘЙКЕС КЕЛМЕЙДІ / DOES NOT MATCH"
            lines.append(f"📊 Тексеру / Validation: {match_status:>53}")
        
        lines.append("="*70)
        lines.append(f"📦 Өнім саны / Number of items: {data['item_count']}")
        lines.append("="*70)
        
        return "\n".join(lines)
    
    def print_result(self, data):
        """Нәтижені экранға шығару"""
        print(self._format_text_output(data))


# Негізгі программа
if __name__ == "__main__":
    print("="*70)
    print("ҚАЗАҚСТАНДЫҚ ЧЕК ПАРСЕРІ / KAZAKHSTAN RECEIPT PARSER")
    print("="*70)
    
    # Парсерді іске қосу
    parser = ReceiptParser()
    
    # Файл жолын анықтау
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"📌 Командалық жолдан файл алынды: {file_path}")
    else:
        # Ағымдағы папкада raw.txt бар ма?
        if os.path.exists('raw.txt'):
            file_path = 'raw.txt'
            print(f"📌 'raw.txt' файлы табылды")
        else:
            # Файл жолын сұрау
            file_path = input("📂 raw.txt файлының жолын көрсетіңіз (Enter бассаңыз, 'raw.txt' қолданылады): ").strip()
            if not file_path:
                file_path = 'raw.txt'
                print("📌 'raw.txt' файлы қолданылады")
    
    # Чекті өңдеу
    result = parser.parse(file_path)
    
    if result:
        print("\n" + "="*70)
        print("ӨҢДЕУ НӘТИЖЕСІ / PROCESSING RESULT")
        print("="*70)
        
        # Нәтижені көрсету
        parser.print_result(result)
        
        # Файлдарға сақтау
        print("\n" + "-"*70)
        print("ФАЙЛДАРҒА САҚТАУ / SAVING TO FILES")
        print("-"*70)
        
        json_saved = parser.save_to_json(result, 'output.json')
        text_saved = parser.save_to_text(result, 'output.txt')
        
        if json_saved and text_saved:
            print("\n" + "="*70)
            print("✅ БАРЛЫҚ ФАЙЛДАР СӘТТІ САҚТАЛДЫ!")
            print("="*70)
            print("\n📄 Шығарылған файлдар:")
            print("   - output.json  (JSON формат)")
            print("   - output.txt   (Мәтіндік формат)")
        else:
            print("\n⚠️  Кейбір файлдар сақталмады!")
    else:
        print("\n❌ Чекті өңдеу мүмкін болмады!")