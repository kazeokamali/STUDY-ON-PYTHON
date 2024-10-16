from email.message import tspecials

test_dic= {'name': 'Es','age':'15','height':'153' }
for key in test_dic:
    print(key)
    print(f'{key}:\t {test_dic[key]}')

print('name'in test_dic)
print('Es'in test_dic)
print('Es' in test_dic['name'])

print(test_dic.get('name') )
print(test_dic.keys() )
print( test_dic.values() )
print( test_dic.items() )

print(test_dic.pop('age') )
print( test_dic )

print( test_dic.popitem() )
print( test_dic )
