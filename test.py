import json
import numpy as np

with open('result_cp.json', 'r') as f:
    jsonDict = json.load(f)

result = jsonDict[-1]
cp_4 = np.array(result['pmx_cp-0.4'])
cp_7 = np.array(result['pmx_cp-0.7'])
# cp_9 = np.array(result['pmx'])
# oxcp_7 = np.array(result['pmx_cp-0.7'])

print('CP 0.4 mean:', cp_4.mean())
print('CP 0.4 std:', cp_4.std())

print('CP 0.7 mean:', cp_7.mean())
print('CP 0.7 std:', cp_7.std())

# print('CP 0.9 mean:', cp_9.mean())
# print('CP 0.9 std:', cp_9.std())

# print('OXCP 0.9 mean:', oxcp_7.mean())
# print('OXCP 0.9 std:', oxcp_7.std())