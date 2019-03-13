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

#---主要想法為number_card有{Basic, Normal, Silver, Gold}四項，故找三個
#---節點分為四群，每群至少有15個數，並找出能讓每群的值最大為最佳解，
#---值=max(G1)/sum(G1)+max(G2)/sum(G2)+max(G3)/sum(G3)+max(G4)/sum(G4)
def classifyAge(age, member_card):
    G1, G2, G3, G4 =[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]
    Large = [0, 0, 0]
    check = 0.0
    for i in range(len(age)):
        print(age)
        print(age.sort())
        # print(element)
        if age[i] > 0:
            second_min = age[i]
            print(second_min)
            break

    for N1 in age:
        for N2 in age:
            for N3 in age:
                if N1 > N2> N3 and N1 < max(age) and N3 > second_min and N3 != -1:
                    print("N1:", N1, " N2:", N2, " N3:", N3)
                    for i in range(len(age)):
                        if age[i] >= N1:
                            if member_card[i] == "Basic":
                                G1[0] += 1
                            elif member_card[i] == "Normal":
                                G1[1] += 1
                            elif member_card[i] == "Silver":
                                G1[2] += 1
                            else:
                                G1[3] += 1

                        if age[i] < N1 and age[i] >= N2:
                            if member_card[i] == "Basic":
                                G2[0] += 1
                            elif member_card[i] == "Normal":
                                G2[1] += 1
                            elif member_card[i] == "Silver":
                                G2[2] += 1
                            else:
                            	G2[3] += 1
                        if age[i] < N2 and age[i] >= N3:
                            if member_card[i] == "Basic":
                                G3[0] += 1
                            elif member_card[i] == "Normal":
                                G3[1] += 1
                            elif member_card[i] == "Silver":
                                G3[2] += 1
                            else:
                            	G3[3] += 1
                        if age[i] < N3 and age[i] > 0:
                            if member_card[i] == "Basic":
                                G4[0] += 1
                            elif member_card[i] == "Normal":
                                G4[1] += 1
                            elif member_card[i] == "Silver":
                                G4[2] += 1
                            else:
                            	G4[3] += 1
                    print(G1, G2, G3, G4, max(G1)/sum(G1), max(G2)/sum(G2), max(G3) /sum(G3), max(G4)/sum(G4), max(G1)/sum(G1)+max(G2)/sum(G2)+max(G3)/sum(G3)+max(G4)/sum(G4))
                    if (max(G1)/sum(G1)+max(G2)/sum(G2)+max(G3)/sum(G3)+max(G4)/sum(G4)) > check:
                        Large = [N1, N2, N3]
                        check = max(G1)/sum(G1)+max(G2)/sum(G2)+max(G3)/sum(G3)+max(G4)/sum(G4)
                    G1, G2, G3, G4 =[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] 
    print(Large, check)



D, M, NC, MC, A, YI = read('training.txt')
c = classifyAge(A, MC)
