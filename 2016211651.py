import re

of = open('2016211651.txt','w+')
inf = open('corpus.txt','r')
lin = 0	#行号
max_len = 0	#全部的长度
p1 = r"(^因为|(?<=[^病])因为).+?所以"
p2 = r"[(].+?[)]"
#全部的部分计算最大长度
for eachline in inf:
    lin+=1
    tmp_span = (0,0)
    res = re.search(p1,eachline)
    while res:
        tmp_span = (tmp_span[1]+res.span()[0],tmp_span[1]+res.span()[1])
        max_len = tmp_span[1]-tmp_span[0] if tmp_span[1]-tmp_span[0] > max_len else max_len
        res = re.search(p1,eachline[tmp_span[1]:])
max_len = max_len+6

lin = 0
# of.write('-------------------------------------------------------------------\n')
tplt = "{0:<4}\t{1:{4}<6}\t*因为*\t{2:{4}<{5}}\t&所以&  {3:{4}<15}\n"
# of.write(tplt.format("行号", "前面三个字", "全部", "后面3个字(标点符号算一个字)", chr(12288), max_len))

inf.seek(0,0)
for eachline in inf:
    lin+=1
    tmp_span = (0,0)
    res = re.search(p1,eachline)
    res2 = re.search(p2,eachline)
    res3 = None
    if res2:#匹配括号
        res3 = re.search(p1,eachline[res2.span()[0]:res2.span()[1]])#匹配括号里面的因为所以
        if res3:
            of.write(tplt.format(lin,eachline[res2.span()[0]+res3.span()[0]-3:res2.span()[0]+res3.span()[0]],eachline[res2.span()[0]+res3.span()[0]+2:res2.span()[0]+res3.span()[1]-2],eachline[res2.span()[0]+res3.span()[1]:res2.span()[0]+res3.span()[1]+3],chr(12288),max_len))
            eachline1 = eachline[:res2.span()[0]]+eachline[res2.span()[1]:]
            res4 = re.search(p1,eachline1)#匹配除去括号的因为所以
            if res4:
                len2 = res2.span()[1]-res.span()[0]-6
                of.write(tplt.format(lin,eachline[0 if(res4.span()[0]<3) else res4.span()[0]-3:res4.span()[0]],eachline[res4.span()[0]+2:res4.span()[1]+len2-2],eachline[res4.span()[1]+len2:res4.span()[1]+len2+3 if res4.span()[1]+len2+3 < len(eachline) else len(eachline)-1],chr(12288),max_len))    
    while res:#匹配这一行所有因为所以
        if res3:
            break
        tmp_span = (tmp_span[1]+res.span()[0],tmp_span[1]+res.span()[1])
        of.write(tplt.format(lin,eachline[0 if(tmp_span[0]<3) else tmp_span[0]-3:tmp_span[0]],eachline[tmp_span[0]+2:tmp_span[1]-2],eachline[tmp_span[1]:tmp_span[1]+3 if tmp_span[1]+3 < len(eachline) else len(eachline)-1],chr(12288),max_len))
        res = re.search(p1,eachline[tmp_span[1]:])

# of.write('-------------------------------------------------------------------\n')
of.close()
inf.close()
# !cat 2016211651.txt