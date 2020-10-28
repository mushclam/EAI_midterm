import sys
from simpleError import *

class Knapsack:
    def __init__(self, filename):
        # filename: Save the input filename and use when open file.
        # dataset: Save the data in input file.
        # capacity: Save maximum weight capacity.
        self.filename = filename
        self.dataset = []
        self.capacity = 0

    def reader(self):
        # reader read dataset file and save dict [{item: , weight: , profit:}] in dataset list
        # dataset = [{item:value, weight:value, profit:value}, ...]
        try:
            f = open(self.filename, 'r')
            lines = f.readlines()

            # Check dataset
            if (lines[0].strip() != '0/1 knapsack problem specification'):
                raise DatasetError()
            else:
                print('0-1Knapsack Dataset is loaded!')
                lines.pop(0)

            # Check total weight capacity
            capacityFlag = False
            for line in lines:
                if 'Total weight capacity' in line:
                    _capacity = line.split(':')
                    self.capacity = int(_capacity[1].strip())
                    capacityFlag = True

                    print('Total weight capacity:', self.capacity)
                    break
            
            if not capacityFlag:
                raise CapacityNotExistError()

            # Data reading
            dataFlag = False
            flagInd = -1
            for index, line in enumerate(lines):
                if 'item' in line:
                    dataFlag = True
                    flagInd = index
                    
                    print('Dataset is loading...')
                    break
            
            if not dataFlag:
                raise DatasetError()

            index = 0
            while (index != flagInd):
                lines.pop(0)
                index += 1
            lines.pop(0)

            # Data load on dataset
            for line in lines:
                rawdata = line.split('\t')
                data = {'item':int(rawdata[0]), 'weight':int(rawdata[1]), 'profit':int(rawdata[2])}
                self.dataset.append(data)
            print(len(self.dataset), 'data are loaded!')

            f.close()

        except FileNotFoundError as e:
            print(e)
            sys.exit()

    def printDataset(self):
        # Print all data in dataset on standard output
        for data in self.dataset:
            print('item: %d, weight: %d, profit: %d'%(data['item'], data['weight'], data['profit']))