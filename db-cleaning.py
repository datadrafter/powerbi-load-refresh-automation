# Imports
import csv
import os
import numpy as np
import math

# File to get data from
source_file = 'answerdatacorrect.csv'

# %% ASSIGNMENT 1.1
"""
ASSIGNMENT 1.1
You will have to generate some missing ids, like organizationid and geoid. Use
the data that you have available in a suitable way to infer or generate these ids
"""

# Function to create organizationid
def get_organizationId():
    groupId = []
    quizId = []
    schemeId = []
    organizationId = []
    
    # Getting the different ids to build organizationId
    with open(source_file) as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            groupId.append(col['GroupId'])
            quizId.append(col['QuizId'])
            schemeId.append(col['SchemeOfWorkId'])
    
    # Removing decimals from schemeid
    for i in range(len(groupId)):
        temp = float(schemeId[i])
        temp = math.trunc(temp)
        schemeId[i] = temp
             
    # Putting together organization id with groupid, quizid and schemeid
    for i in range(len(groupId)):
        temp = groupId[i] + "-" + quizId[i] + "-" + str(schemeId[i])
        organizationId.append(temp) 
    
    return organizationId, schemeId
    
# Function to create geoid
def get_geoId(countryCode):
    #geoId is a unique identifier taking into consideration the country code and a number corresponding to each region
    region = []
    with open(source_file) as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            region.append(col['Region'])
    
    # Building a dictionary pairing every possible region with a value from 1 to the number of existing regions
    countriesDict = dict(zip(np.unique(region), range(1,len(np.unique(region))+1)))
    
    # Looping through region looking for matches with the dict keys and assigning the countryCode + value from the dict
    geoId = []
    for i in range(len(countryCode)): 
        for key, value in countriesDict.items():
            if region[i] == key:
                temp = countryCode[i] + "-" + str(value)
                geoId.append(temp)
    
    return geoId

# %% ASSIGNMENT 1.2
"""
ASSIGNMENT 1.2
the iscorrect attribute is the main measure of the datawarehouse. You
can compute its values by comparing the variables answer value and correct answer
"""

def isAnswerCorrect():
    isCorrect = []
    correctAnswer = []
    answerValue = []

    # Getting CorrectAnswer and AnswerValue from the source file to use for calculating the "isCorrect" variable
    with open(source_file) as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            correctAnswer.append(col['CorrectAnswer'])
            answerValue.append(col['AnswerValue'])
    
    # If CorrectAnswer is the same as the answer given by AnswerValue, then we give "1" to isCorrect, 0 otherwise
    for i in range(len(correctAnswer)):
        if correctAnswer[i] == answerValue[i]:
            correct = 1
        else:
            correct = 0
        isCorrect.append(correct)
    
    return isCorrect
        
# %% ASSIGNMENT 1.3
""" 
ASSIGNMENT 1.3
the description in the subject table should be a string describing the
various topics of the question in subject level order 
(explore the subject metadata.csv to learn more about that)
"""

def get_subject_description():
    answerSubjectId = []
    metaSubjectId = []
    metaSubjectName = []
    metaSubjectLevel = []
    
    # Getting the subject Ids corresponding to each answer
    with open(source_file) as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            answerSubjectId.append(col['SubjectId'])
            
    # Cleaning subjectId, removing '[]', ',' and splitting each value
    for i in range(len(answerSubjectId)):
        answerSubjectId[i] = answerSubjectId[i].lstrip(answerSubjectId[i][0]).rstrip(answerSubjectId[i][-1])
        answerSubjectId[i] = answerSubjectId[i].replace(',', '')
        answerSubjectId[i] = answerSubjectId[i].split()
        
    # From the subject_metadata, getting the Id of each individual subject
    with open('subject_metadata.csv') as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            metaSubjectId.append(col['SubjectId'])
    
    # Getting the subject's description
    with open('subject_metadata.csv') as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            metaSubjectName.append(col['Name'])
            
    # Getting the subject's level
    with open('subject_metadata.csv') as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            metaSubjectLevel.append(col['Level'])
            
    for i in range(len(metaSubjectLevel)):
        metaSubjectLevel[i] = int(metaSubjectLevel[i])
        
    # Creating empty lists for the subject description and levels, along with their dictionaries
    answerSubjectDescription = []
    answerSubjectLevel = []
    subjectDescriptionDict = dict(zip(metaSubjectId, metaSubjectName))
    subjectLevelDict = dict(zip(metaSubjectName, metaSubjectLevel)) 
    
    answerSubjectDescription.extend(range(0, len(answerSubjectId)))
    answerSubjectLevel.extend(range(0, len(answerSubjectId)))
    for i in range(len(answerSubjectId)):
        # Using list comprehension to map subject ids to their actual name, the same with level
        answerSubjectDescription[i] = [subjectDescriptionDict[k] for k in answerSubjectId[i]]
        answerSubjectLevel[i] = [subjectLevelDict[k] for k in answerSubjectDescription[i]]
        # Sorting by subject level
        answerSubjectDescription[i] = [x for _,x in sorted(zip(answerSubjectLevel[i],answerSubjectDescription[i]))]
        
    return answerSubjectDescription

