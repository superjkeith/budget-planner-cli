from datetime import datetime, date, timedelta
income_list = []

savings_rate = 0
Summary = ""


def days_till_due(due_date):
    return (due_date - date.today()).days

def due_message(days):
    if days < 0:
        return f"Overdue by {-days} days"
    elif days == 0:
        return "Due today"
    else:
        return f"Due in {days} days"

def pay_per_week(days_due, price):
    if days_due <= 0:
        return None
    weeks = (days_due + 6) // 7
    return round(price / weeks, 2)
   

def convert_amount(income, freqi):
    if freqi == "monthly":
        monthly = income
        weekly = income / 4
    elif freqi == "weekly":
        weekly = income
        monthly = income * 4
    elif freqi == "biweekly":
        weekly = income / 2
        monthly = income * 2
    else:
        weekly = 0
        monthly = 0
    return weekly, monthly
def money_savings(save, Rem_bal):
    return save * Rem_bal
def income_menu(income_list):
        qiname = input("What is the name of your income? ")
        while True:
            try:
                income = float(input("What is the amount of your income? "))
                break
            except ValueError:
                print("need a number, try again")
        while True:
            freqi = input("are you paid monthly, weekly, or biweekly").lower()
            if freqi in ["monthly", "weekly", "biweekly"]:
                break
            else:
                print("Invalid Answer, can you put weekly, biweekly, or monthly.") 
        income_list.append([qiname,income, freqi])      
expense_list = []#expense function
def expense_menu(expense_list):
         qename = input("What is the name of your expense? ")
         while True:
            try:
                expense = float(input("How much is your expenses? "))
                break
            except ValueError:
                print("need a number, try again")
         while True:
            exp_due = input("What date is the expense due? (mm/dd/YYYY) ")
            try:
                exp_date = datetime.strptime(exp_due, "%m/%d/%Y").date()
                break
            except ValueError:
                print("this is an invalid date try again")
                
         while True:
            efreq = input("Is this expense monthly, weekly, or biweekly? ").lower()
            if efreq in ["monthly", "weekly", "biweekly"]:
                break
            else:
                print("Invalid answer can you put weekly or monthly")
         while True:
            ecategory = input("Is this fixed or unfixed? ").lower()
            if ecategory in ["fixed", "unfixed"]:
                break
            else:
                print("This is an invalid answer can you put either fixed or unfixed")
         
            
         expense_list.append([qename,efreq,expense, exp_date, ecategory])
def results(income_list,expense_list):
    total_weekly_income = 0
    total_monthly_income = 0
    expense_total_weekly = 0
    expense_total_monthly = 0
    Weekly_Set_Aside = 0
    for name, price, freq in income_list:
        weekly, monthly = convert_amount(price, freq)
        total_weekly_income += weekly
        total_monthly_income += monthly
        print(f"""
Income: {name}
Amount: ${price:.2f}
Frequency: {freq}""")
    expense_list.sort(key=lambda x: x[3])
    for name, freq, exp, due_date, ecategory in expense_list:
        weekly, monthly = convert_amount(exp, freq)
        expense_total_weekly += weekly
        expense_total_monthly += monthly
        days_due = days_till_due(due_date)
        ppw = pay_per_week(days_due, exp)
        if ppw == None:
            ppw = exp
        Weekly_Set_Aside += ppw
        print(f"""
Expense: {name}
Amount: ${exp:.2f}
Due Date: {due_date}
Fixed/Unfixed: {ecategory}
Recurring: {freq}
{due_message(days_due)}""")
    return (total_weekly_income, total_monthly_income, expense_total_monthly,
expense_total_weekly,
Weekly_Set_Aside)
            
def Savings_menu():
    while True:
        try:
            savings = int(input("How much would you like to put towards savings. 25%, 50%, or 75%? "))
            if savings in [25, 50, 75]:
                savings_rate = savings / 100
                break
            else:
                print("I need a value of either 25, 50, or 75")
        except ValueError:
            print("put either 25, 50 or 75")
    return savings_rate
def compute_totals(income_list, expense_list):
    total_weekly_income = 0
    total_monthly_income = 0
    expense_total_weekly = 0
    expense_total_monthly = 0
    Weekly_Set_Aside = 0
    for name, price, freq in income_list:
        weekly, monthly = convert_amount(price, freq)
        total_weekly_income += weekly
        total_monthly_income += monthly

    for name, freq, exp, due_date, ecategory in expense_list:
        weekly, monthly = convert_amount(exp, freq)
        expense_total_weekly += weekly
        expense_total_monthly += monthly

        days_due = days_till_due(due_date)
        ppw = pay_per_week(days_due, exp)
        if ppw is None:
            ppw = exp

        Weekly_Set_Aside += ppw

    return total_weekly_income, total_monthly_income, expense_total_monthly, expense_total_weekly, Weekly_Set_Aside

        
def Summary_menu(income_list, expense_list, savings_rate):
    (total_weekly_income,
     total_monthly_income,
     expense_total_monthly,
     expense_total_weekly,
     Weekly_Set_Aside) = compute_totals(income_list, expense_list)
    Weekly_available_money = max(0,total_weekly_income - Weekly_Set_Aside)
    weekly_savings = money_savings(savings_rate, Weekly_available_money)
    Rem_available_weekly = max(0,Weekly_available_money - weekly_savings)
    Rem_bal_monthly = max(0,total_monthly_income - expense_total_monthly)
    monthly_savings = money_savings(savings_rate, Rem_bal_monthly)
    Rem_available_monthly = max(0,Rem_bal_monthly - monthly_savings)
    print(f"""
Summary Budget
Weekly Income: ${total_weekly_income:.2f}
Weekly Set Aside: ${Weekly_Set_Aside:.2f}
Weekly Savings: ${weekly_savings:.2f}
Weekly spending: ${Rem_available_weekly:.2f}
Monthly Income: ${total_monthly_income:.2f}
Monthly Expenses: ${expense_total_monthly:.2f}
Monthly Savings: ${monthly_savings:.2f}
Monthly Spending: ${Rem_available_monthly:.2f}
""")
while True:
    Menu = input("""
1) Add Income
2) Add Expenses
3) Show Results
4) Show Summary
5) Savings Rate                 
6) Quit
""").strip()
    if Menu == "1":
        income_menu(income_list)
        pass
    elif Menu == "2":
        expense_menu(expense_list)
        pass
    elif Menu == "3":
        (total_weekly_income, total_monthly_income, expense_total_monthly,
expense_total_weekly,
Weekly_Set_Aside) = results(income_list, expense_list)
        pass
    elif Menu == "4":
        Summary_menu(income_list, expense_list, savings_rate)
        pass
    elif Menu == "5":
        savings_rate = Savings_menu()
        pass
    elif Menu == "6":
        break
    else:
        print("pick 1-6")

