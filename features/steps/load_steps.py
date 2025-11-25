"""
Load Steps for Product BDD Testing
"""
from behave import given
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@given('the following products')
def step_impl(context):
    """Load the database with product data from the table"""
    
    # Get the web driver
    driver = context.driver
    
    # Clear any existing data
    driver.get(context.base_url)
    driver.find_element(By.ID, "clear-btn").click()
    
    # Load each product from the table
    for row in context.table:
        # Navigate to the home page
        driver.get(context.base_url)
        
        # Fill in the product form
        driver.find_element(By.ID, "product_name").send_keys(row['name'])
        driver.find_element(By.ID, "product_description").send_keys(row['description'])
        driver.find_element(By.ID, "product_price").send_keys(row['price'])
        
        # Select category from dropdown
        category_select = Select(driver.find_element(By.ID, "product_category"))
        category_select.select_by_visible_text(row['category'])
        
        # Select availability from dropdown
        available_select = Select(driver.find_element(By.ID, "product_available"))
        available_select.select_by_visible_text(row['available'])
        
        # Click the Create button
        driver.find_element(By.ID, "create-btn").click()
        
        # Wait for success message
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
        )