# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 14:59:38 2018
尋找基因碼
@author: 21068X010 王靖瑤
"""
#define-------------------------
start_key="ATG"
end_key=["TAA","TAG","TGA"]
words=["A","T","G","C"]#染色體以ATGC四個字母（核苷酸）序列來建構
result_key=[]#最後的結果
#end---------------------
#1.操作者輸入染色體基因序列
mainstring=input("Enter a Chromosome string:")
mainstring=str.upper(mainstring)  
nowstart_index=0;
lastend_index=0;
group_count=0;#基因組數
#找出起始碼
def find_s(i_startindex):
    index=mainstring.find(start_key,i_startindex)
    return index;
#找出終點碼
def find_e(i_startindex):
    index=-1;
    for e_s in end_key:
        index=mainstring.find(e_s,i_startindex)
        if(index!=-1):
            break
        
    return index;
#印出搜尋結果    
def print_result():
    if(len(result_key)>0):
        print(result_key)
    else:
        print("no gene is found")
#2.染色體基因序列中基因數目判斷
    #不滿3的倍數輸入，直接以找不到基因回應
if(len(mainstring)%3!=0 and len(mainstring)>=9):
#    print("no gene is found:","基因數非3的倍數或未大於9個基因數")
    print_result()
    #只有A、T、G、C 才是合理的染色體基因序列
elif (all(x in words for x in mainstring)==False):
#    print("no gene is found:","只能輸入A、T、G、C四種基因碼")
    print_result()
else:

    while(lastend_index+9<=len(mainstring)):
        temp_start_index=-1
        #3.找出起點             
        lastend_index=find_s(nowstart_index)
        if(lastend_index>-1):
#            print("找到起點:起->%d"%(lastend_index))
            #4.找到起點, 開始找終點
            nowstart_index=lastend_index+3
            lastend_index=nowstart_index
            #後續基因數目不足，一定找不到終點
            if(nowstart_index>=len(mainstring)):
#                print("no gene is found")
                break
            lastend_index=find_e(nowstart_index)
            #找到終點後，剩餘基因數>=7(3個起點碼，3個終點碼，3碼核苷酸)
            if(lastend_index>-1):
                if ((lastend_index-nowstart_index)%3==0) and (lastend_index-nowstart_index)>0:
                    #print("找到終點:起->%d 終->%d"%(nowstart_index,lastend_index))
                    group_count+=1
#                   print("第%d組基因碼:"%(group_count),mainstring[nowstart_index:lastend_index])
                    result_key.append(mainstring[nowstart_index:lastend_index])
                #基因數不足3倍數，此組不可使用(缺陷？)                
#                else:
#                    print("no gene is found:起->%d 終->%d :%s"%(nowstart_index,lastend_index,"基因數非3倍數"))

                nowstart_index=lastend_index+3
                lastend_index=nowstart_index
            else:
#                print("no gene is found:","找不到終點:起->%d"%(nowstart_index))
                break
         #5.找不到起點，結束迴圈，再見       
        else:
#             print("no gene is found:","找不到起點")
             break
    
    print_result()

#Test Case
#ATGAAATAA -->AAA
#TTATGATATAA-->ATA
#TATGGGGTAAAA-->GGG
#ATGAAATGATAA->AAATGA (有疑問)
#ATGAAATAAATGAAATAA-->AAA AAA
#TTATGATATAATTATGATATAA-->ATA ATA
#ATGAAATAATTATGATATAA-->AAA ATA
#ATGAAAAAAAGG -->no gene is found
#ATGAAATAATATGAAAAAAAGG -->AAA no gene is found
#ATGAAATAAATGTAG -->AAA no gene is found
#ATGAAATAAATGAAATAATAG-->AAA AAA
#ATGTAAATGAAAGGCTGA -->no gene is found AAAGGC