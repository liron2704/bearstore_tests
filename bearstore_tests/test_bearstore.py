from unittest import TestCase
from selenium import webdriver
from time import sleep
from bearstore_pages.HomePage import HomePage
from bearstore_pages.CategoryPage import CategoryPage
from selenium.webdriver.common.by import By
from bearstore_pages.ProductPage import ProductPage
from bearstore_tests.data_from_xlsx import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestPageTransitions(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://bearstore-testsite.smartbear.com/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.home_page = HomePage(self.driver)
        self.category_page = CategoryPage(self.driver)
        self.product_page = ProductPage(self.driver)

    def test_page_transition(self):
        file_path = r"C:\Users\nachala\Desktop\test_data.xlsx"
        category_name = read_data_from_xlsx(file_path,'K2')
        product_name = read_data_from_xlsx(file_path,'K4')
        home_page_title_excel = read_data_from_xlsx(file_path,'K5')

        try:
            # Use HomePage class to select the category
            self.home_page.selected_category(category_name)

            # Verify that the page header matches the selected category
            header_element = self.category_page.get_header_element()
            self.assertEqual(category_name.lower(), header_element.text.strip().lower())

            # Write "Pass" to cell B1 if the test passes

            write_test_result_to_xlsx(file_path, "K19", "Pass")

        except Exception as e:
            # Write "Fail" to cell B1 if the test fails
            write_test_result_to_xlsx(file_path, "K19", f"Fail: {str(e)}")
            raise  # Mark the test as failed

    #--------------------------------------1B----------------------------------------------------------

        # Second Test (Product) - Run this regardless of the first test result
        try:
            # Use ProductPage class to select the product
            self.category_page.selected_product(product_name)

            # Verify that the page header matches the selected product
            header_element = self.product_page.get_header_element()
            self.assertEqual(product_name.lower(), header_element.text.strip().lower())

            # Write "Pass" to cell B2 if the test passes
            write_test_result_to_xlsx(file_path, "K19", "Pass")

        except Exception as e:
            # Write "Fail" to cell B2 if the test fails
            write_test_result_to_xlsx(file_path, "K19", f"Fail: {str(e)}")
            raise

    #--------------------------------------1C-------------------------------------------------------------

        try:
            self.driver.back()
            # wait until previous page loads
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            header_element = self.category_page.get_header_element()
            self.assertEqual(category_name.lower(), header_element.text.strip().lower())
            write_test_result_to_xlsx(file_path, "K19", "Pass")

        except Exception as e:
            # Write "Fail" to cell B3 if the test fails
            write_test_result_to_xlsx(file_path, "K19", f"Fail: {str(e)}")
            raise


        # --------------------------------------1D-------------------------------------------------------------
        try:
            self.driver.back()
            # wait until previous page loads
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            home_page_title = self.home_page.get_header_element()
            self.assertEqual(home_page_title_excel.lower(), home_page_title.text.strip().lower())
            write_test_result_to_xlsx(file_path, "K19", "Pass")

        except Exception as e:
            # Write "Fail" to cell B4 if the test fails
            write_test_result_to_xlsx(file_path, "K19", f"Fail: {str(e)}")
            raise

    def test_quantity_on_cart(self):
        pass

    def tearDown(self):
        sleep(2)
        self.driver.quit()




