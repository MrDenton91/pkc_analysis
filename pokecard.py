import time
import logging, coloredlogs
from time import gmtime, strftime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
mylogs = logging.getLogger(__name__)
mylogs.setLevel(logging.INFO)

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='C:\\Users\\Nick\\Desktop\\Project_LcCollector\\pkLCollector.log', filemode='w')
coloredlogs.install(level=logging.INFO)

base_url = 'https://www.tcgplayer.com/search/pokemon/product?productLineName=pokemon&page=1&view=grid&ProductTypeName=Cards'



def card_collector():

    # where I currently have my chromedriver saved
    DRIVER_PATH = 'C:\\Users\\Nick\\Desktop\\Project_LcCollector\\chromedriver.exe'

    # want this to be in wodowless mode, can change with Headless
    options = Options()
    options.headless = False
    options.add_argument("--test-type")
    options.add_argument('--window-size=1920,1200')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options = options, executable_path = DRIVER_PATH) 


    pokemon_card = []
    pokemon_card_url = []
    pokemon_rarity = []
    pokemon_set = []
    pokemon_market_value = []

    rarity = ['Common', 'Uncommon', 'Promo', 'Rare', 'Holo+Rare', 'Ultra+Rare', 
    'Secret+Rare', 'Shiny+Holo+Rare', 'Prism+Rare', 'Rare+BREAK', 'Classic+Collection', 
    'Rare+Ace', 'Amazing+Rare', 'Radiant+Rare']
    #rarity = ['Common']

    rarity_dictionary = {}
    # going to need to grab the information by card rarity
    # 'https://www.tcgplayer.com/search/pokemon/product?productLineName=pokemon&page=1&view=grid&ProductTypeName=Cards&RarityName=Common'

    for rare in rarity:
        logging.info('Starting '+ rare +' Page Scrape')
        first_page_url = 'https://www.tcgplayer.com/search/pokemon/product?productLineName=pokemon&page=1&view=grid&ProductTypeName=Cards&RarityName='+ rare
        driver.get(first_page_url)
        time.sleep(7)
        try:
            number_of_pages= driver.find_element_by_xpath('/html/body/div[2]/div/div/section[2]/section/section/section/div[2]/div[1]/div/div[2]/button[10]/span')
            rarity_dictionary[rare] = int(number_of_pages.text)
        except:
            logging.info('Unable to Collect Total Number of Pages for ' + rare)
            logging.info('Setting page length to default of 11')
            rarity_dictionary[rare] = 11
    logging.info(rarity_dictionary)

    for y in rarity:
        # at most tcgplayer shows 200 pages of content
        # need to refine the loops such that Rarity is a dictionary keys = rarity solution = page numbers
        # first step is to hit each page 1 and grab the last bit of information
        # information can be located at this x_path element = /html/body/div[2]/div/div/section[2]/section/section/section/div[2]/div[1]/div/div[2]/button[10]/span
        ## grab the text vaule, and convert it to an interger

        ## For loop goes to each firrst page to find the total number of pages in each rarity type

        logging.info(str(rarity_dictionary[y]) + ' Total number of ' + y + ' pages')

        for i in range(1, int(rarity_dictionary[y]) +1):
            # the 24 entries per-page
            # populates Url
            cards_url = 'https://www.tcgplayer.com/search/pokemon/product?productLineName=pokemon&page='+ str(i) +'&view=grid&ProductTypeName=Cards&RarityName=' + str(y)
            driver.get(cards_url)
            time.sleep(2)

            for x in range(1,25):
                try:

                    # how many cards on in the rarity set
                    logging.info("Starting Colossal Battles Run " + str(i) + '/'+ str(rarity_dictionary[y] +1) + " in rarity " + y)
                    #num_of_rarity_cards = driver.find_element_by_xpath('/html/body/div[3]/div/div/section[2]/section/section/div/div[2]/div[3]/div[1]/div/div/span[1]/span/text()')    
                    current_card = x*i
                    # creating variables to populate appropriate lists
                    # Current Bug / issue lies in the scrapping proceess in one of these elements or all
                    ## Warrents futher investigation,

                    ### findings first element isn't being grabbed need to retune scrapping
                    #logging.info("Starting Pokemon Card poke_card_title grab")
                    poke_card_title = driver.find_element_by_xpath( '/html/body/div[2]/div/div/section[2]/section/section/section/section/div[' + str(x) + ']/div/a/section/span[3]')
            
                    #/html/body/div[2]/div/div/section[2]/section/section/section/section/div[1]/div/a/section
                    #/html/body/div[2]/div/div/section[2]/section/section/section/section/div[2]/div/a/section
                    #/html/body/div[2]/div/div/section[2]/section/section/section/section/div[1]/div/a
                    card_url = driver.find_element_by_xpath('/html/body/div[2]/div/div/section[2]/section/section/section/section/div[' + str(x) +']/div/a' )

                    #logging.info("Starting Pokemon Card poke_card_rarity grab")
                    poke_card_rarity = driver.find_element_by_xpath( '/html/body/div[2]/div/div/section[2]/section/section/section/section/div[' + str(x) + ']/div/a/section/section[2]/span[1]')

                    
                    #logging.info("Starting Pokemon Card poke_card_set grab")
                    poke_card_set = driver.find_element_by_xpath( '/html/body/div[2]/div/div/section[2]/section/section/section/section/div[' + str(x) + ']/div/a/section/span[2]')

                    #poke_card_set_number = driver.find_element_by_xpath( '/html/body/div[2]/div/div/section[2]/section/section/section/section/div[' + str(x) + ']/div/a/section/span[2]/span[3]')
                    #logging.info("Starting Pokemon Card poke_card_set_number grab")

                    poke_card_market_value = driver.find_element_by_xpath( '/html/body/div[2]/div/div/section[2]/section/section/section/section/div[' + str(x) + ']/div/a/section/section[3]/section/span[2]')
                    #logging.info("Starting Pokemon Card poke_card_market_value grab")
                    #logging.info('Battling ' + str(current_card) +  " / " + poke_card_title.text)

                    logging.info("Captured " + poke_card_title.text + " at Price " + poke_card_market_value.text)

                    # populate lists
                    #logging.info('Captured: ' + poke_card_title.text)
                    pokemon_card.append(str(poke_card_title.text))
                    pokemon_card_url.append(str(card_url.get_attribute('href')))
                    pokemon_rarity.append(str(poke_card_rarity.text))
                    pokemon_set.append(str(poke_card_set.text))
                    #pokemon_set_number.append(str(poke_card_set_number))
                    pokemon_market_value.append(str((poke_card_market_value.text).replace("$","")))

                    logging.info(poke_card_title.text + " Added to Collection")
                    #logging.info('Captured ' + str(current_card.text) +  " / " + num_of_rarity_cards.text)
                    
                except:
                    logging.info('Unable to capture last entry' + str(x))
           
    ## Grabing information on the sealed products

    time.sleep(3)
    logging.info('Starting Colossal Booster Runs')
    for q in range(1,201):

        cards_url = 'https://www.tcgplayer.com/search/pokemon/product?productLineName=pokemon&page=' + str(q) + '&view=grid&ProductTypeName=Sealed+Products'
        #https://www.tcgplayer.com/search/pokemon/product?productLineName=pokemon&page=1&view=grid&ProductTypeName=Sealed+Products&RarityName=
        driver.get(cards_url)
        time.sleep(3)
        logging.info("Starting Sealed Product Run " + str(q))

        for xr in range(1,25):
            try:
                #print("poke_sealed_prodcut items")
                poke_sealed_prodcut = driver.find_element_by_xpath( '/html/body/div[2]/div/div/section[2]/section/section/section/section/div[' + str(xr) + ']/div/a/section/span[3]')
                #print("poke_card_set items")

                poke_card_set = driver.find_element_by_xpath( '/html/body/div[2]/div/div/section[2]/section/section/section/section/div[' + str(xr) + ']/div/a/section/span[2]')
                #print("poke_card_market_value items")
                poke_card_market_value = driver.find_element_by_xpath( '/html/body/div[2]/div/div/section[2]/section/section/section/section/div[' + str(xr) + ']/div/a/section/section[2]/section/span[2]')
                card_url = driver.find_element_by_xpath('/html/body/div[2]/div/div/section[2]/section/section/section/section/div[' + str(xr) +']/div/a' )
                #print("card_url items")
                logging.info('Booster ' + poke_sealed_prodcut.text + ' Collected')
                #print("adding items")
                pokemon_card.append(str(poke_sealed_prodcut.text))
                pokemon_card_url.append(str(card_url.get_attribute('href')))
                pokemon_rarity.append('Sealed+Products')
                pokemon_set.append(str(poke_card_set.text))
                #pokemon_set_number.append(str(poke_card_set_number))
                pokemon_market_value.append(str((poke_card_market_value.text).replace("$","")))

                logging.info(poke_sealed_prodcut.text + " Added to Collection")
            except:
                logging.info('Unable to caputre Booster last entry')




    driver.quit()
    logging.info('Capture Runs Complete')

    return pokemon_card, pokemon_card_url, pokemon_rarity, pokemon_set, pokemon_market_value

