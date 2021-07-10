from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
driver = webdriver.Chrome()
actions = ActionChains(driver)

def start_program():
    driver.get("https://fjhoneycombdemo.steadylogic.com/?lang=en-US&sessionKey=715aaef2616a882c31dc5489965a6c5a")

def get_cells_remaining():
    cells = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[2]/div[1]/div/div/front-additional-parts/div/div[1]/div/div[2]')
    return int(cells.text)

def get_portfolio_value():
    portfolio = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[3]/div[1]/app-bet/div/div[1]/div[2]/div[1]')
    return float(portfolio.text)

def get_last_multiplier():
    recent_bet = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[1]/div[1]/app-betting-history/div/front-my-bets/div/div[2]/div/div[3]')
    return recent_bet.text

def get_data():
    cells_remaining = get_cells_remaining()
    portfolio_value = get_portfolio_value()
    last_multiplier = get_last_multiplier()
    return {'cells remaining' : cells_remaining , 'portfolio value' : portfolio_value , 'last multiplier' : float(last_multiplier[:-1])}

def send_in_order(order_size):
    random_button = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[3]/div[1]/app-bet/div/div[2]/div[2]/front-random-button/div')
    bet_amount_box = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[3]/div[1]/app-bet/div/div[2]/div[1]/div/app-amount-selector/div/div[1]/div/app-amount-input-standard/div/div/input')
    bet_amount_box.send_keys(Keys.CONTROL , 'a')
    bet_amount_box.send_keys(Keys.BACKSPACE)
    time.sleep(0.5)
    bet_amount_box.send_keys(str(order_size))
    actions.click(random_button).perform()
    actions.reset_actions()


