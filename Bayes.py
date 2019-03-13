import numpy
import random
import math


def read(datafile):
    #-----讀檔，整理資料
    raw = []
    datas, temp_datas = [], []
    crimefile = open(datafile, 'r')
    for line in crimefile.readlines():
        raw.append((line.replace(" ", ","))[1:-2].split(","))

    #datas = numpy.zeros((len(raw),5),int)
    datas = [[" " for m in range(5)] for n in range(len(raw))]

    for i in range(len(raw)):
        for j in range(9):
            if j == len(raw[i]):
                break
            else:
                if (j % 2) == 0:
                    if raw[i][j] == "0" or raw[i][j] == "2":
                        datas[i][int(raw[i][j])] = raw[i][j + 1]
                    else:
                        datas[i][int(raw[i][j])] = int(raw[i][j + 1])
                
    for i in range(len(raw)):
        if datas[i][2] == " ":
            datas[i][2] = "Basic"
        if datas[i][3] == ' ':
            datas[i][3] = -1

    marital_status, num_children_at_home, member_card, age, year_income = [], [], [], [], []
    for element in datas[:]:
        marital_status.append(element[0])
        num_children_at_home.append(element[1])
        member_card.append(element[2])
        age.append(element[3])
        year_income.append(element[4])

    return datas, marital_status, num_children_at_home, member_card, age, year_income


def classifyAge(age):
    #-----轉換屬量資料，透過附件(classify.py)找出節點
    new_age = [" " for m in range(len(age))]
    #print(age)
    for i in range(len(age)):
        if age[i] < 45:
            new_age[i]="A"
        elif age[i] <57 and age[i] >= 45:
            new_age[i]="B"
        elif age[i] <79 and age[i] >= 57:
            new_age[i]="C"
        elif age[i] <100 and age[i] >= 79:
            new_age[i]="D"
    #print(new_age)
    return new_age

#######################################################################################################
def count1(DB, CountObject):
    c=0
    for i in range(len(DB)):
        if DB[i] == CountObject :
            c+=1
    #print(CountObject, c)
    return c
def count2(E, H, CountObjectE, CountObjectH):
    c=0
    for i in range(len(E)):
        if E[i] == CountObjectE and H[i] == CountObjectH:
            c+=1
    #print(CountObjectE, CountObjectH, c)
    return c 

def getConditionProb(evidence, hypothesis):
    array_H, array_E = [], []
    for element in hypothesis:
        #print(element)
        if element not in array_H and element!=" ":
            array_H.append(element)
    for element in evidence:
        #print(element)
        if element not in array_E and element!=" ":
            array_E.append(element)
    #print(array_H, array_E)
    #print(len(array_H), len(array_E)) 
    conditionProb = [[" " for m in range(3)] for n in range(len(array_H)*len(array_E))]
    #print(len(conditionProb))
    i=0
    for elementH in array_H:
        for elementE in array_E:
            conditionProb[i][0]=elementE
            conditionProb[i][1]=elementH
            conditionProb[i][2]=float(count2(evidence, hypothesis, elementE, elementH)/count1(hypothesis, elementH))
            i+=1
    #print(conditionProb)
    return conditionProb

def getPriorProb(hypothesis):
    #-----計算priorProb
    array_H=[]
    for element in hypothesis:
        #print(element)
        if element not in array_H and element!=" ":
            array_H.append(element)
    priorProb = [[" " for m in range(2)] for n in range(len(array_H))]
    i=0
    for elementH in array_H:
        priorProb[i][0]=elementH
        priorProb[i][1]=float(count1(hypothesis, elementH)/len(hypothesis))
        #print(elementH, conditionProb[i][0],conditionProb[i][1])
        i+=1
    return priorProb

