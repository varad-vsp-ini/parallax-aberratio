"""
newcomb_core.py

Core static Newcomb's Problem simulation: payoff matrix, CDT/EDT agents,
an adaptive Predictor (blind accuracy + history-informed guessing), and
the Simulate() function that runs N trials at a given (p_base, alpha).

This file is a LIBRARY — it defines functions and constants only. It does
not take user input, generate plots, or run anything on import. That's
intentional: run_sweep.py (and applications/slop_detector/slop_newcomb.py)
both import directly from this file, so the core logic lives in exactly
one place.
"""

import random as r
import numpy as np

# ------------------------------------------------------------------
# The World
# ------------------------------------------------------------------
ONE = 1   # one-box
TWO = 2   # two-box

# Payoff Matrix
# rows = agent action (ONE, TWO), cols = predictor's guess (ONE, TWO)
payoff_matrix = np.array([
    [1000000, 0],
    [1001000, 1000]
])

MIN_HISTORY = 5  # cold-start threshold before the informed guess trusts the mode


def opposite(A):
    return TWO if A == ONE else ONE


# ------------------------------------------------------------------
# Agents
# ------------------------------------------------------------------
def CDTAgent():
    """Strategic dominance check on the payoff matrix — generalized,
    works for any 2x2 payoff matrix, not hardcoded to these numbers."""
    one_box_payoffs = payoff_matrix[0, :]
    two_box_payoffs = payoff_matrix[1, :]

    if np.all(two_box_payoffs > one_box_payoffs):
        return TWO
    elif np.all(one_box_payoffs > two_box_payoffs):
        return ONE
    else:
        return r.randint(ONE, TWO)  # no clean dominance


def EDTAgent(p):
    """Expected utility computed directly from the payoff matrix."""
    EU_one = p * payoff_matrix[0, 0] + (1 - p) * payoff_matrix[0, 1]
    EU_two = p * payoff_matrix[1, 1] + (1 - p) * payoff_matrix[1, 0]

    if EU_one == EU_two:
        return r.randint(ONE, TWO)
    return ONE if EU_one > EU_two else TWO


# ------------------------------------------------------------------
# Predictor
# ------------------------------------------------------------------
def InformedGuess(history):
    """Guess the mode of past actions. Cold-starts to a random guess
    until MIN_HISTORY observations are available."""
    if len(history) < MIN_HISTORY:
        return r.randint(ONE, TWO)

    count_one = history.count(ONE)
    count_two = history.count(TWO)

    if count_one == count_two:
        return r.randint(ONE, TWO)
    return ONE if count_one > count_two else TWO


def Predictor(A, p_base, alpha, history):
    """
    With probability alpha: use the history-informed guess (adaptive branch).
    With probability (1-alpha): use the blind mechanism — matches the
    agent's actual action with probability p_base, else flips it.

    NOTE: the informed branch never sees the current trial's action A,
    only past history — this avoids the circularity of the predictor
    "grading its own guess." Correctness of the informed branch emerges
    naturally from comparing the guess to A after the fact.
    """
    if r.random() < alpha:
        return InformedGuess(history)
    else:
        return A if r.random() < p_base else opposite(A)


def Transfer(predictor_guess, agent_choice, Acct):
    if predictor_guess == ONE and agent_choice == ONE:
        Acct += 1000000
    elif predictor_guess == ONE and agent_choice == TWO:
        Acct += 1001000
    elif predictor_guess == TWO and agent_choice == ONE:
        Acct += 0
    elif predictor_guess == TWO and agent_choice == TWO:
        Acct += 1000
    return Acct


# ------------------------------------------------------------------
# Experiment harness
# ------------------------------------------------------------------
def Simulate(p_base, alpha, n):
    """
    Runs n trials of CDT and EDT agents (each with their own fresh
    history) against the same Predictor design, at fixed (p_base, alpha).

    Returns: (CDT_mean, EDT_mean, CDT_accuracy, EDT_accuracy)
    """
    ct_CDT = 0
    ct_EDT = 0
    CDTBal = 0
    EDTBal = 0

    history_CDT = []
    history_EDT = []

    for _ in range(n):

        A_CDT = CDTAgent()
        Ahat_CDT = Predictor(A_CDT, p_base, alpha, history_CDT)
        history_CDT.append(A_CDT)

        A_EDT = EDTAgent(p_base)
        Ahat_EDT = Predictor(A_EDT, p_base, alpha, history_EDT)
        history_EDT.append(A_EDT)

        CDTBal = Transfer(Ahat_CDT, A_CDT, CDTBal)
        EDTBal = Transfer(Ahat_EDT, A_EDT, EDTBal)

        if Ahat_CDT == A_CDT:
            ct_CDT += 1
        if Ahat_EDT == A_EDT:
            ct_EDT += 1

    CDT_mean = CDTBal / n
    EDT_mean = EDTBal / n
    CDT_accuracy = ct_CDT / n
    EDT_accuracy = ct_EDT / n

    return CDT_mean, EDT_mean, CDT_accuracy, EDT_accuracy
