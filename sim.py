# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 04:14:02 2026

@author: Varad
"""
import random as r
import matplotlib.pyplot as plt
import numpy as np

# The World
# Agent choices
ONE = 1
TWO = 2

# Box possibilities
M = [0, 1000000]

p = float(input("Enter accuracy value: "))
n = int(input("How Many Times Should Experiment Run? : "))

# Payoff Matrix
payoff_matrix = np.array([
    [1000000, 0],
    [1001000, 1000]
])

def opposite(A):
    if A == ONE:
        A = TWO
    else:
        A = ONE
    return A
def Predictor(A):
    if r.random() < p:
        A_hat = A
    else:
        A_hat = opposite(A)
    return A_hat
        
def EDTAgent():
    EU = np.array([
        1000000 * p,
        1001000 - 1000000 * p
    ])

    if EU[0] == EU[1]:
        return r.randint(ONE, TWO)

    action_index = np.argmax(EU)

    return action_index + 1
    
def CDTAgent():
    one_box_payoffs = payoff_matrix[0, :]
    two_box_payoffs = payoff_matrix[1, :]

    if np.all(two_box_payoffs > one_box_payoffs):
        return TWO
    else:
        return ONE

def Transfer(predictor, agentchoice, Acct):
    if(predictor == ONE and agentchoice == ONE):
        Acct = Acct + 1000000
    elif(predictor == ONE and agentchoice == TWO):
        Acct = Acct + 1001000
    elif(predictor == TWO and agentchoice == ONE):
        Acct = Acct + 0
    elif(predictor == TWO and agentchoice == TWO):
        Acct = Acct + 1000
    return Acct
    

def Simulate(n):
    ct_CDT = 0
    ct_EDT = 0
    CDTBal = 0
    EDTBal = 0
    for i in range(n):
    
        # CDT
        A_CDT = CDTAgent()
        Ahat_CDT = Predictor(A_CDT)
    
        # EDT
        A_EDT = EDTAgent()
        Ahat_EDT = Predictor(A_EDT)
    
        if i < 5:
            print("Trial:", i + 1)
            print("CDT:", A_CDT, Ahat_CDT)
            print("EDT:", A_EDT, Ahat_EDT)
    
        CDTBal = Transfer(Ahat_CDT, A_CDT, CDTBal)
        EDTBal = Transfer(Ahat_EDT, A_EDT, EDTBal)
        
        if Ahat_CDT == A_CDT:
            ct_CDT += 1

        if Ahat_EDT == A_EDT:
            ct_EDT += 1
        
        
        
    print("Correct:", ct_CDT+ct_EDT)
    print("Total:", n)
    print("Observed accuracy:", (ct_CDT+ct_EDT) / (2*n))
    print(CDTBal)
    print(EDTBal)

Simulate(n)