# %% ASSIGNMENT 1.4
""" 
ASSIGNMENT 1.4
find a way of integrating the continent into the Geography table. You can
retrieve the information somewhere, or find a way of providing it yourself
"""

def get_continent(countryCode):
    continent = []
    
    # Assigning continent based on countryCode
    for i in range(len(countryCode)):
        if countryCode[i] in {"be", "de", "es", "fr", "ie", "it", "uk"}:
            continentName = "Europe"
        elif countryCode[i] in {"ca", "us"}:
            continentName = "America"
        elif countryCode[i] in {"nz", "au"}:
            continentName = "Oceania"            
        else:
            continentName = "Unknown continent"
        
        continent.append(continentName)
    
    return continent

def get_countryName(countryCode):
    countryName = []
    
    # Building a dictionary with the country codes and the full name of the country
    countryShort = np.unique(countryCode)
    countryFull = ["Australia", "Belgium", "Canada", "Germany", "Spain", "France", "Ireland", 
                   "Italy", "New Zealand", "United Kingdom", "United States"]
    countriesDict = dict(zip(countryShort, countryFull)) 
    
    # Mapping countryCode to full name
    countryName.extend(range(0, len(countryCode)))
    for i in range(len(countryCode)):
        for key, value in countriesDict.items():
            if countryCode[i] in key:
                countryName[i] = value
        
    return countryName

# %% ASSIGNMENT 1.5
"""
ASSIGNMENT 1.5
the Data table should accommodate for both dates of birth of users and for
dates of answers. You can clip dates to the day, discarding hours and minutes.
"""

def get_date():
    # Taking date of birth and date of answer to prepare them to be put together in the column date
    dateBirth = []
    dateAnswerfull = []
    dateAnswer = []
    datefull = []

    # After having the dates in the date column, we take their year, month, day and quarter
    date = []
    year = []
    month = []
    day = []
    quarter = []
        
    # Getting dates of birth and answer
    with open(source_file) as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            dateBirth.append(col['DateOfBirth'])
            dateAnswerfull.append(col['DateAnswered'])
 
    # Preparing the date column together with date of birth and date of answer
    for i in range(len(dateBirth)):
        dateAnswerfull[i] = dateAnswerfull[i].replace('-', ' ')
        dateAnswerfull[i] = dateAnswerfull[i].split()
        dateAnswerfull[i].pop(3)
        
        temp = dateAnswerfull[i][0] + "-" + dateAnswerfull[i][1] + "-" + dateAnswerfull[i][2]
        dateAnswer.append(temp)
        
        datefull.append(dateAnswer[i])
        datefull.append(dateBirth[i])
    
    # Removing repeated dates
    date_unique = list(np.unique(datefull))
    
    # Getting year, month, day and quarter for each date
    for i in range(len(date_unique)):
        date_unique[i] = date_unique[i].replace('-', ' ')
        date_unique[i] = date_unique[i].split()
        
        tempYear = date_unique[i][0]
        year.append(tempYear)
        tempMonth = date_unique[i][1]
        month.append(tempMonth)
        tempDay = date_unique[i][2]
        day.append(tempDay)
        
        if date_unique[i][1] in {'01','02','03'}:
            tempQuarter = 1
        elif date_unique[i][1] in {'04','05','06'}:
            tempQuarter = 2
        elif date_unique[i][1] in {'07','08','09'}:
            tempQuarter = 3
        elif date_unique[i][1] in {'10','11','12'}:
            tempQuarter = 4
        quarter.append(tempQuarter)   
        
        temp = date_unique[i][0] + "-" + date_unique[i][1] + "-" + date_unique[i][2]
        date.append(temp)
        
    return dateAnswer, date, year, month, day, quarter    

