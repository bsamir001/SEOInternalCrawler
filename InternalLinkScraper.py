import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

json_file = "a.json"

# خواندن لینک‌ها از فایل a.txt
def read_urls_from_file():
    with open('a.txt', 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

# دریافت لینک‌های داخلی از صفحه
async def get_internal_links(session, url):
    internal_links = []
    try:
        # ارسال درخواست به صفحه با تایم‌اوت بیشتر (۳۰ ثانیه)
        async with session.get(url, timeout=30) as response:
            response.raise_for_status()  # اگر صفحه باز نشد خطا می‌دهد

            # پردازش HTML
            soup = BeautifulSoup(await response.text(), 'html.parser')

            # پیدا کردن تمام تگ‌های <a>
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']

                # استخراج متن تگ <a>
                link_text = a_tag.get_text(strip=True)

                # بررسی لینک‌ها و ذخیره کردن فقط لینک‌های داخلی
                if href.startswith('/'):  # لینک‌های داخلی معمولاً با "/" شروع می‌شوند
                    full_url = urljoin(url, href)  # استفاده از urljoin برای افزودن دامنه اصلی به لینک داخلی
                elif href.startswith(url):  # لینک‌هایی که دامنه مشابه دارند
                    full_url = href
                else:
                    continue

                # ذخیره لینک‌ها و متن تگ <a> به عنوان کلید
                internal_links.append((full_url, link_text))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    
    return internal_links

# ذخیره کردن داده‌ها در فایل JSON
def save_to_json(data):
    with open(json_file, 'w', encoding='utf-8') as jsonf:
        # اضافه کردن ensure_ascii=False برای ذخیره‌سازی کاراکترهای فارسی
        json.dump(data, jsonf, indent=4, ensure_ascii=False)

# به‌روزرسانی داده‌ها و ذخیره‌سازی فایل JSON
def update_json(keyword, url, target_urls, data):
    if keyword == "":  # اگر keyword خالی بود، از ذخیره‌سازی جلوگیری می‌کنیم
        return

    if keyword not in data:
        data[keyword] = []

    data[keyword].append({
        "url": url,
        "target_urls": target_urls
    })

    # ذخیره فایل JSON پس از هر بار به‌روزرسانی
    save_to_json(data)

# پردازش و استخراج لینک‌های داخلی
async def process_urls():
    urls = read_urls_from_file()
    data = {}  # برای ذخیره داده‌ها

    # ساخت یک لیست از درخواست‌های همزمان
    async with aiohttp.ClientSession() as session:
        tasks = []  # لیست وظایف همزمان
        for url in urls:
            tasks.append(get_internal_links(session, url))  # اضافه کردن هر درخواست به لیست tasks

        # انجام همه درخواست‌ها به صورت همزمان و گرفتن نتایج
        results = await asyncio.gather(*tasks)

        # پردازش نتایج به دست آمده
        for i, (url, internal_links) in enumerate(zip(urls, results), start=1):
            print(f"Processing {i}/{len(urls)}: {url}")
            for link, link_text in internal_links:
                keyword = link_text  # به جای استفاده از URL، متن تگ را به عنوان keyword ذخیره می‌کنیم
                update_json(keyword, url, [link], data)

            # ذخیره‌سازی داده‌ها بعد از هر بار پردازش URL
            save_to_json(data)
            print(f"Link {i}/{len(urls)}: {url}")

# اجرای برنامه به صورت همزمان
if __name__ == "__main__":
    asyncio.run(process_urls())
