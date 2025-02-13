from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class HomePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def categories_list(self):
        """Returns all <a> tags within the category div."""
        return self.driver.find_elements(By.CSS_SELECTOR, ".artlist-homepage-categories a span")


    def click_on_category(self, category_name):
        """ Clicks on the category with the given name. """
        for category in self.categories_list():
            if category.text.strip() == category_name:
                category.click()
                return

    def return_to_home_page(self):
        self.driver.find_element(By.CSS_SELECTOR,'.brand').click()

    def get_header_element(self):
        return self.driver.find_element(By.CSS_SELECTOR,'.h2')

    def get_shopping_cart_element(self):
        return self.driver.find_element(By.CSS_SELECTOR,'#shopbar-cart > a')