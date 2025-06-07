import asyncio
import aiohttp
import json

# فایل JSON برای ذخیره نتایج
output_file = "d.json"

# خواندن داده‌ها از a.json
def read_json():
    with open('a.json', 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

# تابع بررسی وضعیت URL
async def check_url_status(session, url):
    try:
        async with session.get(url, timeout=30) as response:
            status = response.status
            return status
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# بررسی همه URLها و ذخیره نتایج
async def process_urls():
    data = read_json()  # خواندن داده‌ها از فایل a.json
    results = {}  # برای ذخیره نتایج

    async with aiohttp.ClientSession() as session:
        tasks = []  # لیست وظایف همزمان

        # حلقه برای بررسی URLهای مختلف
        for key, value in data.items():
            target_url = value[0]['target_urls'][0]  # انتخاب تنها یکی از URLها (همه URLها یکسان هستند)
            tasks.append(check_url_status(session, target_url))  # اضافه کردن درخواست به لیست

        # انجام درخواست‌ها به صورت همزمان و گرفتن نتایج
        status_codes = await asyncio.gather(*tasks)  # در اینجا همه درخواست‌ها همزمان اجرا می‌شوند

        # پردازش نتایج
        for idx, (key, value) in enumerate(data.items()):
            target_url = value[0]['target_urls'][0]
            status_code = status_codes[idx]
            
            if status_code and status_code != 200:  # اگر وضعیت غیر از 200 بود
                if target_url not in results:
                    results[target_url] = {
                        "status": status_code,
                        "urls": [value[0]['url']]
                    }
                else:
                    results[target_url]["urls"].append(value[0]['url'])

    # ذخیره نتایج در فایل JSON
    save_to_json(results)

# ذخیره نتایج به فایل d.json
def save_to_json(data):
    with open(output_file, 'w', encoding='utf-8') as jsonf:
        json.dump(data, jsonf, indent=4, ensure_ascii=False)

# اجرای برنامه
if __name__ == "__main__":
    asyncio.run(process_urls())
