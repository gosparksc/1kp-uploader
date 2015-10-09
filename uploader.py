from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import sys, os, csv, re, time

# TODO: integrate HandBrake CLI for video compression (https://handbrake.fr/downloads2.php)

def account_create(item):
    driver.find_element_by_link_text("Pitch Your Idea").click()
    Select(driver.find_element_by_id("edit-university")).select_by_visible_text("University of Southern California")
    driver.find_element_by_id("edit-first-name").clear()
    driver.find_element_by_id("edit-first-name").send_keys(item[0])
    driver.find_element_by_id("edit-last-name").clear()
    driver.find_element_by_id("edit-last-name").send_keys(item[1])
    driver.find_element_by_id("appendedInput").clear()
    driver.find_element_by_id("appendedInput").send_keys(item[2][:-8])
    driver.find_element_by_id("edit-umid").clear()
    driver.find_element_by_id("edit-umid").send_keys(password[0])
    Select(driver.find_element_by_id("edit-college")).select_by_visible_text(item[3])
    Select(driver.find_element_by_id("edit-grad-year")).select_by_visible_text(item[4])
    if(driver.find_element_by_id("edit-newsletter").is_selected()):
        driver.find_element_by_id("edit-newsletter").click()
    driver.find_element_by_id("edit-continue").click()

def account_login(item, pwd):
    driver.find_element_by_link_text("Login").click()
    driver.find_element_by_id("edit-name").clear()
    driver.find_element_by_id("edit-name").send_keys(item[2])
    driver.find_element_by_id("edit-pass").clear()
    driver.find_element_by_id("edit-pass").send_keys(pwd)
    driver.find_element_by_id("edit-submit").click()

def pitch_add(item):
    driver.find_element_by_link_text("Pitch Your Idea").click()
    driver.find_element_by_id("edit-title").clear()
    driver.find_element_by_id("edit-title").send_keys(item[5])
    Select(driver.find_element_by_id("edit-category")).select_by_visible_text(item[6])
    driver.find_element_by_id("edit-description").clear()
    driver.find_element_by_id("edit-description").send_keys(item[7])
    driver.find_element_by_id("edit-continue").click()
    driver.find_element_by_css_selector("*[data-selector='upload-video']").click()
    driver.find_element_by_css_selector('input[type="file"]').clear()
    # TODO: remove spaces from names (for example, "Doo Hyun Nam"). don't remove special characters ("-")
    driver.find_element_by_css_selector('input[type="file"]').send_keys(video_dir + "/" + item[0].lower() + "_" + item[1].lower() + ".mp4")
    while(len(driver.find_elements_by_class_name("btn-default")) == 0):
        time.sleep(2)

confirm = raw_input("Type YES to continue: ")
if(confirm != "YES"):
    sys.exit()

driver = webdriver.Firefox()
base_url = "http://1000pitches.com"
data_path = "data/video_pitch_data.csv"
video_dir = os.getcwd() + "/data/videos"

file = open(data_path, "rU")
reader = csv.reader(file)

item = ["", # 0 FIRST_NAME
        "", # 1 LAST_NAME
        "", # 2 USC_EMAIL
        "", # 3 COLLEGE_NAME
        "", # 4 GRADUATION_YEAR
        "", # 5 PITCH_TITLE
        "", # 6 PITCH_CATEGORY
        ""] # 7 PITCH_DESCRIPTION

for row in reader:
    i = 0
    print ">>>>> PITCH NUMBER " + str(i) + " <<<<<"

    for col in row:
        item[i] = col

        # special cases
        if(i == 3 and col == "Unknown"):
            item[i] = "Letters, Arts and Sciences"
        if(i == 3 and col == "Dramatic Arts"):
            item[i] = "Letters, Arts and Sciences"
        if(i == 3 and col == "Arts, Technology, Business"):
            item[i] = "Business"
        if(i == 6 and col == "University Improvements"):
            item[i] = "U-Provements"
        if(i == 6 and col == "Mobile"):
            item[i] = "Mobile Apps"
        if(i == 7 and col == ""):
            item[i] = item[5]

        print (item[i])

        i += 1

    item[i-1] = re.sub("[\n]", "", item[i-1])

    password = [item[0].lower() + "." + item[1].lower(),
            item[0],
            item[0].lower()]

    # start automation
    driver.get(base_url + "/")
    assert "1000 Pitches" in driver.title

    account_create(item)

    # if account already exists
    j = 0
    while(len(driver.find_elements_by_class_name("error")) > 0):
        if(j >= len(password)):
            # TODO: handle case where alternative email exists in system, but all passwords are incorrect
            item[2] = "1kp2015" + item[2]
            print "UNABLE TO LOGIN. Trying alternative " + item[2] + "."
            account_create(item)
            j = 0
        else:
            account_login(item, password[j])
            j += 1

    pitch_add(item)

    driver.find_element_by_id("edit-continue").click()
    driver.find_element_by_id("edit-submit").click()

    # check that pitch was submitted successfully
    form_contents = driver.find_element_by_id("pitch-form").text
    assert "Your pitch has been submitted" in form_contents

    driver.find_element_by_link_text("Logout").click()

driver.close()
