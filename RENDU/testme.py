from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
import unittest, time
import credentials


class Testone2team(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('/RENDU/chromedriver')
        self.driver.implicitly_wait(30)
        self.base_url = "https://chewie.one2team.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_one2team(self):
        driver = self.driver
        driver.get(self.base_url)
        self.driver.implicitly_wait(10)

        #1. Login Page
        driver.find_element_by_id("userName").clear()
        driver.find_element_by_id("userName").send_keys(credentials.login['username'])
        driver.find_element_by_id("passWord").clear()
        driver.find_element_by_id("passWord").send_keys(credentials.login['password'])
        driver.find_element_by_id("domainName").clear()
        driver.find_element_by_id("domainName").send_keys(credentials.login['domain'])
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        time.sleep(10)
        if driver.current_url == self.base_url and driver.title == "chewie.one2team.com/telco":
            print("Login Successful Passed")
        else:
            print("Login Unsuccessful Failed")
            self.driver.close()
        time.sleep(10)

        #2.Go to Slideboard and select Zz_Taches Project
        driver.get(credentials.login['slideboard'])
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select2-chosen-2")))
        driver.find_element_by_id("select2-chosen-2").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "select2-result-label-7")))
        driver.find_element_by_id("select2-result-label-7").click()
        time.sleep(10)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "menu")))

        #3. Creation of a card named test
        driver.find_element_by_xpath("//div[@id='columns-container']/div/div[3]/div/div[2]/div/span/span").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "cardName")))
        driver.find_element_by_id("cardName").clear()
        driver.find_element_by_id("cardName").send_keys("test")
        driver.find_element_by_css_selector("div.btn-label.ng-binding").click()
        if driver.find_element_by_xpath("//*[@id='toast-container']/div"):
            print("Card named test is created")
        else:
            print("No Card was created")

        #4.Drag and Drop the new card
        source_element = driver.find_element_by_xpath("//*[@id='/ogp/5993618']/div/div[4]")
        dest_element = driver.find_element_by_xpath("//*[@id='/ogp/5741508']/div/div[4]")
        ActionChains(driver).drag_and_drop(source_element, dest_element).perform()
        print("Drag and drop Done")


        #5.Open the card and Upload a document on it
        driver.find_element_by_xpath("//div[@id='/ogp/2180144']/div/div[4]").click()
        time.sleep(10)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//div[@id='card-popin-back-content-current']/div/div[2]/card-modal-collapse-column-dumb/div/div/card-modal-block-dumb[2]/div/div/div/span")))
        driver.find_element_by_xpath("//div[@id='card-popin-back-content-current']/div/div[2]/card-modal-collapse-column-dumb/div/div/card-modal-block-dumb[2]/div/div/div/span").click()
        time.sleep(10)
        driver.find_element_by_link_text("+").click()
        driver.find_element_by_id("add-file-document_18").send_keys("/RENDU/images.png")
        driver.find_element_by_xpath("//div[@id='card-popin-back-content-current']/div/div/div/div[4]/span").click()
        print("Card uploaded")


        # Deconnexion
        time.sleep(10)
        driver.find_element_by_css_selector("div.user-avatar").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='right-buttons']/user-profile/span/div")))
        driver.find_element_by_xpath("//*[@id='right-buttons']/user-profile/span/ul/li[2]/a").click()
        if driver.title == "One2team - Connexion":
            print("Deconnexion Successful Passed")
        else:
            print("Deconnexion Failed")

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
