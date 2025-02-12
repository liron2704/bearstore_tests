from unittest import TestCase
from selenium import webdriver
from time import sleep

from bearstore_pages.CartPage import CartPage
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
        
        self.file_path = r"C:\Users\nachala\Desktop\test_data.xlsx"
        self.home_page = HomePage(self.driver)
        self.category_page = CategoryPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)

    # Test 1
    def test_page_transition(self):
        category_name = read_data_from_xlsx(self.file_path,'K2')
        product_name = read_data_from_xlsx(self.file_path,'K4')
        home_page_title_excel = read_data_from_xlsx(self.file_path,'K5')

        try:
            # Use HomePage class to select the category
            self.home_page.click_on_category(category_name)

            # Verify that the page header matches the selected category
            header_element = self.category_page.get_header_element()
            self.assertEqual(category_name.lower(), header_element.text.strip().lower())

        except Exception as e:
            # Write "Fail" to cell B1 if the test fails
            write_test_result_to_xlsx(self.file_path, "K19", f"Fail: {str(e)}")
            raise  # Mark the test as failed

    #--------------------------------------1B----------------------------------------------------------

        # Second Test (Product) - Run this regardless of the first test result
        try:
            # Use ProductPage class to select the product
            self.category_page.click_on_product(product_name)

            # Verify that the page header matches the selected product
            header_element = self.product_page.get_header_element()
            self.assertEqual(product_name.lower(), header_element.text.strip().lower())

        except Exception as e:
            # Write "Fail" to cell B2 if the test fails
            write_test_result_to_xlsx(self.file_path, "K19", f"Fail: {str(e)}")
            raise

    #--------------------------------------1C-------------------------------------------------------------

        try:
            self.driver.back()
            # wait until previous page loads
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            header_element = self.category_page.get_header_element()
            self.assertEqual(category_name.lower(), header_element.text.strip().lower())

        except Exception as e:
            # Write "Fail" to cell B3 if the test fails
            write_test_result_to_xlsx(self.file_path, "K19", f"Fail: {str(e)}")
            raise


        # --------------------------------------1D-------------------------------------------------------------
        try:
            self.driver.back()
            # wait until previous page loads
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            home_page_title = self.home_page.get_header_element()
            self.assertEqual(home_page_title_excel.lower(), home_page_title.text.strip().lower())
            write_test_result_to_xlsx(self.file_path, "K19", "Pass")

        except Exception as e:
            # Write "Fail" to cell B4 if the test fails
            write_test_result_to_xlsx(self.file_path, "K19", f"Fail: {str(e)}")
            raise

    # Test 2
    def test_quantity_on_cart(self):
        category_name1 = read_data_from_xlsx(self.file_path,'J2')
        product_name1 = read_data_from_xlsx(self.file_path,'J4')
        quantity_product1 = read_data_from_xlsx(self.file_path,'J6')

        category_name2 = read_data_from_xlsx(self.file_path,'J7')
        product_name2 = read_data_from_xlsx(self.file_path,'J9')
        quantity_product2 = read_data_from_xlsx(self.file_path,'J10')

        
        try:
            self.home_page.click_on_category(category_name1)
            self.category_page.click_on_product(product_name1)
            self.product_page.change_quantity(quantity_product1)
            self.product_page.add_to_cart()
            self.home_page.return_to_home_page()
            self.home_page.click_on_category(category_name2)
            self.category_page.click_on_product(product_name2)
            self.product_page.change_quantity(quantity_product2)
            self.product_page.add_to_cart()

            cart_quantity_list = self.cart_page.get_quantity_list()
            total_quantity = 0

            for quantity in cart_quantity_list:
                total_quantity += int(quantity.get_attribute("value"))

            # Test total quantity compare to excel data
            self.assertEqual(int(quantity_product1)+int(quantity_product2),total_quantity)

            # Wait until orange badge span updates
            WebDriverWait(self.driver, 5).until(
                lambda driver: int(self.cart_page.get_total_quantity_badge_span()) == total_quantity)

            # Test total quantity compare to badge orange tag
            self.assertEqual(int(self.cart_page.get_total_quantity_badge_span()),total_quantity)

            write_test_result_to_xlsx(self.file_path, "J19", "Pass")
            self.cart_page.remove_all_products()

        except Exception as e:
            write_test_result_to_xlsx(self.file_path, "J19", f"Fail: {str(e)}")
            raise

    # Test 3
    def test_correct_product_details(self):
        category_name1 = read_data_from_xlsx(self.file_path, 'I2')
        product_name1 = read_data_from_xlsx(self.file_path, 'I4')
        quantity_product1 = read_data_from_xlsx(self.file_path, 'I6')

        category_name2 = read_data_from_xlsx(self.file_path, 'I7')
        product_name2 = read_data_from_xlsx(self.file_path, 'I9')
        quantity_product2 = read_data_from_xlsx(self.file_path, 'I10')

        category_name3 = read_data_from_xlsx(self.file_path, 'I11')
        product_name3 = read_data_from_xlsx(self.file_path, 'I13')
        quantity_product3 = read_data_from_xlsx(self.file_path, 'I14')

        try:
            self.home_page.click_on_category(category_name1)
            self.category_page.click_on_product(product_name1)

            product1_price = self.product_page.get_price()
            product1_name = self.product_page.get_header_element()

            self.product_page.change_quantity(quantity_product1)
            self.product_page.add_to_cart()
            self.home_page.return_to_home_page()
            self.home_page.click_on_category(category_name2)
            self.category_page.click_on_product(product_name2)

            product2_price = self.product_page.get_price()
            product2_name = self.product_page.get_header_element()

            self.product_page.change_quantity(quantity_product2)
            self.product_page.add_to_cart()
            self.home_page.return_to_home_page()
            self.home_page.click_on_category(category_name3)
            self.category_page.click_on_product(product_name3)

            product3_price = self.product_page.get_price()
            product3_name = self.product_page.get_header_element()

            self.product_page.change_quantity(quantity_product3)
            self.product_page.add_to_cart()




        except Exception as e:
            write_test_result_to_xlsx(self.file_path, "I19", f"Fail: {str(e)}")
            raise



    def tearDown(self):
        sleep(4)
        self.driver.quit()




