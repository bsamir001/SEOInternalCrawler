import json
from collections import Counter

# تابع برای بارگذاری داده‌ها از فایل JSON
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# تابع برای ذخیره داده‌ها در فایل
def save_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

# پردازش دسته اول
def process_category_one(data):
    result = []
    for keyword, items in data.items():
        if len(items) >= 4:
            # شمارش تعداد تکرار target_urls
            target_urls_count = Counter()
            for item in items:
                target_urls_count.update(item['target_urls'])
            
            # چک کردن تعداد انواع مختلف target_urls
            if len(target_urls_count) > 10:
                continue  # اگر تعداد انواع target_urls بیشتر از 10 بود، ادامه بده

            # شناسایی target_urls صحیح (با بیشترین تکرار)
            majority_target_url = target_urls_count.most_common(1)[0][0]
            # جدا کردن target_urls های غلط
            wrong_target_urls = [url for url, count in target_urls_count.items() if url != majority_target_url]

            for wrong_url in wrong_target_urls:
                result.append(f"{keyword} : {wrong_url}")
    
    return result

# پردازش دسته دوم
def process_category_two(data):
    result = []
    for keyword, items in data.items():
        if len(items) < 4:
            target_urls_set = set()  # برای جلوگیری از ذخیره تکراری‌ها
            for item in items:
                target_urls_set.update(item['target_urls'])
            
            for url in target_urls_set:
                result.append(f"{keyword} : {url}")
    
    return result

# اصلی‌ترین کد اسکریپت
def main():
    # بارگذاری داده‌ها از فایل a.json
    data = load_data('a.json')
    
    # پردازش دسته اول و دسته دوم
    category_one_result = process_category_one(data)
    category_two_result = process_category_two(data)
    
    # ذخیره‌سازی نتایج در فایل‌ها
    save_to_file('b.txt', '\n'.join(category_one_result))
    save_to_file('c.txt', '\n'.join(category_two_result))

    print("عملیات با موفقیت انجام شد!")

# اجرای اسکریپت
if __name__ == "__main__":
    main()
