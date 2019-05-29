#二维字典，统计时对值+1处理
def add1(dict1,k1,k2):
    if k1 in dict1.keys():
        if k2 in dict1[k1].keys():
            dict1[k1][k2]+=1
        else:
            dict1[k1].update({k2:1})
    else:
        dict1.update({k1:{k2:1}})

#统计训练样本中词表
from zhon.hanzi import punctuation
f = open("corpus_for_ass2train.txt",'r')
#二维字典
bi_dict = {}
#词表
dictionary = set([])
for eachline in f:
    data = eachline.replace('\n','').split(' ')
    begin = True
    for i in range(len(data)-1):
        if begin and data[i] not in punctuation:
            add1(bi_dict,'start',data[i])
            begin = False
        else:
            if data[i+1] not in punctuation:
                if data[i] in punctuation:
                    begin = True
                else:
                    add1(bi_dict,data[i],data[i+1])
    for each in data:
        if each not in punctuation:
            dictionary.add(each)
f.close()

#统计二维字典每一行所有出现的次数，保存在字典的total中
sum1=0
for each2 in bi_dict['start'].keys():
    sum1+=bi_dict['start'][each2]
bi_dict['start'].update({'total':sum1})

for each in bi_dict.keys():
    sum1=0
    for each2 in bi_dict[each].keys():
        sum1+=bi_dict[each][each2]
    bi_dict[each].update({'total':sum1})




import copy
Max_length = 4
#递归寻找所有切分可能，并把所有切分可能保存在res二维列表里面
def qie(str1,last_str):
    if(str1 =='$'):
        if len(result)!=0:
            tmp = []
            len_result = len(result)-1
            tmp.append(result[len_result][0])
            find = result[len_result][1]
            for j in range(len_result,-1,-1):
                if(result[j][0]==find):
                    tmp.insert(0,result[j][0])
                    find = result[j][1]
                if find=='':
                    break;
            res.append(copy.deepcopy(tmp))


    length = len(str1) if len(str1) <= Max_length else Max_length
    for i in range(length,0,-1):
        if(str1[:i]) in dictionary:
            result.append([str1[:i],last_str])
            qie(str1[i:],str1[:i])


#找到所有切分可能中概率最大的那个
def get_max(list1):
    if len(list1)==0:
        return -1
    for each in list1:
        each.insert(0,'start')
    max_i = 0
    max_p = 0
    for i in range(len(list1)):
        p = 1
        for j in range(len(list1[i])-1):
            if list1[i][j] not in bi_dict.keys():
                p *= 1/len(dictionary)
            else:
                c = 1 if list1[i][j+1] not in bi_dict[list1[i][j]].keys() else 1+bi_dict[list1[i][j]][list1[i][j+1]]
                p *= c/(len(dictionary)+bi_dict[list1[i][j]]['total'])
        max_p = p if p > max_p else max_p
        max_i = i if p > max_p else max_i
    return list1[max_i]


#训练
i_f = open('corpus_for_ass2test.txt','r')
o_f = open('2016211651.txt','w')
for eachline in i_f:
    # print(eachline)
    while(True):
        i = 0#定位这段话的位置
        while((eachline[i] not in punctuation) and (eachline[i] != '\n')):
            i+=1
        sentense = eachline[:i]
        if len(sentense)<25:
            result = []
            res = []
            qie(sentense+'$','')
            max_res = get_max(res)
            if max_res != -1:
                max_res.pop(0)
                for each in max_res:
                    o_f.write(each+' ')
        else:
            result = []
            res = []
            qie(sentense[:25]+'$','')
            max_res = get_max(res)
            if max_res != -1:
                max_res.pop(0)
                for each in max_res:
                    o_f.write(each+' ')

            result = []
            res = []
            qie(sentense[25:]+'$','')
            max_res = get_max(res)
            if max_res != -1:
                max_res.pop(0)
                for each in max_res:
                    o_f.write(each+' ')
        # print(res)        
        while eachline[i] in punctuation:
        	o_f.write(eachline[i]+' ')
        	i+=1
        if(eachline[i] == '\n'):
            o_f.write('\n')
            break
            
        eachline = eachline[i:]
print('success!')
i_f.close()
o_f.close()