def get_answerDateId(dateDict):
    dateAnswer = []
    answerDateId = []
    
    with open('Tables/Answers_copy2.csv') as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            dateAnswer.append(col['DateAnswered'])
    
    # comparing date of answer to the values of the dictionary with the dates, if they match, assign id
    answerDateId.extend(range(0, len(dateAnswer)))
    for i in range(len(dateAnswer)):
        for key, value in dateDict.items():
            if dateAnswer[i] in value:
                answerDateId[i] = key
    
    return answerDateId
    
def get_userDateId(dateDict):
    dateBirth = []
    birthDateId = []
    
    with open('Tables/User_copy3.csv') as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            dateBirth.append(col['DateOfBirth'])
    
    # comparing date of birth to the values of the dictionary with the dates, if they match, assign id
    birthDateId.extend(range(0, len(dateBirth)))
    for i in range(len(dateBirth)):
        for key, value in dateDict.items():
            if dateBirth[i] in value:
                birthDateId[i] = key
                
    return birthDateId

# %% TABLE CREATION

# %%% DATE

# Column indexes to be removed
cols_to_remove = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] 
# Reverse so we remove from the end first
cols_to_remove = sorted(cols_to_remove, reverse=True) 

# Opening the original file and removing not needed columns, then writing the rest to the new table
with open(source_file, "r") as source:
    reader = csv.reader(source)
    with open('Tables/Date_copy.csv', "w", newline='') as result:
        writer = csv.writer(result)
        for row in reader:
            for col_index in cols_to_remove:
                del row[col_index]
            writer.writerow(row)
            
answerDate, date, year, month, day, quarter = get_date()

# Creating an id that goes with each date obtained from the previous function
dateId = []
for i in range(len(date)):
    temp = str(i+1)
    dateId.append(temp)
    
# Bulding a dictionary to store each date with its id
dateDict = dict(zip(dateId, date))

with open('Tables/Date_copy.csv', 'r') as file_input:
    file_output = open('Tables/Date.csv', 'w')
    reader = csv.reader(file_input)
    writer = csv.writer(file_output, delimiter=',', lineterminator='\n')

    for i, row in enumerate(reader):
        if i==0:
            row.append("DateId")
            row.append("Date")
            row.append("Day")
            row.append("Month")
            row.append("Year")
            row.append("Quarter")
            writer.writerow(row)
        else:
            row.append(dateId[i-1])
            row.append(date[i-1])
            row.append(day[i-1])
            row.append(month[i-1])
            row.append(year[i-1])
            row.append(quarter[i-1])
            writer.writerow(row)
        
        if i == len(date):
            break
            
    file_output.close()

os.remove('Tables/Date_copy.csv')

# %%% ANSWERS

# Column indexes to be removed
cols_to_remove = [5,6,7,8,10,11,12,14,15,16] 
# Reverse so we remove from the end first
cols_to_remove = sorted(cols_to_remove, reverse=True) 

# Opening the original file and removing not needed columns, then writing the rest to the new table
with open(source_file, "r") as source:
    reader = csv.reader(source)
    with open('Tables/Answers_copy.csv', "w", newline='') as result:
        writer = csv.writer(result)
        for row in reader:
            for col_index in cols_to_remove:
                del row[col_index]
            writer.writerow(row)

isCorrect = isAnswerCorrect()
organizationId, schemeId = get_organizationId()

# Adding the previously created isCorrect list as a column for the Answers table
with open('Tables/Answers_copy.csv', 'r') as file_input:
    file_output = open('Tables/Answers_copy2.csv', 'w')
    reader = csv.reader(file_input)
    writer = csv.writer(file_output, delimiter=',', lineterminator='\n')

    for i, row in enumerate(reader):
        if i==0:
            row.append("isCorrect")
            row.append("OrganizationId")
            row.append("DateAnswered")
            writer.writerow(row)
        else:
            row.append(isCorrect[i-1])
            row.append(organizationId[i-1])
            row.append(answerDate[i-1])
            writer.writerow(row)
            
    file_output.close()
    
