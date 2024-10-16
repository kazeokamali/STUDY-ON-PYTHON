content_p = input('随便输入文本')
letter_count = {}

for i in content_p:
    if 'A'<i < 'Z' or 'a' < i < 'z':
        letter_count[i] = letter_count.get( i,0 )+ 1
sort_con =sorted( letter_count, key = letter_count.get, reverse=True )

for key in sort_con:
    print(f'{key} \t appeared {letter_count[key]}')



stocks = {
    'AAPL': 191.88,
    'GOOG': 1186.96,
    'IBM': 149.24,
    'ORCL': 48.44,
    'ACN': 166.89,
    'FB': 208.09,
    'SYMC': 21.29
}
stocks2 = {key: value for key, value in stocks.items() if value > 100}
print(stocks2)