import openpyxl

def write_test_result_to_xlsx(file_path, cell, result):
    """Writes the test result (e.g., 'Pass' or 'Fail') to the specified cell in the xlsx file."""
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    sheet[cell] = result  # Write the test result to the specified cell
    workbook.save(file_path)  # Save the changes
    workbook.close()

def read_data_from_xlsx(file_path,cell):
    """Reads the category name from the specified xlsx file."""
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    data = sheet[cell].value.strip()  # Ensure it removes extra spaces in the Excel file
    workbook.close()
    return data


# def read_product_from_xlsx(file_path):
#     workbook = openpyxl.load_workbook(file_path)
#     sheet = workbook.active
#     product_name = sheet["A2"].value.strip()  # Ensure it removes extra spaces in the Excel file
#     workbook.close()
#     return product_name
#
# def read_home_page_title_from_xlsx(file_path):
#     workbook = openpyxl.load_workbook(file_path)
#     sheet = workbook.active
#     home_page_title = sheet["A4"].value.strip()  # Ensure it removes extra spaces in the Excel file
#     workbook.close()
#     return home_page_title

