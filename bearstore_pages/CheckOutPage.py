from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class CheckOutPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def enter_first_name(self, first_name):
        first_name_field = self.driver.find_element(By.ID, 'NewAddress_FirstName')
        first_name_field.clear()
        first_name_field.send_keys(first_name)

    def enter_last_name(self, last_name):
        last_name_field = self.driver.find_element(By.ID, 'NewAddress_LastName')
        last_name_field.clear()
        last_name_field.send_keys(last_name)

    def enter_billing_address(self,first_name,last_name):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)

    def next_button_billing_address_element(self):
        return self.driver.find_element(By.CLASS_NAME, 'select-billing-address-button')

    def ship_to_this_address_button_element(self):
        return self.driver.find_element(By.CLASS_NAME, 'select-shipping-address-button')

    def next_button_shipping_method_element(self):
        return self.driver.find_element(By.CLASS_NAME, 'shipping-method-next-step-button')

    def next_button_payment_method_element(self):
        return self.driver.find_element(By.CSS_SELECTOR, '.payment-method-next-step-button')

    def get_agreement_checkbox_element(self):
        return self.driver.find_element(By.ID,'termsofservice')

    def get_confirm_button_element(self):
        return self.driver.find_element(By.CLASS_NAME,'btn-danger')

    def get_confirmation_header_element(self):
        return self.driver.find_element(By.TAG_NAME,'h1')

    def get_order_details_button_element(self):
        return self.driver.find_element(By.CSS_SELECTOR,'.btn-warning')

    def get_order_number_element(self):
        return self.driver.find_element(By.CSS_SELECTOR,'p > a > strong')

    def new_address_next_element(self):
        return self.driver.find_element(By.CSS_SELECTOR,'.new-address-next-step-button')

