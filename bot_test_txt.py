import os
import csv



test_dict = {}

if os.path.exists('test.csv'):
    # initialize the dictionaries to be empty
    with open('test.csv', 'r') as f:
        content = csv.reader(f)
        for row in content:
            # print(row)
            key = row[0]
            test_dict[key] = row[1]
print(test_dict)

a = ['a', 'b', 'c', 'd']
b = [5, 6, 7, 8]


count = 0
for l in a:
    test_dict[l] = b[count]
    count += 1

with open('test.csv', 'w') as f:
    for key in test_dict.keys():
        f.write("{},{}\n".format(key, test_dict[key]))

print(test_dict)