def getPosteriorProb(conditionProb, priorProb):
    #-----先計算jointConditionProb
    jointConditionProb = [[" " for m in range(6)] for n in range(1280)]
    j=0
    #print(jointConditionProb)
    member_card=["Basic", "Normal", "Silver", "Gold"]
    marital_status = ["S", "M"]
    num_children_at_home = [1,2,3,4,5]
    age=["A","B","C","D"]
    year_income = [20000,40000,60000,80000,100000,120000,140000,160000]


    for elementMC in member_card:
        for elementM in marital_status:
            for elementNC in num_children_at_home:
                for elementA in age:
                    for elementYI in year_income:
                        #print(j, elementMC, elementM, elementNC, elementA, elementYI)
                        jointConditionProb[j][0] = elementMC
                        jointConditionProb[j][1] = elementM
                        jointConditionProb[j][2] = elementNC
                        jointConditionProb[j][3] = elementA
                        jointConditionProb[j][4] = elementYI
                        jointConditionProb[j][5] = 1
                        j+=1

    for elementMC in member_card:
        for elementM in marital_status:
            for i in range(len(conditionProb)):
                for j in range(len(jointConditionProb)):
                    if conditionProb[i][0]==elementM and conditionProb[i][1] == elementMC and jointConditionProb[j][0] == elementMC and jointConditionProb[j][1] ==elementM:
                        jointConditionProb[j][5]*=conditionProb[i][2]
    for elementMC in member_card:
        for elementNC in num_children_at_home:
            for i in range(len(conditionProb)):
                for j in range(len(jointConditionProb)):
                    if conditionProb[i][0]==elementNC and conditionProb[i][1] == elementMC and jointConditionProb[j][0] == elementMC and jointConditionProb[j][2] ==elementNC:
                        jointConditionProb[j][5]*=conditionProb[i][2]
    for elementMC in member_card:
        for elementA in age:
            for i in range(len(conditionProb)):
                for j in range(len(jointConditionProb)):
                    if conditionProb[i][0]==elementA and conditionProb[i][1] == elementMC and jointConditionProb[j][0] == elementMC and jointConditionProb[j][3] ==elementA:
                        jointConditionProb[j][5]*=conditionProb[i][2]
    for elementMC in member_card:
        for elementYI in year_income:
            for i in range(len(conditionProb)):
                for j in range(len(jointConditionProb)):
                    if conditionProb[i][0]==elementYI and conditionProb[i][1] == elementMC and jointConditionProb[j][0] == elementMC and jointConditionProb[j][4] ==elementYI:
                        jointConditionProb[j][5]*=conditionProb[i][2]
    #print(jointConditionProb)
    #-----再計算posteriorProb
    posteriorProb = jointConditionProb
    for elementM in marital_status:
        for elementNC in num_children_at_home:
            for elementA in age:
                for elementYI in year_income:
                    for elementMC in member_card:
                        for i in range(len(posteriorProb)):
                            for j in range(len(priorProb)):
                                if posteriorProb[i][1]==elementM and posteriorProb[i][2]==elementNC and posteriorProb[i][3]==elementA and posteriorProb[i][4]==elementYI and posteriorProb[i][0]==elementMC and priorProb[j][0]==elementMC:
                                    posteriorProb[i][5] *= priorProb[j][1]
    temp_value = [[" " for m in range(5)] for n in range(320)]
    for i in range(len(temp_value)):
        temp_value[i][4] =0.0

    j=0
    for elementM in marital_status:
        for elementNC in num_children_at_home:
            for elementA in age:
                for elementYI in year_income:
                    for i in range(len(posteriorProb)):
                        if posteriorProb[i][1]==elementM and posteriorProb[i][2]==elementNC and posteriorProb[i][3]==elementA and posteriorProb[i][4]==elementYI:
                            temp_value[j][0] = elementM
                            temp_value[j][1] = elementNC
                            temp_value[j][2] = elementA
                            temp_value[j][3] = elementYI
                            temp_value[j][4] += posteriorProb[i][5]
                    j+=1

    for elementM in marital_status:
        for elementNC in num_children_at_home:
            for elementA in age:
                for elementYI in year_income:
                    for elementMC in member_card:
                        for j in range(len(temp_value)):
                            for i in range(len(posteriorProb)):
                                if posteriorProb[i][1]==elementM and posteriorProb[i][2]==elementNC and posteriorProb[i][3]==elementA and posteriorProb[i][4]==elementYI and posteriorProb[i][0]==elementMC and temp_value[j][0]==elementM and temp_value[j][1]==elementNC and temp_value[j][2]==elementA and temp_value[j][3]==elementYI: 
                                    posteriorProb[i][5] /= temp_value[j][4]
    #print(posteriorProb)

    return posteriorProb
