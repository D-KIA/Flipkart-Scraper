# ................................................Flipkart Scraper..................................................

from selenium import webdriver
from selenium.webdriver.common.by import By
from csv import writer

# Class for Flipkart Scraping
class flipkart:
    # Constants
    base_url = 'https://www.flipkart.com'
    driver = webdriver.Chrome()
    page_no = 1

    def __init__(self, search, pages=1):
        self.search = search
        self.pages = pages

    # Make new CSV
    def new_csv(self):
        f = open('search_output.csv', 'w', encoding='utf8')  ## opening file in write mode
        thewriter = writer(f)
        headers = ['Name', 'Rating', 'Price', 'Link']  ## Adding Headers
        thewriter.writerow(headers)

    # Add to existing CSV
    def add_csv(self):
        f = open('search_output.csv', 'a', encoding='utf8')  ## opening file in write mode
        thewriter = writer(f)
        thewriter.writerow(self.content)

    # Searching for content
    def searching(self):
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(7)
        self.driver.find_element(By.CSS_SELECTOR, 'button[class="_2KpZ6l _2doB4z"]').click()

        search_bar = self.driver.find_element(By.CSS_SELECTOR, 'input[title="Search for products, brands and more"]')
        search_bar.send_keys(self.search)
        self.driver.find_element(By.CSS_SELECTOR, 'button[class="L0Z3Pu"]').click()

    # Scrapes the required content
    def scraper(self):
        self.new_csv()
        self.searching()

        while self.page_no <= self.pages:
            product = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="_4ddWXP"]')

            for i in range(0, len(product)):
                    try:
                        name = product[i].find_element(By.CSS_SELECTOR, 'a[class="s1Q9rs"]').get_attribute('title')
                    except:
                        name = None
                    try:
                        rating = float(product[i].find_element(By.CSS_SELECTOR, 'div[class="_3LWZlK"]').text)
                    except:
                        rating = None

                    try:
                        price = int(product[i].find_element(By.CSS_SELECTOR, 'div[class="_30jeq3"]').text[1:].replace(',', ''))
                    except:
                        price = None

                    try:
                        link = product[i].find_element(By.CSS_SELECTOR, 'a[class="s1Q9rs"]').get_attribute('href')
                    except:
                        link = None

                    self.content = [name, rating, price, link]

                    self.add_csv()
            try:
                next_page = self.driver.find_elements(By.CSS_SELECTOR, 'a[class="_1LKTO3"]')[-1].get_attribute('href')
                self.driver.get(next_page)
                self.page_no += 1
            except:
                print('last page reached')
                break

def get_info():
    search = input('What do you want to search: ')
    pages = int(input('How many pages do you want to scrape: '))
    print('Working....')
    test = flipkart(search, pages)
    test.scraper()
    print('Done')

# Main
get_info()

