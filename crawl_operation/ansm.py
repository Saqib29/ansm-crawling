from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time


class SearchOperation:
    def __init__(self):
        
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.url = "https://ansm.sante.fr/S-informer/Informations-de-securite-Lettres-aux-professionnels-de-sante"


    def search(self, search_string, date, anteriority):

        # keep chrome position away to hide window
        # self.driver.set_window_position(-3000, -30)
        self.driver.get(self.url)
        self.driver.refresh()

        """
        # searching strategy for type selection commented
        if search_string != '':
            search_field = self.driver.find_elements_by_id('filter_text')[0]
            search_field.clear()

            search_field.send_keys(search_string)
            search_field.send_keys(Keys.ENTER)

        elif search_string == '' and value_type != '':
            self.types(value_type)
        """

        # get seaching field and send search string
        search_field = self.driver.find_elements_by_id('filter_text')[0]
        search_field.clear()
        search_field.send_keys(search_string)
        search_field.send_keys(Keys.ENTER)



        #  search by date or anteriority
        if date[0] != '' and date[1] != '':
            self.select_date(date)
            
        elif anteriority != '':
            self.select_anteriority(anteriority)
            
        

        # crawling strategy
        time.sleep(2)
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
                    
                except:
                    continue
                
                # appending data in the list searched_results 
                searched_results.append([count, category, product_type, article_date, article_title, content])

        except Exception as e:
            print(e)

        time.sleep(5)
        self.driver.quit()
        total_result = len(searched_results)


        return (searched_results, total_result)





    # for selection an an anteriority
    def select_anteriority(self, anteriority):
        date_btn = self.driver.find_element_by_xpath('//*[@id="filter_result"]/div/div[2]/div/div[4]/a')
        date_btn.send_keys(Keys.ENTER)
        time.sleep(2)

        if anteriority == 'this_week':
            this_week = self.driver.find_element_by_xpath('//*[@id="h-filters4"]/div/div/div[1]/div/div[1]/label/span')
            this_week.click()
            
        elif anteriority == 'this_month':
            this_month = self.driver.find_element_by_xpath('//*[@id="h-filters4"]/div/div/div[1]/div/div[2]/label/span')
            this_month.click()

        elif anteriority == '6-month-old':
            this_month = self.driver.find_element_by_xpath('//*[@id="h-filters4"]/div/div/div[1]/div/div[3]/label/span')
            this_month.click()

        elif anteriority == '1-year-old':
            this_month = self.driver.find_element_by_xpath('//*[@id="h-filters4"]/div/div/div[1]/div/div[4]/label/span')
            this_month.click()

        time.sleep(2)
        valider = self.driver.find_element_by_link_text("Valider")
        self.driver.execute_script("arguments[0].click();", valider)





    # method to select time period
    def select_date(self, date):
        date_btn = self.driver.find_element_by_xpath('//*[@id="filter_result"]/div/div[2]/div/div[4]/a')
        date_btn.send_keys(Keys.ENTER)
        time.sleep(2)
        




    #  type selection method is not called for now
    def types(self, value_type):
        
        type = self.driver.find_element_by_xpath('//*[@id="wrapper"]/div[1]/a[4]')
        type.send_keys(Keys.ENTER)

        if value_type == 'DEFAUT_QUALITE':
            DEFAUT_QUALITE = self.driver.find_element_by_xpath('//*[@id="pt-filters-type"]/div/div[1]/div[1]/div[1]/div/div')
            DEFAUT_QUALITE.click()
        elif value_type == 'INFORMATION_AUX_UTILISATURS':
            INFORMATION_AUX_UTILISATURS = self.driver.find_element_by_xpath('//*[@id="pt-filters-type"]/div/div[1]/div[1]/div[2]/div/div')
            INFORMATION_AUX_UTILISATURS.click()
        elif value_type == 'RAPPEL_DE_PRODUIT':
            RAPPEL_DE_PRODUIT = self.driver.find_element_by_xpath('//*[@id="pt-filters-type"]/div/div[1]/div[1]/div[3]/div/div')
            RAPPEL_DE_PRODUIT.click()

        # RISQUES_MEDICAMENTEUX = self.driver.find_element_by_xpath('//*[@id="pt-filters-type"]/div/div[1]/div[2]/div/div/div')
        # RISQUES_MEDICAMENTEUX.click()
        
        click = self.driver.find_element_by_xpath('//*[@id="pt-filters-type"]/div/div[2]/a[1]')
        click.click()




# obj = SearchOperation() 
# results = obj.search("Covid")



# print(results[0])
# print()
# print(results[1])
