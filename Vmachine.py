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

def formatter (amount, notes, result = None):
    if amount < 0:
        return []
    result_notes = change(amount, notes, result=None)[1]
    
    change_given = []
    for note in result_notes:
        change_given.append(str(format(note /float(100), '.2f')))
    return change_given

def  add_change_log(code, input_val):
    notes_given = formatter(int(float(format(input_val - product[code]['price'], '.2f')) * 100), [1000, 500, 400, 200, 100, 50])
    
    change = [str(code).zfill(2), str(round(input_val, 2))]
    change.extend(notes_given)
    with open('changes.txt', 'a') as my_file:
        my_file.write(', '.join(change))
        my_file.write('\n')
        
def  add_product_log(code):
    product_log = [str(code).zfill(2), product[code]['Product-name'], product[code]['price'], (product[code]['count'])]
    with open('purchase_log.csv', 'a') as my_file:
        writer = csv.writer(my_file, dialect='excel')
        writer.writerow(product_log)

def add_price_log(code, input_val):
    notes_given = formatter(int(float(format(input_val - product[code]['price'], '.2f')) * 100), [1000, 500, 400, 200, 100, 50])
    for note in notes_given:
        price_log = [note, price['NGN'][note]]
        with open('price_log.csv', 'a') as my_file:
            writer = csv.writer(my_file)
            writer.writerow(price_log)

def add_price_log_1():
    with open('price_log.csv', 'a') as my_file:
        writer = csv.writer(my_file)
        for row in sorted(price['NGN'].iteritems()):
            writer.writerow(row)

def note_check(code, input_val):
    change_given = format(input_val - product[code]['price'], '.2f')
    note_list = price['NGN'].keys()
    if ((change_given in note_list or change_given == 0.0) and change_given != '0.0'):
        note_count = price['NGN'][change_given]
        if note_count > 1 or change_given == '0.0':
            print(change_given, 'Exact Change cannot be ruturned')
        else:
            print(change_given)
    else:
        print(change_given)


def purchase_test(code, input_val):
    if code in product:
        