##########################################################################################################################
def getRule(posteriorProb):
    #-----取得CLass Rule
    member_card=["Basic", "Normal", "Silver", "Gold"]
    marital_status = ["S", "M"]
    num_children_at_home = [1,2,3,4,5]
    age=["A","B","C","D"]
    year_income = [20000,40000,60000,80000,100000,120000,140000,160000]

    Rule = [[" " for m in range(5)] for n in range(320)]
    largeNum = 0.0
    largeMC = " "
    j=0
    for elementM in marital_status:
        for elementNC in num_children_at_home:
            for elementA in age:
                for elementYI in year_income:
                    for i in range(len(posteriorProb)):
                        if posteriorProb[i][1]==elementM and posteriorProb[i][2]==elementNC and posteriorProb[i][3]==elementA and posteriorProb[i][4]==elementYI:
                            if posteriorProb[i][5] > largeNum:
                                largeNum = posteriorProb[i][5]
                                largeMC = posteriorProb[i][0]
                    Rule[j][0]=elementM
                    Rule[j][1]=elementNC
                    Rule[j][2]=elementA
                    Rule[j][3]=elementYI
                    Rule[j][4]=largeMC
                    largeNum = 0.0
                    largeMC = " "
                    j+=1
    #print(Rule)
    return Rule

def classifier(Rule, File):
    #-----用training data訓練之分類器
    marital_status = ["S", "M"]
    num_children_at_home = [1,2,3,4,5]
    age=["A","B","C","D"]
    year_income = [20000,40000,60000,80000,100000,120000,140000,160000]

    testDB, testM, testNC, testMC, testA, testYI = read(File)
    testA = classifyAge(testA)
    testData = [[" " for m in range(5)] for n in range(len(testDB))]
    for i in range(len(testDB)):
        testData[i][0] = testM[i]
        testData[i][1] = testNC[i]
        testData[i][2] = testA[i]
        testData[i][3] = testYI[i]

    
    for i in range(len(testData)):
        for j in range(len(Rule)):
            if testData[i][0]==Rule[j][0] and testData[i][1]==Rule[j][1] and testData[i][2]==Rule[j][2] and testData[i][3]==Rule[j][3]:
                testData[i][4] = Rule[j][4]
    accumRule=[]        
    for i in range(len(testData)):
    	if testData[i][4]==" ":
            for j in range(len(Rule)):
                if testData[i][0]==Rule[j][0] or testData[i][1]==Rule[j][1] or testData[i][2]==Rule[j][2] or testData[i][3]==Rule[j][3]:
                    accumRule.append(Rule[j][4])
            testData[i][4] = max(accumRule, key=accumRule.count)
            accumRule=[]
    
    writefile=open('Output Result.txt', 'w')
    for i in range(len(testData)):
        writefile.write(str(testDB[i])+" member_card ="+testData[i][4])
        writefile.write('\r\n')


    return(testData)


###------------main------------###
D, M, NC, MC, A, YI = read('training.txt')
A = classifyAge(A)

#-----conditionProb--------
conditionProb = []
temp = getConditionProb(M, MC)
for set in temp:
    conditionProb.append(set)
temp = getConditionProb(NC, MC)
for set in temp:
    conditionProb.append(set)
temp = getConditionProb(A, MC)
for set in temp:
    conditionProb.append(set)
temp = getConditionProb(YI, MC)
for set in temp:
    conditionProb.append(set)
#print(conditionProb)

#-----priorProb------------
priorProb=[]
priorProb = getPriorProb(MC)
#print(priorProb)

#-----posteriorProb---------
posteriorProb=[]
posteriorProb = getPosteriorProb(conditionProb, priorProb)

#-----rule---------------
rule=[]
rule = getRule(posteriorProb)

#-----classifier---------
result=[]
result=classifier(rule, 'test.txt')

#print(result)