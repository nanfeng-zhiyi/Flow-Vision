import numpy as np

data = np.load('../dataset/PEMS/PEMS04/dataset.npz')

print(data.files)
arr = data['data']


print(arr.shape)
print(arr)
