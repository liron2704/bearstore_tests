from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_quantity_list(self):
        return self.driver.find_elements(By.XPATH,"//div[@class='offcanvas-cart-item']//input[@name='item.EnteredQuantity']")

    def get_total_quantity_badge_span(self):
        return self.driver.find_element(By.CSS_SELECTOR,'#cart-tab > span.badge').text

    def remove_all_products(self):
        delete_button_list = self.driver.find_elements(By.CSS_SELECTOR, '.btn-to-danger')

        if not delete_button_list:  # Base case: stop if no buttons are found
            return

        delete_button_list[0].click()  # Remove the first product
        WebDriverWait(self.driver, 5).until(EC.staleness_of(delete_button_list[0]))  # Wait until it's removed
        # Recursive call to remove the next product with the updated list
        self.remove_all_products()

    def products_name_list(self):
        return self.driver.find_elements(By.CSS_SELECTOR,'col-data')
