from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import sys, os, csv, re, time

confirm = raw_input("Type YES to continue: ")
if(confirm != "YES"):
    sys.exit()

driver = webdriver.Firefox()
base_url = "http://1000pitches.com"
data_path = "data/video_pitch_data.csv"
video_dir = os.getcwd() + "/data/videos"

file = open(data_path, "rU")
reader = csv.reader(file)

item = ["", # FIRST_NAME
        "", # LAST_NAME
        "", # USC_EMAIL
        "", # COLLEGE_NAME
        "", # GRADUATION_YEAR
        "", # PITCH_TITLE
        "", # PITCH_CATEGORY
        ""] # PITCH_DESCRIPTION

for row in reader:
    i = 0
    print ">>>>> PITCH NUMBER " + str(i) + " <<<<<"
    for col in row:
        item[i] = col
        print (item[i])
        i += 1
    item[i-1] = re.sub("[\n]", "", item[i-1])
    password = item[0].lower() + "." + item[1].lower()

    driver.get(base_url + "/")
    assert "1000 Pitches" in driver.title
    driver.find_element_by_link_text("Pitch Your Idea").click()
    Select(driver.find_element_by_id("edit-university")).select_by_visible_text("University of Southern California")
    driver.find_element_by_id("edit-first-name").clear()
    driver.find_element_by_id("edit-first-name").send_keys(item[0])
    driver.find_element_by_id("edit-last-name").clear()
    driver.find_element_by_id("edit-last-name").send_keys(item[1])
    driver.find_element_by_id("appendedInput").clear()
    driver.find_element_by_id("appendedInput").send_keys(item[2][:-8])
    driver.find_element_by_id("edit-umid").clear()
    driver.find_element_by_id("edit-umid").send_keys(password)
    # TODO: ensure colleges in Google Sheets match options
    Select(driver.find_element_by_id("edit-college")).select_by_visible_text(item[3])
    Select(driver.find_element_by_id("edit-grad-year")).select_by_visible_text(item[4])
    if(driver.find_element_by_id("edit-newsletter").is_selected()):
        driver.find_element_by_id("edit-newsletter").click()
    driver.find_element_by_id("edit-continue").click()
    if(len(driver.find_elements_by_class_name("error")) > 0):
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("edit-name").clear()
        driver.find_element_by_id("edit-name").send_keys(item[2])
        driver.find_element_by_id("edit-pass").clear()
        driver.find_element_by_id("edit-pass").send_keys(password)
        driver.find_element_by_id("edit-submit").click()
        driver.find_element_by_link_text("Pitch Your Idea").click()
    driver.find_element_by_id("edit-title").clear()
    driver.find_element_by_id("edit-title").send_keys(item[5])
    Select(driver.find_element_by_id("edit-category")).select_by_visible_text(item[6])
    driver.find_element_by_id("edit-description").clear()
    driver.find_element_by_id("edit-description").send_keys(item[7])
    driver.find_element_by_id("edit-continue").click()
    driver.find_element_by_css_selector("*[data-selector='upload-video']").click()
    driver.find_element_by_css_selector('input[type="file"]').clear()
    driver.find_element_by_css_selector('input[type="file"]').send_keys(video_dir + "/" + item[0].lower() + "_" + item[1].lower() + ".mov")
    while(len(driver.find_elements_by_class_name("btn-default")) == 0):
        time.sleep(2)
    driver.find_element_by_id("edit-continue").click()
    driver.find_element_by_id("edit-submit").click()
    driver.find_element_by_link_text("Logout").click()

driver.close()
