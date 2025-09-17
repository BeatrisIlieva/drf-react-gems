dict = {'1': 1, '2': 2}
inputs = {'10': '1'}
res = {key: inputs.get(key, {}).get(key, "") for key in dict.keys()}
print(res)