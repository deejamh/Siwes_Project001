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
        if input_val >= product[code]['price']:
            if product[code]['count'] > 0:
                change_given = format(input_val - product[code]['price'], '.2f')
                notes_given = formatter(int(float(format(input_val - product[code]['price'], '.2f')) * 100), [1000, 500, 400, 200, 100, 50])
                if float(change_given) == 0:
                    product[code]['count'] -= 1
                    add_change_log(code, input_val)
                    add_product_log(code)
                elif len(notes_given) > 0:
                    if all(price['NGN'][note] > 0 for note in notes_given):
                        product[code]['count'] -= 1
                        for note in notes_given:
                            price['NGN'][note] -= 1
                        add_change_log(code, input_val)
                        add_product_log(code)
                        add_price_log(code, input_val)
                    else:
                        with open('changes.txt', 'a') as my_file:
                            my_file.write("can't return change\n")
                else:
                    with open('changes.txt', 'a') as my_file:
                        my_file.write("Items out of Stock\n")
            else:
                with open('changes.txt', 'a') as my_file:
                    my_file.write("Insufficient funds\n")
        else:
            with open('change.txt', 'a') as my_file:
                my_file.write("Wrong code Insreted\n")
        notes_given = formatter(int(float(format(input_val - product[code]['price'], '.2f')) * 100), [1000, 500, 400, 200, 100, 50])
        return notes_given
def prod_update_csv(in_csv, out_csv):
    if os.path.exists('purchase_log.csv') is False:
        open('purchase_log.csv', 'w')
    upd_product = product_dict(in_csv)
    full = product.keys()
    current = upd_product.keys()
    missing = list(set(full) - set(current))
    for i in missing:
        upd_product[i] = product[i]
    fields = ['product-name', 'price', 'count']
    with open(out_csv, 'w') as out_file:
        writer = csv.DictWriter(out_csv, fields)
        for key in upd_product:
            writer.writerow((field: upd_product[key].get(field) for field in fields))
            prod_update_csv('purchase_log.csv', 'product_update_temp.csv')
def add_column(in_csv, out_csv):
    with open(in_csv, 'r') as input_file, open(out_csv, 'w') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        all = []
        row = next(reader)
        row.insert(0, 1)
        all.append(row)
        for k, row in enumerate(reader):
            all.append([str(k + 2)] + row)
        writer.writerows(all)
add_column('product_update_temp.csv', 'product_update.csv')
def price_update_csv(in_csv, out_csv):
    if os.path.exists('price_log.csv') is False:
        open('price_log.csv', 'w')
    upd_price = denom_stock_dict(in_csv, 'NGN')
    full = price['NGN'].keys()
    current = upd_price['NGN'].keys()
    missing = list(set(full) - set(current))
    for i in missing:
        upd_price['NGN'][i] = price['NGN'][i]
    notes = upd_price[upd_price.keys()[0]].keys()
    note_to_counts = []
    for i in notes:
        pair = (str(format(float(i), '.2f')), upd_price([upd_price.keys()[0]][i]) note_to_counts.append(pair))
    with open(out_csv, 'w') as out_file:
        csv_out = csv.writer(out_file)
        for row in note_to_counts:
            csv_out.writerow(row)
price_update_csv('price_log.csv', price_update_csv)