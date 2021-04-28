from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


class SearchOperation:
    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("headless")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.url = "https://ansm.sante.fr/S-informer/Informations-de-securite-Lettres-aux-professionnels-de-sante"


    # main search method
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
        # headless solved after add this strategies instead
        value = self.driver.execute_script('return arguments[0].value;', search_field)
        self.driver.execute_script('''
            var elem = arguments[0];
            var value = arguments[1];
            elem.value = value;
        ''', search_field, search_string)
        search_icon = self.driver.find_element_by_xpath('//*[@id="btn-header-icon"]')
        self.driver.execute_script('arguments[0].click();', search_icon)
        
        self.driver.implicitly_wait(2)

        search_button = self.driver.find_element_by_xpath('//*[@id="btn-header-search"]')
        self.driver.execute_script('arguments[0].click();', search_button)



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
                    # try except for each 
                    try:
                        category = data.find_element_by_xpath('//*[@id="wrapper"]/div/div/article[1]/a/span[1]').text
                    except:
                        category = 'N/A'
                    
                    try:
                        product_type = data.find_element_by_xpath('//*[@id="wrapper"]/div/div/article[1]/a/span[2]').text
                    except:
                        product_type = 'N/A'
                    
                    try:
                        article_date = data.find_element_by_class_name('article-date').text
                    except:
                        article_date = 'N/A'


                    content = data.find_element_by_class_name('article-content').text
                    if len(content) == 0:
                        content = 'N/A'
                    article_title = data.find_element_by_class_name('article-title').text
                    count += 1
                    
                except:
                    continue
                
                # appending data in the list searched_results 
                searched_results.append([count, category, product_type, article_date, article_title, content])

        except Exception as e:
            print(e)

        time.sleep(5)
        # self.driver.quit()
        total_result = len(searched_results)


        return (searched_results, total_result)





    # for selection an an anteriority
    def select_anteriority(self, anteriority):
        date_btn = self.driver.find_element_by_xpath('//*[@id="filter_result"]/div/div[2]/div/div[4]/a')
        # date_btn.send_keys(Keys.ENTER)
        self.driver.execute_script("arguments[0].click();", date_btn)
        time.sleep(2)

        if anteriority == 'this_week':
            this_week = self.driver.find_element_by_xpath('//*[@id="h-filters4"]/div/div/div[1]/div/div[1]/label/span')
            # this_week.click()
            self.driver.execute_script("arguments[0].click();", this_week)

            
        elif anteriority == 'this_month':
            this_month = self.driver.find_element_by_xpath('//*[@id="h-filters4"]/div/div/div[1]/div/div[2]/label/span')
            # this_month.click()
            self.driver.execute_script("arguments[0].click();", this_month)


        elif anteriority == '6-month-old':
            this_month = self.driver.find_element_by_xpath('//*[@id="h-filters4"]/div/div/div[1]/div/div[3]/label/span')
            # this_month.click()
            self.driver.execute_script("arguments[0].click();", this_month)


        elif anteriority == '1-year-old':
            this_month = self.driver.find_element_by_xpath('//*[@id="h-filters4"]/div/div/div[1]/div/div[4]/label/span')
            # this_month.click()
            self.driver.execute_script("arguments[0].click();", this_month)
            

        time.sleep(2)
        self.valider()




    #  valider button
    def valider(self):
        valider = self.driver.find_element_by_link_text("Valider")
        self.driver.execute_script("arguments[0].click();", valider)




    # method to select time period by date
    def select_date(self, date):
        date_btn = self.driver.find_element_by_xpath('//*[@id="filter_result"]/div/div[2]/div/div[4]/a')
        self.driver.execute_script("arguments[0].click();", date_btn)
        time.sleep(2)

        # set start date
        startDate = self.driver.find_element_by_id('filter_startDate')
        value = self.driver.execute_script('return arguments[0].value;', startDate)
        self.driver.execute_script('''
            var elem = arguments[0];
            var value = arguments[1];
            elem.value = value;
        ''', startDate, date[0])

        # set end date
        endDate = self.driver.find_element_by_id('filter_endDate')
        value = self.driver.execute_script('return arguments[0].value;', endDate)
        self.driver.execute_script('''
            var elem = arguments[0];
            var value = arguments[1];
            elem.value = value;
        ''', endDate, date[1])

        time.sleep(1)
        self.valider()
        
        



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


