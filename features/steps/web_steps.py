"""
Web Steps for BDD Testing
"""
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


######################################################################
# BUTTON CLICK STEP
######################################################################
@when('I press the "{button}" button')
def step_impl(context, button):
    """Click a button by its ID"""
    button_id = button.lower().replace(" ", "-") + "-btn"
    context.driver.find_element(By.ID, button_id).click()


######################################################################
# VERIFY TEXT IS PRESENT
######################################################################
@then('I should see "{text}" in the results')
def step_impl(context, text):
    """Check if text is present in the search results table"""
    element = context.driver.find_element(By.ID, "search_results")
    assert text in element.text, f"Expected '{text}' to be in results but it was not found"


######################################################################
# VERIFY TEXT IS NOT PRESENT
######################################################################
@then('I should not see "{text}" in the results')
def step_impl(context, text):
    """Check if text is NOT present in the search results table"""
    element = context.driver.find_element(By.ID, "search_results")
    assert text not in element.text, f"Expected '{text}' NOT to be in results but it was found"


######################################################################
# VERIFY MESSAGE IS PRESENT
######################################################################
@then('I should see the message "{message}"')
def step_impl(context, message):
    """Check if a specific message appears in the flash message area"""
    element = context.driver.find_element(By.ID, "flash_message")
    assert message in element.text, f"Expected message '{message}' but got '{element.text}'"


######################################################################
# ADDITIONAL HELPER STEPS
######################################################################

@when('I visit the "{page}" page')
def step_impl(context, page):
    """Navigate to a specific page"""
    context.driver.get(context.base_url)


@when('I set the "{field_name}" to "{value}"')
def step_impl(context, field_name, value):
    """Set a field value"""
    field_id = "product_" + field_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, field_id)
    element.clear()
    element.send_keys(value)


@when('I select "{value}" in the "{field_name}" dropdown')
def step_impl(context, value, field_name):
    """Select a value from a dropdown"""
    field_id = "product_" + field_name.lower().replace(" ", "_")
    select = Select(context.driver.find_element(By.ID, field_id))
    select.select_by_visible_text(value)


@when('I copy the "{field_name}" field')
def step_impl(context, field_name):
    """Copy a field value to clipboard (store in context)"""
    field_id = "product_" + field_name.lower()
    element = context.driver.find_element(By.ID, field_id)
    context.clipboard = element.get_attribute('value')


@when('I paste the "{field_name}" field')
def step_impl(context, field_name):
    """Paste a previously copied value"""
    field_id = "product_" + field_name.lower()
    element = context.driver.find_element(By.ID, field_id)
    element.clear()
    element.send_keys(context.clipboard)


@when('I change "{field_name}" to "{value}"')
def step_impl(context, field_name, value):
    """Change a field to a new value"""
    field_id = "product_" + field_name.lower()
    element = context.driver.find_element(By.ID, field_id)
    element.clear()
    element.send_keys(value)


@then('I should see "{text}" in the title')
def step_impl(context, text):
    """Check if text is in the page title"""
    assert text in context.driver.title


@then('I should not see "{text}"')
def step_impl(context, text):
    """Check if text is not present on the page"""
    page_text = context.driver.find_element(By.TAG_NAME, 'body').text
    assert text not in page_text


@then('I should see "{value}" in the "{field_name}" field')
def step_impl(context, value, field_name):
    """Check if a field contains a specific value"""
    field_id = "product_" + field_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, field_id)
    assert element.get_attribute('value') == value


@then('I should see "{value}" in the "{field_name}" dropdown')
def step_impl(context, value, field_name):
    """Check if a dropdown has a specific value selected"""
    field_id = "product_" + field_name.lower().replace(" ", "_")
    select = Select(context.driver.find_element(By.ID, field_id))
    assert select.first_selected_option.text == value