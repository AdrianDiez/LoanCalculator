# Imports
import pandas as pd
from datetime import date
import numpy as np
from collections import OrderedDict
from dateutil.relativedelta import *


def amortize(principal, interest_rate, years, addl_principal=0, annual_payments=12, start_date=date.today()):
    # func to calculate the payments
    pmt = -round(np.pmt(interest_rate / annual_payments, years * annual_payments, principal), 2)
    # initialize the variables to keep track of the periods and running balances
    p = 1
    beg_balance = principal
    end_balance = principal

    while end_balance > 0:
        # Recalculate the interest based on the current balance
        interest = round(((interest_rate / annual_payments) * beg_balance), 2)

        # Determine payment based on whether or not this period will pay off the loan
        pmt = min(pmt, beg_balance + interest)
        principal = pmt - interest

        # Ensure additional payment gets adjusted if the loan is being paid off
        addl_principal = min(addl_principal, beg_balance - principal)
        end_balance = beg_balance - (principal + addl_principal)

        yield OrderedDict([('Month', start_date),
                           ('Period', p),
                           ('Begin Balance', beg_balance),
                           ('Payment', pmt),
                           ('Principal', principal),
                           ('Interest', interest),
                           ('Additional_Payment', addl_principal),
                           ('End Balance', end_balance)])

        # Increment the counter, balance and date
        p += 1
        start_date += relativedelta(months=1)
        beg_balance = end_balance


# interest_rate: current interest rate
# initial_date: date where the mortgage was sign
# current_date: current date
# top_cap: maximum interest rate possible
# one_time_cap: maximum growth of interest rate over one period
# loan_type: ARM type. The first number is the number of years where the interest doesn't change, the next the calculation period
# down: if the index go down the interest rate goes down with it?

def calculate_arm(interest_rate, initial_date, current_date, top_cap, one_time_cap, years, loan_type='5/1', down=True):
    pass


# Returns all the dates where we need to recalculate the interest rate
# initial_date: initial date of the calculation. datetime.date
# loan_type: ARM type. The first number is the number of years where the interest doesn't change, the next the calculation period
# years: number of years that the loan will be alive

def calculate_interest_changes(initial_date, loan_type, years):
    no_change = int(loan_type.split('/')[0])
    adjust = int(loan_type.split('/')[1])
    first_adjustment = add_years(initial_date, no_change)
    dates = [add_years(first_adjustment, x) for x in range(years - no_change) if x % adjust == 0]
    return dates


# Add years to the date d
# d: datetime.date
# years: number of years you want to add

def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))


print(calculate_interest_changes(date(2019, 3, 23), '5/3', 30))
schedule = pd.DataFrame(amortize(400000, .043, 30, addl_principal=0, start_date=date(2019, 5, 20)))
print(schedule['Interest'].sum())
print(schedule.head())
