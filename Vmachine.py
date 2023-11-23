import os
import csv
from random import randint, uniform

def curr_dict(currency_file):
    denomination = {}
    with open(currency_file, 'r') as my_file:
        reader = csv.reader(my_file)
        for row in  reader:
            value = []
            for column in row:
                value.append(column)
            denomination[row[0]] = value[1:]
    return denomination

def denom_stock_dict(stock_file, currency):
    denom_stock = {}
    
    with open(stock_file, 'r') as my_file:
        reader = csv.reader(my_file)
        for row in  reader:
            value = {}
            for row in reader:
                value[row[0]] = int(row[1])
            denom_stock[currency] = value
    return denom_stock

def product_dict(prod_file):
    products = {}
    
    with open(prod_file, 'r') as my_file:
        reader = csv.reader(my_file)
        for row in  reader:
            value = {}
            for column in row:
                value["Product-name"] = row[1]
                value["price"] = float(row[2])
                value["count"] = int(row[3])
                products[int(row[0])] = value
    return products

currency = curr_dict('currency.csv')
product = product_dict('products.csv')
price = denom_stock_dict('price.csv','NGN')

def change(amount, notes, result = None):
    result = [] if result is None else result
    if len(notes) == 0:
        return len(result), result
    
    max_note = max(notes)
    notes.remove(max_note)
    answer = amount // max_note
    if answer  == 0 and max_note < amount:
        result = result + ([max_note] * answer)
        return result
    else:
        result = result + ([max_note] * answer)
        return change(amount % max_note, notes, result)
    
note_list = [1000, 500, 400, 200, 100, 50]