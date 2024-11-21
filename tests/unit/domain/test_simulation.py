# class TestSimulationCase:
#     def test_create_age(self):

# Dataset
#     array[start_year:end_year]
#     - salarys
#     - - "id":[s:e]
#     - expenses
#     - - "id":[s:e]
#     - houses
#     - - "id":[s:e]
#     - childs
#     - - "id":[s:e]
#     - investments
#     - - "id":[s:e]
#     - left
#     - - "id":[s:e]

# Calc
# for i in [s:e]
#     salary_sum[i] - expense_sum[i] - house_sum[i] - child_sum[i] - risk*salary[i] = left[i]
#     left[i]*investment_rate = new_investment
#     for invest in investments[i]:
#         update_investment = investments*return_rate + new_investment * investment_distrubuted_ratio
#         invest[i+1] = update_investment