def outputToCSV(pokemon_card, pokemon_card_url, pokemon_rarity, pokemon_set, pokemon_market_value):
    
    date = str(strftime("%Y-%m-%d", gmtime()))
    file_name = str(date) + '_pkdata.csv'
    file_location = './' + file_name
    logging.info("Creating Database File")

    fields = ['Name', 'Url', 'Rarity', 'Set', 'Market Value']

    with open(file_location, 'a') as f:
        for x in range(0,len(fields)):
            f.write("%s," % fields[x])
        f.write("\n")
        for i in range(0,len(pokemon_card)):
            f.write("%s," % pokemon_card[i])
            f.write("%s," % pokemon_card_url[i])
            f.write("%s," % pokemon_rarity[i])
            f.write("%s," % pokemon_set[i])
            f.write("%s" % pokemon_market_value[i])
            f.write("\n")
            logging.info(str(i + 1) + '/' + str(len(pokemon_card)))
        f.close()
    logging.info("Completed Database " + file_name)
    
  
    pass

if __name__ == '__main__':
    pokemon_card, pokemon_card_url, pokemon_rarity, pokemon_set, poke_card_market_value = card_collector()
    outputToCSV(pokemon_card, pokemon_card_url, pokemon_rarity, pokemon_set, poke_card_market_value)

##############################################
    ## First Entry on a Page
    #/html/body/div[3]/div/div/section[2]/section/section/section/section/div[1]/div/a/section/span[3]

    ## last Entry on a Page
    #/html/body/div[3]/div/div/section[2]/section/section/section/section/div[24]/div/a/section/span[3]

##############################################

    ## Pokemon Card Title 
    #/html/body/div[3]/div/div/section[2]/section/section/section/section/div[7]/div/a/section/span[3]

    ## Rarity of card
    #/html/body/div[3]/div/div/section[2]/section/section/section/section/div[7]/div/a/section/section[2]/span[1]

    ## Pokemon Set Title
    #/html/body/div[3]/div/div/section[2]/section/section/section/section/div[7]/div/a/section/span[2]

    ## Number in that set 
    #/html/body/div[3]/div/div/section[2]/section/section/section/section/div[7]/div/a/section/section[2]/span[3]

    ## Market Price for Card
    #/html/body/div[3]/div/div/section[2]/section/section/section/section/div[7]/div/a/section/section[3]/section/span[2]

##############################################