from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPopUp:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_quantity_list(self):
        return self.driver.find_elements(By.XPATH,"//div[@class='offcanvas-cart-item']//input[@name='item.EnteredQuantity']")

    def get_quantity_list_number(self):
        """ Returns the total amount of products in the basket """
        quantities = self.driver.find_elements(By.XPATH,"//div[@class='offcanvas-cart-item']//input[@name='item.EnteredQuantity']")
        quantity_list = []
        for quantity in quantities:
            quantity_list.append(int(quantity.get_attribute("value")))
        return quantity_list

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

    def remove_product_by_index(self,index):
        delete_button_list = self.driver.find_elements(By.CSS_SELECTOR, '.btn-to-danger')
        if index >= len(delete_button_list) or index < 0:  # Check for valid index
            raise IndexError(f"Index {index} is out of range. Available products: {len(delete_button_list)}")
        delete_button_list[index].click() # Remove the selected product

    def products_name_list_elements(self):
        return self.driver.find_elements(By.CSS_SELECTOR,'.col-data >a')

    def price_list(self):
        price_elements_list = self.driver.find_elements(By.CSS_SELECTOR,'.unit-price')
        price_list = []
        for price_element in price_elements_list:
            price_strip = price_element.text.strip()
            price = ''.join(char for char in price_strip if char.isdigit() or char == '.')
            price_list.append(float(price))
        return price_list

    def is_cart_visible(self):
        """Helper function to check if the cart subtotal element is visible."""
        try:
            return WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".offcanvas-cart-header"))
            )
        except:
            return False

    def go_to_cart_element(self):
        return self.driver.find_element(By.CSS_SELECTOR,'.btn-success')

    def get_total_amount_price(self):
        price_strip = self.driver.find_element(By.CSS_SELECTOR, '.sub-total').text.strip()
        price_str = ''.join(char for char in price_strip if char.isdigit() or char == '.')
        price = float(price_str)
        return price