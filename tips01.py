# #1 --------------------------------------------
# cities = ['Ivano-Frankivsk', 'Lviv', 'Kiyv']
# for i, city in enumerate(cities):
#     print(i, city)
# #2 --------------------------------------------
# mx= [1,7,9]
# my= [0,3,5]
# for x,y in zip(mx,my):
#     print(x,y,sep='|')
# #3 --------------------------------------------
# x = 10
# y = -10
# print('Before: a = %d, b = %d ' % (x,y))
# x , y = y , x
# print('After: a = %d, b = %d ' % (x,y))

# #4 --------------------------------------------
# ages = {
#     'Nata'.lower() : 31,
#     'Vova' : 40
# }

# age = ages.get('nata','Unknown')
# print('Aga is %s' % (age))

# #5 --------------------------------------------
# char = 'g'
# chars = ['a','g','t']
# for fchar in chars:
#     if char == fchar:
#         print('Found!')
#         break
# else: #if not break
#     print('Not found!')

# #6 --------------------------------------------
# f = open('config.ini')
# text = f.read()
# for line in text.split('/n'):
#     print(line)
# f.close()

##better
# with open('config.ini') as f:
#     for line in f:
#         print(line)

# #7 --------------------------------------------
# print('Start!')
# try:
#     print(int('1'))
# except:
#     print('Crash!')
# else: #in no-exception
#     print('Converse ok!')
# finally: #always
#     print('Final!')
# print('Done!')

# def addCommand(st, data):
#     try:
#         ind0 = st.find('(')
#         ind1 = st.find(')')
#         if ind0 == -1 or ind1 == -1:
#             raise Exception('has no ()')
#         print(ind0, ind1)
#         stCommand = st[0:ind0].strip()
#         stData = [el.strip() for el in st[ind0+1:ind1].strip().split(',')]
#         print(stCommand)
#     except Exception as e:
#         data.append('Error')
#         data.append(str(e))
#     else:
#         data.append(stCommand)
#         data.append(stData)


# mas = []
# addCommand('TimeWait (16000, 20000   , Try and     )', mas)
# addCommand('TimeWait 16000, 20000   , Try and     )', mas)
# print(mas)

def isText(text,searches):
    for search in searches.split(';'):
        if search.strip() in text:
            return True
    return False

print(isText('Proba find text','Proba1;   find'))

must be: You need: You will want: improved :You improve :needs to be
