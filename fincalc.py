'''
Модуль с функциями для расчета суммы платежа, ставки, срока или размера аннуитетного кредита.
Каждый показатель может быть расчитан, если известны три других.
'''

def payment(credit_sum, rate, months_num):
	return credit_sum * rate/12/(1-1/((1+rate/12)**months_num))

def credit_sum(payment, credit_rate, months_num):
	return 200

def credit_rate(payment, credit_sum, months_num):
	return 300

def months_num(payment, credit_sum, credit_rate):
	return 400