answerDateId = get_answerDateId(dateDict)

with open('Tables/Answers_copy2.csv', 'r') as file_input:
    file_output = open('Tables/Answers.csv', 'w')
    reader = csv.reader(file_input)
    writer = csv.writer(file_output, delimiter=',', lineterminator='\n')

    for i, row in enumerate(reader):
        if i==0:
            row.append("DateId")
            writer.writerow(row)
        else:
            row.append(answerDateId[i-1])
            writer.writerow(row)
            
    file_output.close()

os.remove('Tables/Answers_copy.csv')
os.remove('Tables/Answers_copy2.csv')

# %%% ORGANIZATION

# Column indexes to be removed
cols_to_remove = [0,1,2,3,4,5,6,7,8,9,12,13,14,15,16] 
# Reverse so we remove from the end first
cols_to_remove = sorted(cols_to_remove, reverse=True) 

# Opening the original file and removing not needed columns, then writing the rest to the new table
with open(source_file, "r") as source:
    reader = csv.reader(source)
    with open('Tables/Organization_copy.csv', "w", newline='') as result:
        writer = csv.writer(result)
        for row in reader:
            for col_index in cols_to_remove:
                del row[col_index]
            writer.writerow(row)
            
# Adding the previously created subject_description as a column for the Subject table
with open('Tables/Organization_copy.csv', 'r') as file_input:
    file_output = open('Tables/Organization_copy2.csv', 'w')
    reader = csv.reader(file_input)
    writer = csv.writer(file_output, delimiter=',', lineterminator='\n')

    for i, row in enumerate(reader):
        if i==0:
            row.append("OrganizationId")
            row.append("SchemeOfWorkId")
            writer.writerow(row)
        else:
            row.append(organizationId[i-1])
            row.append(schemeId[i-1])
            writer.writerow(row)
            
    file_output.close()
    
# Removing duplicates
with open('Tables/Organization_copy2.csv', 'r') as file_input, open('Tables/Organization.csv', 'w') as file_output:
    seen = set()
    for line in file_input:
        if line in seen: continue # skip duplicate

        seen.add(line)
        file_output.write(line)
                    
os.remove('Tables/Organization_copy.csv')
os.remove('Tables/Organization_copy2.csv')

# %%% USER

# Column indexes to be removed
cols_to_remove = [0,2,3,4,6,7,8,9,10,11,12,13,14,15,16] 
# Reverse so we remove from the end first
cols_to_remove = sorted(cols_to_remove, reverse=True)  

# Opening the original file and removing not needed columns, then writing the rest to the new table
with open(source_file, "r") as source:
    reader = csv.reader(source)
    with open('Tables/User_copy.csv', "w", newline='') as result:
        writer = csv.writer(result)
        for row in reader:
            for col_index in cols_to_remove:
                del row[col_index]
            writer.writerow(row)
   
# Getting CountryCode and dateofBirth to use in functions
countryCode = []
dateofBirth = []
with open(source_file) as dataFile:
    reader = csv.DictReader(dataFile)
    for col in reader:
        countryCode.append(col['CountryCode'])
        dateofBirth.append(col['DateOfBirth'])
        
geoId = get_geoId(countryCode)

# Adding the previously created continent list as a column for the Geography table
with open('Tables/User_copy.csv', 'r') as file_input:
    file_output = open('Tables/User_copy2.csv', 'w')
    reader = csv.reader(file_input)
    writer = csv.writer(file_output, delimiter=',', lineterminator='\n')

    for i, row in enumerate(reader):
        if i==0:
            row.append("GeoId")
            row.append("DateOfBirth")
            writer.writerow(row)
        else:
            row.append(geoId[i-1])
            row.append(dateofBirth[i-1])
            writer.writerow(row)
            
    file_output.close()
    
# Removing duplicates
with open('Tables/User_copy2.csv', 'r') as file_input, open('Tables/User_copy3.csv', 'w') as file_output:
    seen = set()
    for line in file_input:
        if line in seen: continue # skip duplicate

        seen.add(line)
        file_output.write(line)
        
