from unittest import TestCase
from selenium import webdriver
from time import sleep
from bearstore_pages.HomePage import HomePage
from bearstore_pages.ProductPage import ProductPage
from selenium.webdriver.common.by import By
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
        self.product_page = ProductPage(self.driver)

    def test_page_transition(self):
        file_path = r"C:\Users\nachala\Desktop\test_data.xlsx"
        category_name = read_category_from_xlsx(file_path)
        product_name = read_product_from_xlsx(file_path)
        home_page_title_excel = read_home_page_title_from_xlsx(file_path)

        # First Test (Category)
        category_test_name_passed = True  # Flag to track if category test passed
        # Second Test (Product)
        product_test_name_passed = True  # Flag to track if category test passed
        # Third Test (Previous page - Category Page Display)
        previous_category_page_display = True  # Flag to track if category test passed
        #Four Test (Previous page - Home Page)
        previous_homepage_page_display = True

        try:
            # Use HomePage class to select the category
            self.home_page.selected_category(category_name)

            # Verify that the page header matches the selected category
            header_element = self.driver.find_element(By.CSS_SELECTOR, ".h3")
            self.assertEqual(category_name.lower(), header_element.text.strip().lower())

            # Write "Pass" to cell B1 if the test passes

            write_test_result_to_xlsx(file_path, "B1", "Pass")

        except Exception as e:
            # Write "Fail" to cell B1 if the test fails
            write_test_result_to_xlsx(file_path, "B1", f"Fail: {str(e)}")
            category_test_name_passed = False  # Mark the test as failed

    #--------------------------------------1B----------------------------------------------------------

        # Second Test (Product) - Run this regardless of the first test result
        try:
            # Use ProductPage class to select the product
            self.product_page.selected_product(product_name)

            # Verify that the page header matches the selected product
            header_element = self.driver.find_element(By.CSS_SELECTOR, '.pd-name')
            self.assertEqual(product_name.lower(), header_element.text.strip().lower())

            # Write "Pass" to cell B2 if the test passes
            write_test_result_to_xlsx(file_path, "B2", "Pass")

        except Exception as e:
            # Write "Fail" to cell B2 if the test fails
            write_test_result_to_xlsx(file_path, "B2", f"Fail: {str(e)}")
            product_test_name_passed = False

    #--------------------------------------1C-------------------------------------------------------------

        try:
            self.driver.back()
            # wait until previous page loads
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            header_element = self.driver.find_element(By.CSS_SELECTOR, ".h3")
            self.assertEqual(category_name.lower(), header_element.text.strip().lower())
            write_test_result_to_xlsx(file_path, "B3", "Pass")

        except Exception as e:
            # Write "Fail" to cell B3 if the test fails
            write_test_result_to_xlsx(file_path, "B3", f"Fail: {str(e)}")
            previous_category_page_display = False

        # --------------------------------------1D-------------------------------------------------------------
        try:
            self.driver.back()
            # wait until previous page loads
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            home_page_title = self.driver.find_element(By.CSS_SELECTOR,'.h2')
            self.assertEqual(home_page_title_excel.lower(), home_page_title.text.strip().lower())
            write_test_result_to_xlsx(file_path, "B4", "Pass")

        except Exception as e:
            # Write "Fail" to cell B4 if the test fails
            write_test_result_to_xlsx(file_path, "B4", f"Fail: {str(e)}")
            previous_homepage_page_display = False

        # Fails report
        fail_report = ''
        if not category_test_name_passed:
            fail_report = 'Category Name Test Failed (1A)\n'
        if not product_test_name_passed:
            fail_report = f'{fail_report} Product Name Test Failed (1B)\n'
        if not previous_category_page_display:
            fail_report = f'{fail_report} Previous category page Test Failed (1C)\n'
        if not previous_homepage_page_display:
            fail_report = f'{fail_report} Previous Home Page Test Failed (1D)\n'

        if fail_report != '':
            self.fail(f'{fail_report}')

    def tearDown(self):
        sleep(2)
        self.driver.quit()
