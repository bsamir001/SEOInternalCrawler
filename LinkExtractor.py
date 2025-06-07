import os
import re
import xml.etree.ElementTree as ET

def extract_https_links_from_files(directory):
    # الگوی جستجو برای پیدا کردن لینک‌های HTTPS
    https_pattern = r'https://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,6}(:[0-9]{1,5})?(/[\w\-\./?%&=]*)?'

    # لیستی برای ذخیره لینک‌ها
    links = []

    # مرور تمام فایل‌های XML در دایرکتوری
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory, filename)
            try:
                # پردازش فایل XML
                tree = ET.parse(file_path)
                root = tree.getroot()

                # جستجو در تمام تگ‌ها برای پیدا کردن لینک‌ها
                for elem in root.iter():
                    if elem.text:
                        found_links = re.findall(https_pattern, elem.text)
                        for link in found_links:
                            links.append(link)

            except Exception as e:
                print(f"خطا در پردازش فایل {filename}: {e}")

    # حذف تکراری‌ها
    unique_links = list(set(links))

    # اضافه کردن https://asarayan.com به هر لینک و جایگزینی ')' و '' و '()' ها
    updated_links = []
    for link in unique_links:
        updated_link = f"https://asarayan.com{link}"
        # جایگزینی ')' و '('', ' با فضای خالی
        updated_link = updated_link.replace("('', '", " ").replace("') ", " ").replace(" ", "").replace("')", "")
        
        # بررسی برای حذف لینک‌هایی که به jpg، png یا webp ختم می‌شوند
        if updated_link.endswith(('jpg', 'png', 'webp', 'JPG', 'PNG', 'WEBP')):
            continue  # این لینک را حذف می‌کنیم
        
        updated_links.append(updated_link)

    # نوشتن لینک‌ها در فایل a.txt
    with open(os.path.join(directory, 'a.txt'), 'w') as file:
        for link in updated_links:
            file.write(link + '\n')
    
    return updated_links

# استفاده از اسکریپت
directory = os.path.dirname(os.path.realpath(__file__))  # استفاده از دایرکتوری فعلی اسکریپت
links = extract_https_links_from_files(directory)

# چاپ لینک‌های استخراج‌شده
for link in links:
    print(link)
