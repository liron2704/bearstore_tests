from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class RegisterPage:
    def __init__(self , driver : webdriver.Chrome):
        self.driver = driver

    def enter_first_name(self, first_name):
        first_name_field = self.driver.find_element(By.ID, 'FirstName')
        first_name_field.clear()
        first_name_field.send_keys(first_name)

    def enter_last_name(self, last_name):
        last_name_field = self.driver.find_element(By.ID, 'LastName')
        last_name_field.clear()
        last_name_field.send_keys(last_name)

    def select_birth_date(self, day, month, year):
        day_dropdown = Select(self.driver.find_element(By.ID, "DateOfBirthDay"))
        day_dropdown.select_by_value(day)
        month_dropdown = Select(self.driver.find_element(By.ID, "DateOfBirthMonth"))
        month_dropdown.select_by_visible_text(month)
        year_dropdown = Select(self.driver.find_element(By.ID, "DateOfBirthYear"))
        year_dropdown.select_by_value(year)

    def enter_email(self, email):
        email_field = self.driver.find_element(By.ID, 'Email')
        email_field.clear()
        email_field.send_keys(email)

    def enter_username(self, user_name):
        user_name_field = self.driver.find_element(By.ID, 'Username')
        user_name_field.clear()
        user_name_field.send_keys(user_name)

    def enter_password(self, password):
        password_field = self.driver.find_element(By.ID, 'Password')
        password_field.clear()
        password_field.send_keys(password)

        confirm_password_field = self.driver.find_element(By.ID, "ConfirmPassword")
        confirm_password_field.clear()
        confirm_password_field.send_keys(password)

    def enter_details(self,first_name, last_name, day, month, year, email, user_name, password):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.select_birth_date(day,month,year)
        self.enter_email(email)
        self.enter_username(user_name)
        self.enter_password(password)

    def get_register_button_element(self):
        return self.driver.find_element(By.CLASS_NAME , 'btn-lg')

    def get_continue_element(self):
        return self.driver.find_element(By.CSS_SELECTOR,'.register-continue-button')




    def continue_button_element(self):
        return self.driver.find_element(By.CLASS_NAME , 'btn-secondary')