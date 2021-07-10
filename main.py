from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import csv
import matplotlib.pyplot as plt
import math

global driver
global actions

driver = webdriver.Firefox()
actions = ActionChains(driver)

# DECLARE ALL OF THE JANK ASS FUNCTIONS #
#########################################

def start_program():
    driver.get("https://fjhoneycomb.steadylogic.com/?lang=en-US&sessionKey=3a2c661aeaf50d0ffaa6dd7d37019081")

def get_cells_remaining():
    cells = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[2]/div[1]/div/div/front-additional-parts/div/div[1]/div/div[2]')
    return int(cells.text)

def get_portfolio_value():
    portfolio = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[3]/div[1]/app-bet/div/div[1]/div[2]/div[1]')
    return float(portfolio.text)

def get_last_multiplier():
    recent_bet = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[1]/div[1]/app-betting-history/div/front-my-bets/div/div[2]/div/div[3]')
    return recent_bet.text

def get_time():
    time = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[2]/div[1]/div/div/front-additional-parts/div/div[3]/div/div[2]')
    return time.text

def get_last_user():
    username = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[2]/div[2]/front-betting/div/div[2]/div[2]/div[1]/div[1]/strong')
    return username.text

def get_data():
    cells_remaining = get_cells_remaining()
    portfolio_value = get_portfolio_value()
    last_multiplier = get_last_multiplier()
    current_time = get_time()
    return {'cells remaining' : cells_remaining , 'portfolio value' : portfolio_value ,
            'last multiplier' : float(last_multiplier[:-1]) , 'time remaining' : current_time}


def send_in_order(order_size):
    random_button = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[3]/div[1]/app-bet/div/div[2]/div[2]/front-random-button/div')
    bet_amount_box = driver.find_element_by_xpath('/html/body/front-root/front-game/div/div/div/div[3]/div[1]/app-bet/div/div[2]/div[1]/div/app-amount-selector/div/div[1]/div/app-amount-input-standard/div/div/input')
    bet_amount_box.send_keys(Keys.CONTROL , 'a')
    bet_amount_box.send_keys(Keys.BACKSPACE)
    time.sleep(0.3)
    bet_amount_box.send_keys(str(order_size))
    time.sleep(0.3)
    actions.click(random_button)
    actions.perform()
    print('sent in order , size of  = ' + str(order_size))


def calculate_kelly(remaining_multipliers):
    setu = set(remaining_multipliers)
    values = {}
    length = len(remaining_multipliers)
    for x in setu:
        total = remaining_multipliers.count(x)
        probability = total/length
        x = x -1
        values.update({x : probability})

    sums = []
    xs = []
    for i in range(10000):
        i = i /(20000)
        xs.append(i)
        sum = kelly_shizz(i , values)
        sums.append(sum)

    max = np.argmax(sums)
    amount_to_bet = xs[max]
    return amount_to_bet

def calc_EV(remaining_multipliers):
    EV = (sum(remaining_multipliers) / len(remaining_multipliers))-1
    return EV


def kelly_shizz(x , dict ):
    sum = 0
    for key , value in dict.items():
        sum = sum + (value * np.log(1 + (key * x)))
    return sum
##########################################################################################



### GET ALL THE BASE VARIABLES GOING ###
base_multipliers = [1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.05,1.1,1.1,1.1,
                    1.1,1.1,1.1,1.1,1.1,1.1,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.2,1.3,1.3,1.3,
                    1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.6,1.6,
                    1.6,1.6,1.6,1.6,1.6,1.6,1.6,1.6,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8,2,2,2,2,2,2,
                    2,3,3,3,3,3,3,4,4,4,4,5,5,5,8,8,10,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


time.sleep(5)
starting_portfolio_value = 350
maximum_drawdown = 100
maximum_profit = 5000
last_round_cells = 78
remaining_multipliers = base_multipliers.copy()
cease_algorithm = False
#maximum_order_size = 0.5
kelly_bet = 0.1
last_round_bet = True
user = 'martingaleFTW'
new_round = True
portfolio_value = []

##############################################################
# open up a csv and write some garbage data to it
f = open('honeybeegamedata.csv', 'a')
writer = csv.writer(f)
### OPEN UP THE WEBPAGE AND CLICK ON A GAME ####
start_program()
time.sleep(20)  #wait a few seconds to open up the webpage

while cease_algorithm == False:

    ### TRY TO PULL IN DATA ###
    data_acquired = False
    try:
        data = get_data()
        data_acquired = True
        print(data)
    except:
        print("there was an error in getting the data , no order will be sent")

    if data_acquired != False and data['time remaining'][:2] != '00' and data['cells remaining'] >= 3:
        ### STOP THE ALGORITHM IF WE EXCEED OUR DRAWDOWN LIMIT ###
        if maximum_drawdown < get_portfolio_value() and maximum_profit > get_portfolio_value():
            pass
        else:
            print('algorithm was halted since either maximum drawdown or profit was reached')
            cease_algorithm = True
            break

        ### Check if we are on a new round
        new_round = False
        if last_round_cells < get_cells_remaining() or get_cells_remaining() == 78:
            remaining_multipliers = base_multipliers.copy()
            print('there is a new round len remaining = ' + str(len(remaining_multipliers)))
            new_round = True

        # UPDATE THE LIST
        if new_round == False:
            try:
                remaining_multipliers.remove(data['last multiplier'])
                print(len(remaining_multipliers) , data['cells remaining'])
            except:
                print("multiplier already removed")

        # CALC KELLY AND EV
        kelly_prct = calculate_kelly(remaining_multipliers)
        kelly_bet = math.floor((((data['portfolio value'] * kelly_prct))*.9))
        EV = calc_EV(remaining_multipliers)
        print("expected value = " + str(EV) , " |   Kelly Bet = " + str(kelly_bet))

        last_round_bet = True
        # SEND IN THE ORDER
        if new_round == False and data['cells remaining'] == (last_round_cells - 1) and EV > -0.05 and get_last_user() == user:
            if kelly_bet <= 0.1:
                send_in_order(0.1)
            elif kelly_bet > (data['portfolio value'] * .02):
                send_in_order(math.floor(data['portfolio value'] * .02))
            else:
                send_in_order(kelly_bet)

            actions = 'cat'
            actions = ActionChains(driver)


        elif new_round == True:
            send_in_order(0.1)
            actions = 'cat'
            actions = ActionChains(driver)

        elif get_last_user() != user:
           print("another player detected no new orders will be placed until next new round")


    last_round_cells = get_cells_remaining()


    try:
        writer.writerow([data['portfolio value'] , data['cells remaining'] , EV , kelly_bet])
        f.flush()
    except:
        print('unable to write data to csv right now')


    time.sleep(np.random.rand() + 1)
