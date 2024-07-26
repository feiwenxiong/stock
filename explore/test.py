import random
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
from tqdm import tqdm
def kill():
    person_list = [i for i in range(1,601)]
    while len(person_list)>1:
        length = len(person_list)
        code = random.randint(0,length-1) + 1
        if code % 2 == 1:
            index = code - 1
            person_list.pop(index)
    return person_list[0]

max_list = []
for i in tqdm(range(1,100_0000)):
    value = kill()
    max_list.append(value)

#print(max_list)

max_dic = {}
for item in max_list:
    if item in max_dic:
        max_dic[item] += 1
    else:
        max_dic.update({item:1})

#print(max_dic)

def plot_pandas(data):
    df = pd.DataFrame.from_dict(data, orient='index')

    # 绘制条形图
    df.plot(kind='line')

    # 设置标题和轴标签
    plt.title('字典值条形图')
    plt.xlabel('字典键')
    plt.ylabel('字典值')

    # 显示图形
    plt.show()

#plot_pandas(max_dic)

def plot_pandas2(data):
    ordered_data = OrderedDict(sorted(data.items()))

    # 创建折线图
    plt.plot(ordered_data.keys(), ordered_data.values())

    # 设置标题和轴标签
    plt.title('字典值折线图')
    plt.xlabel('字典键')
    plt.ylabel('字典值')

    # 显示图形
    plt.show()

#print(max_dic)
plot_pandas2(max_dic)
