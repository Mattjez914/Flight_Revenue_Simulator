# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory


#below this point is the code that was given - nat
from IPython.display import display, Javascript
import json
from numpy.random import uniform, seed
from numpy import floor
from collections import namedtuple

def _tickets_sold(p, demand_level, max_qty):
        quantity_demanded = floor(max(0, p - demand_level))
        return min(quantity_demanded, max_qty)

def _save_score(score):
    message = {
        'jupyterEvent': 'custom.exercise_interaction',
        'data': {
            'learnTutorialId': 0,
            'interactionType': "check",
            'questionId': 'Aug31OptimizationChallenge',
            'outcomeType': 'Pass',
            'valueTowardsCompletion': score/10000,
            'failureMessage': None,
            'learnToolsVersion': "Testing"
        }
    }
    js = 'parent.postMessage(%s, "*")' % json.dumps(message)
    display(Javascript(js))

def simulate_revenue(days_left, tickets_left, pricing_function,a,b, rev_to_date=0, demand_level_min=100, demand_level_max=200, verbose=False):
    if (days_left == 0) or (tickets_left == 0):
        if verbose:
            if (days_left == 0):
                print("The flight took off today. ")
            if (tickets_left == 0):
                print("This flight is booked full.")
            print("Total Revenue: ${:.0f}".format(rev_to_date))
        return rev_to_date
    else:
        demand_level = uniform(demand_level_min, demand_level_max)
        p = pricing_function(days_left, tickets_left, demand_level,a,b)
        q = _tickets_sold(demand_level, p, tickets_left)
        if verbose:
            print("{:.0f} days before flight: "
                  "Started with {:.0f} seats. "
                  "Demand level: {:.0f}. "
                  "Price set to ${:.0f}. "
                  "Sold {:.0f} tickets. "
                  "Daily revenue is {:.0f}. Total revenue-to-date is {:.0f}. "
                  "{:.0f} seats remaining".format(days_left, tickets_left, demand_level, p, q, p*q, p*q+rev_to_date, tickets_left-q))
        return simulate_revenue(days_left = days_left-1,
                              tickets_left = tickets_left-q,
                              pricing_function=pricing_function,
                              a = a,
                              b = b,
                              rev_to_date=rev_to_date + p * q,
                              demand_level_min=demand_level_min,
                              demand_level_max=demand_level_max,
                              verbose=verbose)

def pricing_function_monte_carlo(days_left, tickets_left, demand_level,a,b):
    """Sample pricing function"""
    if days_left == 1:
        price = demand_level - tickets_left
    elif days_left == 2:
        if demand_level > 179: 
            price = demand_level - tickets_left
        else:
            price = demand_level - tickets_left/2 
    else:
        if days_left > a:
            if demand_level > b:
                price = demand_level - 8
            else: 
                price = demand_level + 1
        elif days_left > 12: 
            if demand_level > 186:
                price = demand_level - 8
            else:
                price = demand_level + 1
        elif days_left > 3:
            if tickets_left/days_left > 2.5:
                if demand_level > 169:
                    price = demand_level - 17
                else:
                    price = demand_level + 1
            else:
                if demand_level > 180:
                    price = demand_level - 20
                else:
                    price = demand_level + 1
        else: 
            if demand_level > 169:
                price = demand_level - 20
            else:
                price = demand_level - 1
    return price

def score_me_monte_carlo(pricing_function, a, b, sims_per_scenario=200):
    seed(0)
    Scenario = namedtuple('Scenario', 'n_days n_tickets')
    scenarios = [Scenario(n_days=100, n_tickets=100),
                 Scenario(n_days=14, n_tickets=50),
                 Scenario(n_days=2, n_tickets=20),
                Scenario(n_days=1, n_tickets=3),
                 ]
    scenario_scores = []
    days = []
    tickets = []
    scenario_score_list = []
    for s in scenarios:
        scenario_score = sum(simulate_revenue(s.n_days, s.n_tickets, pricing_function,a,b)
                                     for _ in range(sims_per_scenario)) / sims_per_scenario
        #print("Ran {:.0f} flights starting {:.0f} days before flight with {:.0f} tickets. "
              #"Average revenue: ${:.0f}".format(sims_per_scenario,
                                                #s.n_days,
                                                #s.n_tickets,
                                                #scenario_score))
        # easier to record data print (days before flight,tickets,average revenue)
        #print(s.n_days,s.n_tickets,scenario_score)                               
        scenario_scores.append(scenario_score)
        days.append(s.n_days)
        tickets.append(s.n_tickets)
        scenario_score_list.append(scenario_score)
    score = sum(scenario_scores) / len(scenario_scores)
    try:
        _save_score(score)
    except:
        pass
    #print(score)
    return [days,tickets,scenario_score_list]

#score_me_monte_carlo(pricing_function_monte_carlo,2.5, sims_per_scenario=200)


def run_monte_carlo3():
    variable1_value =[]
    variable2_value = []
    days_variable = []
    tickets_variable = []
    scenario_score_variable =[]
    for a in range (13, 100):
        for b in range (150,200):
            x = score_me_monte_carlo(pricing_function_monte_carlo,a,b,sims_per_scenario=200)
            list_days = x[0]
            list_tickets=x[1]
            scenario_score=x[2]
            for i in range(len(list_days)):
                variable1_value.append(a)
                variable2_value.append(b)
                days_variable.append(list_days[i])
                tickets_variable.append(list_tickets[i])
                scenario_score_variable.append(scenario_score[i])
    mega_list = [variable1_value,variable2_value,days_variable,tickets_variable,scenario_score_variable]
    table = list_for_pandas(mega_list)
    return table


def list_for_pandas (run_value):
    variable1_value = run_value[0]
    variable2_value = run_value[1]
    days_variable = run_value[2]
    tickets_variable = run_value[3]
    scenario_score_variable = run_value[4]
    big_list = []
    #gotta make a bunch of little lists
    for i in range(len(variable1_value)):
        mini_list = [variable1_value[i],variable2_value[i],days_variable[i], tickets_variable[i], scenario_score_variable[i]]
        big_list.append(mini_list)
    table = pd.DataFrame(big_list)
    return table


def find_max_for_each_simulation (df):
    df.columns = ['variable','days','tickets','revenue']
    one_hundred = df[df.days == 100]
    one_hundred = one_hundred.sort_values(['revenue'])
    fourteen = df[df.days == 14]
    fourteen = fourteen.sort_values(['revenue'])
    two = df[df.days == 2]
    two = two.sort_values(['revenue'])
    one = df[df.days == 1]
    one = one.sort_values(['revenue'])
    return [one_hundred, fourteen, two, one]

def put_together():
    table = run_monte_carlo3()
    #choice 1
    table.columns = ['variable1','variable2','days','tickets','revenue']
    new_table = table.sort_values(['days','revenue'])
    return new_table
    #choice 2
    #seperate_simulation_df = find_max_for_each_simulation(table)
    #return seperate_simulation_df

#z = run_monte_carlo3()
#monte_carlo_panda_frame = list_for_pandas(z)
#monte_carlo_panda_frame.transpose()
#monte_carlo_panda_frame


