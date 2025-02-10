from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class HomePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def categories_list(self):
        """Returns all <a> tags within the category div."""
        return self.driver.find_elements(By.CSS_SELECTOR, ".artlist-homepage-categories a span")


    def selected_category(self, category_name):
        """ Clicks on the category with the given name. """
        for category in self.categories_list():
            if category.text.strip() == category_name:
                category.click()
                return
