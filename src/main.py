# -*- encoding: utf-8 -*-

from unidecode import unidecode

file_messages = '../data/exemplo.txt'
file_dataset  = '../data/Produtos.csv'
file_result   = '../result/result.csv'


def clear_string(f_str):
    import re

    # Apply lower case to all words and remove accents and "ç"
    f_str = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", unidecode(f_str.lower()))

    # Padronize metrics
    if (' unidades' in f_str):
        f_str = f_str.replace(' unidades',' und')
    if (' unidade' in f_str):
        f_str = f_str.replace(' unidade',' und')
    if (' macos' in f_str):
        f_str = f_str.replace(' macos',' mc')
    if (' maco' in f_str):
        f_str = f_str.replace(' maco',' mc')
    if (' duzias' in f_str):
        f_str = f_str.replace(' duzias',' dz')
    if (' duzia' in f_str):
        f_str = f_str.replace(' duzia',' dz')
    if (' gramas' in f_str):
        f_str = f_str.replace(' gramas',' g')
    if (' grama' in f_str):
        f_str = f_str.replace(' grama',' g')
    if (' quilos' in f_str):
        f_str = f_str.replace(' quilos',' kg')
    if (' quilo' in f_str):
        f_str = f_str.replace(' quilo',' kg')
    if (' kg' in f_str):
        f_str = f_str.replace(' kg','kg')
    if ('1/2kg' in f_str):
        f_str = f_str.replace('1/2kg','500g')
    # Remove punctation marks, hifens and percentages
    if (',' in f_str):
        f_str = f_str.replace(',',' ')
    if ('.' in f_str):
        f_str = f_str.replace('.',' ')
    if ('-' in f_str):
        f_str = f_str.replace('-',' ')
    if ('–' in f_str):
        f_str = f_str.replace('–',' ')
    if ('%' in f_str):
        f_str = f_str.replace('%',' ')
    # Remove stopwords
    if (' de ' in f_str):
        f_str = f_str.replace(' de ',' ')
    if (' e ' in f_str):
        f_str = f_str.replace(' e ',' ')
    if (' com ' in f_str):
        f_str = f_str.replace(' com ',' ')
    if (' em ' in f_str):
        f_str = f_str.replace(' em ',' ')
    # Remove double spaces
    while ('  ' in f_str):
        f_str = f_str.replace('  ',' ')
    # Remove plural
    f_str = f_str.split(' ')
    for i in range(len(f_str)):
        if (len(f_str[i]) < 1): continue
        if (f_str[i][-2:] == 'ns'): f_str[i] = f_str[i][:-2] + 'm'
        elif(f_str[i][-1] == 's'): f_str[i] = f_str[i][:-1]
    f_str = ' '.join(f_str)

    return f_str

# Read data/examplo.txt
def read_messages():
    # Split between each client
    with open(file_messages,'r') as f:
        f_str = f.read().split("\n\n")
        f.close()
    # Fix \n bug: \n is missing
    for i in range(len(f_str)):
        id = ''
        j  = 0
        while(f_str[i][j].isdigit()):
            id += f_str[i][j]
            j += 1
        if (id == ''): continue
        id_next = str(int(id) + 1)
        if ('\n'+id_next+'.' in f_str[i]):
            f_str[i] = f_str[i].replace('\n'+id_next,'\n\n'+id_next)
            f_str[i] = f_str[i].split('\n\n')
    aux = []
    for x in f_str:
        aux += x if type(x) == list else [x]
    f_str = aux[:]
    #print(f_str)
    #exit(-1)

    # Clear string
    for i in range(len(f_str)):
        f_str[i] = clear_string(f_str[i]).split('\n')
    f_str[-1].pop(-1)

    # Fix \n bug: there is a \n in a wrong place
    i = 0
    len_f_srt = len(f_str)
    while (i < len_f_srt):
        if (len(f_str[i]) == 1):
            f_str[i] = f_str[i] + f_str[i+1]
            f_str.pop(i+1)
            len_f_srt = len(f_str)
        i += 1

    return f_str

