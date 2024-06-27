#!/usr/bin/python3
import random
import time
from datetime import date, datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond

USR = "..."
PWD = "..."

# Instantiate webdriver
# chromedriver executable needs to be in a directory specified in PATH (e.g. /usr/local/bin/)
# Alternative: pass absolute path to chromedriver on your local machine
driver = webdriver.Chrome('/usr/local/bin/chromedriver')
wait = WebDriverWait(driver, 10)
driver.get("https://www.sport.ed.ac.uk/online-booking/")

##############################################
############# Global variables ###############
##############################################

class_to_book = "Lane Swimming"
days_in_advance = 3

##############################################
############# Helper functions ###############
##############################################

# Used to simulate random behaviour
def randomisedTimeout(exact_timeout):
    time.sleep(random.uniform(exact_timeout, exact_timeout + 1.5))

##############################################
############ Essential functions #############
##############################################

def log_into_system():
    driver.find_element_by_xpath("//a[@href='/online-booking/Account/LogOn']").click()
    usernameField = driver.find_element_by_xpath("//input[@id='UserName']")
    usernameField.send_keys(USR)
    passwordField = driver.find_element_by_xpath("//input[@id='Password']")
    passwordField.send_keys(PWD)
    driver.find_element_by_xpath("//input[@value='Log on']").click()

def search_for_class(activity):
    driver.find_element_by_xpath("//input[@id='searchForClass']").click()

    dropdownEl = wait.until(cond.visibility_of_element_located((By.XPATH, "//select[@id='SiteID']")))
    dropdown = Select(dropdownEl)
    dropdown.select_by_visible_text("Pleasance Sports Centre")

    activity_dropdown_el = wait.until(cond.visibility_of_element_located((By.XPATH, "//select[@id='Activity']")))

    activity_dropdown = Select(activity_dropdown_el)
    activity_dropdown.select_by_visible_text(activity)
    select_date(days_in_advance)
    perform_search()

def select_date(date_num):
    dateEl = wait.until(cond.visibility_of_element_located((By.XPATH, "//input[@id='SearchDate']")))
    dateStr = dateEl.get_attribute("value")

    start_date = datetime.strptime(dateStr, "%m/%d/%Y")
    select_date = start_date + timedelta(days=date_num)

    dateEl.clear()
    randomisedTimeout(2)
    dateEl.send_keys(select_date.strftime("%m/%d/%Y"))
    randomisedTimeout(2)
    dateEl.send_keys(Keys.RETURN);
    randomisedTimeout(4)

def perform_search():
    searchEl = driver.find_element_by_xpath("//input[@class='NavigationButton']")
    randomisedTimeout(2)
    searchEl.send_keys(Keys.NULL)
    randomisedTimeout(2)
    searchEl.click()
    randomisedTimeout(2)

def bookEvents(resultIDs):
    for ID in resultIDs:
        randomisedTimeout(4)
        try:
            driver.find_element_by_xpath("//a[@href='/online-booking/Search/AddEnrolmentToBasket?SiteNo=1&ResultId=%d']" %ID).click()
            driver.execute_script("window.history.go(-1)")
        except:
            print(f"%dth session not available.", ID)

def add_events_to_basket():
    events = driver.find_elements_by_xpath("//a[starts-with(@href,'/online-booking/Search/AddEnrolmentToBasket?SiteNo=1&ResultId=')]")

    # Usually always 3 to select from except sunday, then only 1
    if len(events) == 1:
        bookEvents([1])
    else:
        if len(events) == 3:
            # Skip morning swim
            bookEvents([2,3])
        else:
            # Unexpected number of swims, just book all of them
            bookEvents(range(1,len(events) + 1))

def finish_booking():
    driver.find_element_by_xpath("//a[@href='/online-booking/Basket/ViewDetail']").click()

    randomisedTimeout(5)

    driver.find_element_by_xpath("//input[@id='TermsAccepted']").click()

    terms_and_conditions = driver.find_element_by_xpath("//input[@id='CheckoutSubmit']")
    terms_and_conditions.send_keys(Keys.NULL)
    terms_and_conditions.click()

    randomisedTimeout(5)

    driver.find_element_by_xpath("//a[@href='/online-booking-payment/Response/FoC']").click()

def print_log_messages():
    print("##################################################################################")
    print("#                                                                                #")
    print("#                                                                                #")
    print(f"#                 Booking process from {date.today()}                            #")
    print("#                                                                                #")
    print("#                                                                                #")
    print("##################################################################################")

def print_status_messages():
    print(f"Trying to book class '{class_to_book}', {days_in_advance} days in advance.")
    print("Booking did not throw any errors. May have been successful.")

##############################################
############## Execute script ################
##############################################

print_log_messages()
log_into_system()
search_for_class(class_to_book)
add_events_to_basket()
finish_booking()
print_status_messages()

driver.quit()
