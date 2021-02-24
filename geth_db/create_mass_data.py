import csv
import random
import string
import pandas as pd


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


data = {}
amount = 100
for i in range(amount):
    guid = get_random_string(8)
    course = get_random_string(3)
    grade = get_random_string(2)

    data[guid] = [course, grade]

df = pd.DataFrame.from_dict({"guid": data.keys(), "grades": data.values()})
df.to_csv('{}guid.csv'.format(amount), index=False, header=False)
print(df.head())
