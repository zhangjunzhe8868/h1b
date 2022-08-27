'''
output the most H1b state and H1b occupation
select EMPLOYER_STATE, count(EMPLOYER_STATE), round(count(*)/sum(count(*)) over (),2) from table where CASE_STATUS="CERTIFIED" group by EMPLOYER_STATE order by count(EMPLOYER_STATE) DESC;
select SOC_NAME, count(SOC_NAME), round(count(*)/sum(count(*)) over (),2) from table where CASE_STATUS="CERTIFIED" group by SOC_NAME order by count(SOC_NAME) DESC
'''

data=[]
dataClean=[]
jobTitle={}
employeeState={}
outJobTitle=[]
outEmployeeState=[]

with open('h1b_input.csv', 'r', encoding="utf8") as f:
    lines=f.readlines()
    firstLine=lines[0].replace('\n','')
    title=firstLine.split(';')
    for i in range(1,len(lines)):
            temp=lines[i].replace('\n','')
            data.append(temp.split(';'))
            
jobTitleIdx=title.index('SOC_NAME')
employeeStateIdx=title.index('EMPLOYER_STATE')
certifiedIdx=title.index('CASE_STATUS')  

for i in range(len(data)):
    if data[i][certifiedIdx]=='CERTIFIED' and data[i][jobTitleIdx]!=-1 and data[i][employeeStateIdx]!=-1:
        dataClean.append(data[i])

totalNum=len(dataClean)

for i in range(len(dataClean)):
    jobTitle[dataClean[i][jobTitleIdx]]=jobTitle.get(dataClean[i][jobTitleIdx],0)+1
    employeeState[dataClean[i][employeeStateIdx]]=employeeState.get(dataClean[i][employeeStateIdx],0)+1

#add more att, then sort
for i in range(len(jobTitle)):
    outJobTitle.append([list(jobTitle.keys())[i].strip('"'),jobTitle[list(jobTitle.keys())[i]],jobTitle[list(jobTitle.keys())[i]]/totalNum])
for i in range(len(employeeState)):
    outEmployeeState.append([list(employeeState.keys())[i],employeeState[list(employeeState.keys())[i]],employeeState[list(employeeState.keys())[i]]/totalNum])

outJobTitle.sort(key=lambda x:x[1],reverse=True)
outEmployeeState.sort(key=lambda x:x[1],reverse=True)

with open('top_10_states.txt', 'w') as f:
    f.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
    for row in outEmployeeState:
        rowtxt = '{};{};{}\n'.format(row[0], row[1], row[2])
        f.write(rowtxt)
    f.close()

with open('top_10_occupations.txt', 'w') as f:
    f.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
    for row in outJobTitle:
        rowtxt = '{};{};{}\n'.format(row[0], row[1], row[2])
        f.write(rowtxt)
    f.close()