# Read data/Produtos.csv
def read_dataset():
    # Split between each product
    with open(file_dataset,'r') as f:
        f_str = f.read().split('"\n"')
        f_str[-1] = f_str[-1][:-2]
        f.close()

    for i in range(len(f_str)):
        # Split the fields in csv file
        f_str[i] = f_str[i].split('","')
        # Remove information between parenthesis
        if ('(' in f_str[i][1]):
            idx_start = f_str[i][1].find('(')
            idx_end = f_str[i][1].find(')') + 1
            f_str[i][1] = f_str[i][1][:idx_start] + f_str[i][1][idx_end:]
        # Clear string
        f_str[i][1] = clear_string(f_str[i][1])
    f_str = f_str[1:]

    # Order dataset by description size
    for i in range(len(f_str)):
        for j in range(len(f_str[i:])):
            if (f_str[j][1] > f_str[i][1]):
                aux      = f_str[i]
                f_str[i] = f_str[j]
                f_str[j] = aux

    return f_str

# Find the product description that matches with the order
def compare_strings(messages, dataset, dict_words):
    matches = []

    # Run over all oreders
    for message in messages:
        customer = message[0]
        for order in message[1:]:
            order_list = order.split()
            min_appears = [100,100,100]
            words_min_appears = ['','','']
            for w in order_list:
                if (w not in dict_words.keys()): continue
                # Check the frequency of each word, looking for the three least frequent
                if (dict_words[w] < min_appears[0]):
                    words_min_appears[0] = w
                    min_appears[0] = dict_words[w]
                elif (dict_words[w] < min_appears[1]):
                    words_min_appears[1] = w
                    min_appears[1] = dict_words[w]
                elif (dict_words[w] < min_appears[2]):
                    words_min_appears[2] = w
                    min_appears[2] = dict_words[w]
            # If no matches...
            if (words_min_appears[0] == ''):
                matches.append([customer,order,'Pedido não recohecido','NENHUM','0'])
                break
            # If match...
            for d in dataset:
                if all(w in d[1] for w in words_min_appears):
                    matches.append([customer,order,d[1],d[0],d[2]])
                    break
    return matches

# Create the word frequency dictionary
def count_words(dataset):
    from collections import Counter

    all_words = ''
    for i in range(len(dataset)):
        all_words += dataset[i][1] + ' '
    all_words = ''.join([i for i in all_words if not i.isdigit()])
    all_words = all_words.split()

    # Remove unnecessary words
    dict_words = dict(Counter(all_words))
    dict_words.pop('und')
    dict_words.pop('kg')
    dict_words.pop('gr')
    dict_words.pop('dz')
    dict_words.pop('mc')
    dict_words.pop('ml')
    dict_words.pop('g')

    return dict_words

# Create the result file
def generate_spreadsheet(matches):
    # Insert the header
    str_result = '"id_cliente","nome_cliente","desc_pedido","desc_estoque","fornecedor","preco","quantidade_solicitada","total"\n'
    for match in matches:
        # Get customer id and name
        customer = match[0]
        id_customer = customer.split()[0]
        name_customer = ' '.join(w for w in customer.split()[1:])

        # Get order description, stock description and price
        desc_order = match[1]
        desc_stock = match[2]
        supplier = match[3]
        price = match[4]

        # Get order quantity
        quantity = [int(s) for s in desc_order.split() if s.isdigit()]
        if ('1/2' in desc_order):  quantity.append(0.5)
        if (len(quantity) == 1):   quantity = quantity[0]
        elif (len(quantity) == 0): quantity = 1
        else:                      quantity = quantity[-1]
        if (str(quantity) in desc_stock): quantity = 1

        # Calc the price of the order
        total = "{:.2f}".format(float(quantity) * float(price.replace(',','.'))).replace('.',',')

        str_result += '"'+id_customer+'","'+name_customer+'","'+desc_order+'","'+desc_stock+'","'+supplier+'","'+price+'","'+str(quantity)+'","'+str(total)+'"\n'

    # Write in result/result.csv
    with open(file_result,'w') as f:
        f.write(str_result)
    f.close()

# Main function
def main():
    messages = read_messages()
    dataset  = read_dataset()
    dict_words = count_words(dataset)

    matches = compare_strings(messages, dataset, dict_words)

    generate_spreadsheet(matches)

if (__name__ == '__main__'):
    main()
