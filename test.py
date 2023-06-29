import json


my_list = [1, 2, 3, 4, 5]
with open('.env', 'r+') as f:
    list_str = json.dump(my_list, f)

print(list_str)
