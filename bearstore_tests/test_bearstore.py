from unittest import TestCase
from selenium import webdriver
from time import sleep

from bearstore_pages.CartPopUp import CartPopUp
from bearstore_pages.HomePage import HomePage
from bearstore_pages.CategoryPage import CategoryPage
from selenium.webdriver.common.by import By
from bearstore_pages.ProductPage import ProductPage
from bearstore_pages.ShoppingCartPage import ShoppingCartPage
from bearstore_tests.data_from_xlsx import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


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
        self.cart_pop_up = CartPopUp(self.driver)
        self.shopping_cart_page = ShoppingCartPage(self.driver)

    # Test 1
    def test_page_transition(self):
        category_name = read_data_from_xlsx(self.file_path,'K2')
        product_name = read_data_from_xlsx(self.file_path,'K4')
        home_page_title_excel = read_data_from_xlsx(self.file_path,'L23')

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

            cart_quantity_list = self.cart_pop_up.get_quantity_list()
            total_quantity = 0

            for quantity in cart_quantity_list:
                total_quantity += int(quantity.get_attribute("value"))

            # Test total quantity compare to excel data
            self.assertEqual(int(quantity_product1)+int(quantity_product2),total_quantity)

            # Wait until orange badge span updates
            WebDriverWait(self.driver, 5).until(
                lambda driver: int(self.cart_pop_up.get_total_quantity_badge_span()) == total_quantity)

            # Test total quantity compare to badge orange tag
            self.assertEqual(int(self.cart_pop_up.get_total_quantity_badge_span()), total_quantity)

            write_test_result_to_xlsx(self.file_path, "J19", "Pass")
            self.cart_pop_up.remove_all_products()

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
            product1_name = self.product_page.get_header_element().text

            self.product_page.change_quantity(quantity_product1)
            self.product_page.add_to_cart()
            self.home_page.return_to_home_page()
            self.home_page.click_on_category(category_name2)
            self.category_page.click_on_product(product_name2)

            product2_price = self.product_page.get_price()
            product2_name = self.product_page.get_header_element().text

            self.product_page.change_quantity(quantity_product2)
            self.product_page.add_to_cart()
            self.home_page.return_to_home_page()
            self.home_page.click_on_category(category_name3)
            self.category_page.click_on_product(product_name3)

            product3_price = self.product_page.get_price()
            product3_name = self.product_page.get_header_element().text

            self.product_page.change_quantity(quantity_product3)
            self.product_page.add_to_cart()

            product_names = [product1_name, product2_name, product3_name]
            product_prices = [product1_price, product2_price, product3_price]
            product_quantities = [int(quantity_product1), int(quantity_product2), int(quantity_product3)]

            cart_page_names = self.cart_pop_up.products_name_list_elements()
            cart_page_prices = self.cart_pop_up.price_list()
            cart_page_quantities = self.cart_pop_up.get_quantity_list_number()

            for i in range(3):  # Loop through product indices
                self.assertEqual(product_names[i], cart_page_names[2 - i].text)  # Reverse order for cart_page_names
                self.assertEqual(product_prices[i], cart_page_prices[2 - i])
                self.assertEqual(product_quantities[i], cart_page_quantities[2 - i])

            write_test_result_to_xlsx(self.file_path, "I19", "Pass")
            self.cart_pop_up.remove_all_products()

        except Exception as e:
            write_test_result_to_xlsx(self.file_path, "I19", f"Fail: {str(e)}")
            raise

    # Test 4
    def test_delete_one_product(self):
        category_name1 = read_data_from_xlsx(self.file_path, 'H2')
        product_name1 = read_data_from_xlsx(self.file_path, 'H4')

        category_name2 = read_data_from_xlsx(self.file_path, 'H7')
        product_name2 = read_data_from_xlsx(self.file_path, 'H9')

        try:
            self.home_page.click_on_category(category_name1)
            self.category_page.click_on_product(product_name1)

            product1_price = self.product_page.get_price()
            product1_name = self.product_page.get_header_element().text

            self.product_page.add_to_cart()
            self.home_page.return_to_home_page()
            self.home_page.click_on_category(category_name2)
            self.category_page.click_on_product(product_name2)
            self.product_page.add_to_cart()

            initial_count = len(self.cart_pop_up.products_name_list_elements())
            self.cart_pop_up.remove_product_by_index(0)

            # Wait for the length of the product list to decrease by one
            WebDriverWait(self.driver, 10).until(
                lambda driver: len(self.cart_pop_up.products_name_list_elements()) == initial_count - 1
            )
            self.assertEqual(product1_name, self.cart_pop_up.products_name_list_elements()[0].text)
            self.assertEqual(product1_price, self.cart_pop_up.price_list()[0])
            self.assertEqual(1, self.cart_pop_up.get_quantity_list_number()[0])

            write_test_result_to_xlsx(self.file_path, "H19", "Pass")
            self.cart_pop_up.remove_all_products()

        except Exception as e:
            write_test_result_to_xlsx(self.file_path, "H19", f"Fail: {str(e)}")
            raise

    # Test 5
    def test_cart_transition(self):
        category_name1 = read_data_from_xlsx(self.file_path, 'G2')
        product_name1 = read_data_from_xlsx(self.file_path, 'G4')
        shopping_cart_page_title = read_data_from_xlsx(self.file_path,'L22')

        try:
            self.home_page.click_on_category(category_name1)
            self.category_page.click_on_product(product_name1)
            self.product_page.add_to_cart()

            # Wait for the cart popup to be visible
            subtotal_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".offcanvas-cart-header"))
            )

            #5(A)
            self.assertTrue(subtotal_element.is_displayed())

            # Click outside the cart to close it
            self.driver.find_element(By.CSS_SELECTOR, '.canvas-blocker').click()

            # Wait until the cart popup disappears
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".offcanvas-cart-header"))
            )

            # Verify that the cart is no longer visible (5B)
            self.assertFalse(self.cart_pop_up.is_cart_visible())

            self.home_page.get_shopping_cart_element().click()

            # Verify that the cart is visible (5C)
            self.assertTrue(self.cart_pop_up.is_cart_visible())

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn-success"))
            )
            self.cart_pop_up.go_to_cart_element().click()

            #(5D)
            self.assertEqual(shopping_cart_page_title,self.shopping_cart_page.get_header_element().text)

            write_test_result_to_xlsx(self.file_path, "G19", "Pass")
            self.cart_pop_up.remove_all_products()

        except Exception as e:
            write_test_result_to_xlsx(self.file_path, "G19", f"Fail: {str(e)}")
            raise

    # Test 6
    def test_total_cart_amount(self):
        category_name1 = read_data_from_xlsx(self.file_path, 'F2')
        product_name1 = read_data_from_xlsx(self.file_path, 'F4')
        quantity_product1 = read_data_from_xlsx(self.file_path, 'F6')

        category_name2 = read_data_from_xlsx(self.file_path, 'F7')
        product_name2 = read_data_from_xlsx(self.file_path, 'F9')
        quantity_product2 = read_data_from_xlsx(self.file_path, 'F10')

        category_name3 = read_data_from_xlsx(self.file_path, 'F11')
        product_name3 = read_data_from_xlsx(self.file_path, 'F13')
        quantity_product3 = read_data_from_xlsx(self.file_path, 'F14')

        try:
            self.home_page.click_on_category(category_name1)
            self.category_page.click_on_product(product_name1)
            product1_price = self.product_page.get_price()
            self.product_page.change_quantity(quantity_product1)
            self.product_page.add_to_cart()
            self.home_page.return_to_home_page()
            self.home_page.click_on_category(category_name2)
            self.category_page.click_on_product(product_name2)
            product2_price = self.product_page.get_price()
            self.product_page.change_quantity(quantity_product2)
            self.product_page.add_to_cart()
            self.home_page.return_to_home_page()
            self.home_page.click_on_category(category_name3)
            self.category_page.click_on_product(product_name3)

            product3_price = self.product_page.get_price()
            self.product_page.change_quantity(quantity_product3)
            self.product_page.add_to_cart()
            cart_pop_up_total_price = self.cart_pop_up.get_total_amount_price()
            total_price = ((product1_price * int(quantity_product1)) + (product2_price * int(quantity_product2))
                           + (product3_price * int(quantity_product3)))
            self.assertEqual(cart_pop_up_total_price,total_price)

            self.cart_pop_up.go_to_cart_element().click()
            cart_total_price = self.shopping_cart_page.get_total_amount_price()
            self.assertEqual(cart_total_price, total_price)
            write_test_result_to_xlsx(self.file_path, "F19", "Pass")
            logging.basicConfig(level=logging.INFO)
            logging.info(f' product1 name: {product_name1}')
            logging.info(f' product2 name: {product_name2}')
            logging.info(f' product3 name: {product_name3}')
            logging.info(f' product1 price: {product1_price}')
            logging.info(f' product2 price: {product2_price}')
            logging.info(f' product3 price: {product3_price}')
            logging.info(f' product1 quantity: {quantity_product1}')
            logging.info(f' product1 quantity: {quantity_product2}')
            logging.info(f' product1 quantity: {quantity_product3}')

            self.cart_pop_up.remove_all_products()

        except Exception as e:
            write_test_result_to_xlsx(self.file_path, "F19", f"Fail: {str(e)}")
            raise

    # Test 7
    def test_cart_page_updates(self):
        category_name1 = read_data_from_xlsx(self.file_path, 'E2')
        product_name1 = read_data_from_xlsx(self.file_path, 'E4')
        quantity_product1 = read_data_from_xlsx(self.file_path, 'E6')

        category_name2 = read_data_from_xlsx(self.file_path, 'E7')
        product_name2 = read_data_from_xlsx(self.file_path, 'E9')
        quantity_product2 = read_data_from_xlsx(self.file_path, 'E10')
        quantity_list = [quantity_product2, quantity_product1]

        try:
            self.home_page.click_on_category(category_name1)
            self.category_page.click_on_product(product_name1)
            self.product_page.add_to_cart()
            self.home_page.return_to_home_page()
            self.home_page.click_on_category(category_name2)
            self.category_page.click_on_product(product_name2)
            self.product_page.add_to_cart()
            self.cart_pop_up.go_to_cart_element().click()

            # Change quantities and wait for the updates
            self.shopping_cart_page.change_quantities(quantity_list)

            # Fetch updated unit prices from the cart
            unit_price_list = self.shopping_cart_page.get_unit_price_list()[::-1]

            # Calculate expected prices using the updated unit prices
            expected_price1 = unit_price_list[0] * float(quantity_product1)
            expected_price2 = unit_price_list[1] * float(quantity_product2)

            # Verify the updated total prices
            total_products_price_list = self.shopping_cart_page.get_total_products_price_list()[::-1]

            self.assertAlmostEqual(total_products_price_list[0], expected_price1)
            self.assertAlmostEqual(total_products_price_list[1], expected_price2)

            # Verify the subtotal
            sub_total = (float(self.shopping_cart_page.get_total_products_price_list()[0]) +
                         float(self.shopping_cart_page.get_total_products_price_list()[1]))

            self.assertEqual(self.shopping_cart_page.get_sub_total_price(), sub_total)

            self.home_page.return_to_home_page()
            self.home_page.get_shopping_cart_element().click()
            self.assertEqual(self.cart_pop_up.get_total_amount_price(),sub_total)

            write_test_result_to_xlsx(self.file_path, "E19", "Pass")

            # Clean up: Remove all products from the cart
            self.cart_pop_up.remove_all_products()

        except Exception as e:
            write_test_result_to_xlsx(self.file_path, "E19", f"Fail: {str(e)}")
            raise

    # Test 8
    #def test_


    def tearDown(self):
        sleep(2)
        self.driver.quit()




