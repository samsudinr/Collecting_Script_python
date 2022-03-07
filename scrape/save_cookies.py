# save the current cookies as a Python object using pickle
import pickle
import selenium.webdriver

driver = selenium.webdriver.Firefox()
driver.get("http://www.google.com")
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

# read cookies
import pickle
import selenium.webdriver

driver = selenium.webdriver.Firefox()
driver.get("http://www.google.com")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
