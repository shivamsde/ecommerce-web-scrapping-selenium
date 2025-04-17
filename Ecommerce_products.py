from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# Step 1: Setup Selenium and scroll to load all products
service = Service(r'C:\Users\Shivam SDE\OneDrive\Desktop\chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = 'https://www.ajio.com/s/deodrants-5260-44722'
driver.get(url)
time.sleep(3)

old_height = driver.execute_script('return document.body.scrollHeight')
counter = 1

while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(2)

    new_height = driver.execute_script('return document.body.scrollHeight')

    print(f"Scroll Count: {counter} | Height: {old_height} → {new_height}")
    counter += 1

    if new_height == old_height:
        break
    old_height = new_height

# Step 2: Get final HTML and close browser
html = driver.page_source
driver.quit()

# Optional: Save the file (already handled)
with open('ajio.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Step 3: Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
products = soup.find_all('div', class_='item rilrtl-products-list__item item')
print(f"\n Total products found: {len(products)}")

# Step 4: Extract details
data = []

for product in products:
    try:
        brand = product.find('div', class_='brand').text.strip()
        name = product.find('div', class_='nameCls').text.strip()

        rating = product.find('p', class_='_3I65V')
        rating = rating.text.strip() if rating else 'N/A'

        rating_count = product.find('p', attrs={"aria-label": lambda x: x and '|' in x})
        rating_count = rating_count.text.strip().replace('|', '').strip() if rating_count else 'N/A'

        discounted_price = product.find('span', class_='price')
        discounted_price = discounted_price.text.strip() if discounted_price else 'N/A'

        original_price = product.find('span', class_='orginal-price')
        original_price = original_price.text.strip() if original_price else 'N/A'

        discount = product.find('span', class_='discount')
        discount = discount.text.strip() if discount else 'N/A'

        offer_price = product.select_one('div.offer-div-new span.offer-pricess-new')
        offer_price = offer_price.text.strip() if offer_price else 'N/A'

        data.append({
            "Brand": brand,
            "Product Name": name,
            "Rating": rating,
            "No. of Ratings": rating_count,
            "Discounted Price": discounted_price,
            "Original Price": original_price,
            "Discount": discount,
            "Offer Price": offer_price
        })

    except Exception as e:
        print(f" Error extracting a product: {e}")
        continue

# Step 5: Save to CSV
df = pd.DataFrame(data)
df.to_csv("ajio_deodorants_full.csv", index=False)
print("\n CSV file 'ajio_deodorants_full.csv' created successfully!")