userDateId = get_userDateId(dateDict)

with open('Tables/User_copy3.csv', 'r') as file_input:
    file_output = open('Tables/User.csv', 'w')
    reader = csv.reader(file_input)
    writer = csv.writer(file_output, delimiter=',', lineterminator='\n')

    for i, row in enumerate(reader):
        if i==0:
            row.append("DateId")
            writer.writerow(row)
        else:
            row.append(userDateId[i-1])
            writer.writerow(row)
            
    file_output.close()
            
os.remove('Tables/User_copy.csv')
os.remove('Tables/User_copy2.csv')
os.remove('Tables/User_copy3.csv')

# %%% SUBJECT

# Column indexes to be removed
cols_to_remove = [0,1,2,3,4,5,6,7,8,9,10,11,12,14,15,16] 
# Reverse so we remove from the end first
cols_to_remove = sorted(cols_to_remove, reverse=True) 

# Opening the original file and removing not needed columns, then writing the rest to the new table
with open(source_file, "r") as source:
    reader = csv.reader(source)
    with open('Tables/Subject_copy.csv', "w", newline='') as result:
        writer = csv.writer(result)
        for row in reader:
            for col_index in cols_to_remove:
                del row[col_index]
            writer.writerow(row)

subject_description = get_subject_description()

# Adding the previously created subject_description as a column for the Subject table
with open('Tables/Subject_copy.csv', 'r') as file_input:
    file_output = open('Tables/Subject_copy2.csv', 'w')
    reader = csv.reader(file_input)
    writer = csv.writer(file_output, delimiter=',', lineterminator='\n')

    for i, row in enumerate(reader):
        if i==0:
            row.append("Description")
            writer.writerow(row)
        else:
            row.append(subject_description[i-1])
            writer.writerow(row)
            
    file_output.close()
    
# Removing duplicates
with open('Tables/Subject_copy2.csv', 'r') as file_input, open('Tables/Subject.csv', 'w') as file_output:
    seen = set()
    for line in file_input:
        if line in seen: continue # skip duplicate

        seen.add(line)
        file_output.write(line)
        
os.remove('Tables/Subject_copy.csv')
os.remove('Tables/Subject_copy2.csv')

# %%% GEOGRAPHY

# Column indexes to be removed
cols_to_remove = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16] 
# Reverse so we remove from the end first
cols_to_remove = sorted(cols_to_remove, reverse=True) 

# Opening the original file and removing not needed columns, then writing the rest to the new table
with open(source_file, "r") as source:
    reader = csv.reader(source)
    with open('Tables/Geography_copy.csv', "w", newline='') as result:
        writer = csv.writer(result)
        for row in reader:
            for col_index in cols_to_remove:
                del row[col_index]
            writer.writerow(row)

# Getting CountryCode to use in different geography functions, such as continent or countryName
countryCode = []
with open(source_file) as dataFile:
    reader = csv.DictReader(dataFile)
    for col in reader:
        countryCode.append(col['CountryCode'])

continent = get_continent(countryCode)
countryName = get_countryName(countryCode)
geoId = get_geoId(countryCode)

# Adding the previously created continent list as a column for the Geography table
with open('Tables/Geography_copy.csv', 'r') as file_input:
    file_output = open('Tables/Geography_copy2.csv', 'w')
    reader = csv.reader(file_input)
    writer = csv.writer(file_output, delimiter=',', lineterminator='\n')

    for i, row in enumerate(reader):
        if i==0:
            row.append("GeoId")
            row.append("CountryName")
            row.append("Continent")
            writer.writerow(row)
        else:
            row.append(geoId[i-1])
            row.append(countryName[i-1])
            row.append(continent[i-1])
            writer.writerow(row)    
                
    file_output.close()
        
# Removing duplicates
with open('Tables/Geography_copy2.csv', 'r') as file_input, open('Tables/Geography.csv', 'w') as file_output:
    seen = set()
    for line in file_input:
        if line in seen: continue # skip duplicate

        seen.add(line)
        file_output.write(line)
   
os.remove('Tables/Geography_copy.csv')
os.remove('Tables/Geography_copy2.csv')