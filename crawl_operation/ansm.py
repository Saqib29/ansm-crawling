from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver import DesiredCapabilities
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
import time


class SearchOperation:
    def __init__(self, driver_path):
        # chrome_option = Options()
        # chrome_option.add_argument('--headless')

        # capabilities = DesiredCapabilities.CHROME.copy()
        # capabilities['acceptSslCerts'] = True 
        # capabilities['acceptInsecureCerts'] = True

        # chromedriver = "../chromedriver/chromedriver"
        chromedriver = driver_path
        self.driver = webdriver.Chrome(chromedriver)
        # self.driver = webdriver.PhantomJS('D:/Lexero GmbH/phantomjs-2.1.1-windows/bin/phantomjs.exe')
        self.url = "https://ansm.sante.fr/S-informer/Informations-de-securite-Lettres-aux-professionnels-de-sante"


    def search(self, search_string):

        # keep chrome position away to hide window
        self.driver.set_window_position(-3000, -30)
        self.driver.get(self.url)
        self.driver.refresh()


        # get search field
        search_field = self.driver.find_elements_by_id('filter_text')[0]
        search_field.clear()

        # send searhed string and search
        search_field.send_keys(search_string)
        search_field.send_keys(Keys.ENTER)



        searched_results = []
        articles = self.driver.find_elements_by_tag_name('article')
        count = 0
        try:
            for i in range(1, len(articles)+1):
                data = self.driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/article['+ str(i) +']')
                try:
                        
                    category = data.find_element_by_xpath('//*[@id="wrapper"]/div/div/article[1]/a/span[1]').text
                    product_type = data.find_element_by_xpath('//*[@id="wrapper"]/div/div/article[1]/a/span[2]').text
                    content = data.find_element_by_class_name('article-content').text
                    article_date = data.find_element_by_class_name('article-date').text
                    article_title = data.find_element_by_class_name('article-title').text
                    count += 1
                    # print(product_type, category, article_date, article_title)
                except:
                    continue
                
                # appending data in the list searched_results 
                searched_results.append([count, category, product_type, article_date, article_title, content])

        except Exception as e:
            print(e)

        
        # time.sleep(10)
        self.driver.quit()

        total_result = len(searched_results)

        return (searched_results, total_result)


# obj = SearchOperation() 
# results = obj.search("Covid")



# print(results[0])
# print()
# print(results[1])
