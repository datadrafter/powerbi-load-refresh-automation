import pyodbc as odbc
import csv

# %% Fetching values from the previously created tables

### ANSWERS ###
def get_answers():
    answerid = []
    questionid = []
    userid = []
    organizationid = []
    dateid = []
    subjectid = []
    answer_value = []
    correct_answer = []
    iscorrect = []
    confidence = []
    
    with open('Tables/Answers.csv') as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            answerid.append(col['AnswerId'])
            questionid.append(col['QuestionId'])
            userid.append(col['UserId'])
            organizationid.append(col['OrganizationId'])
            dateid.append(col['DateId'])
            subjectid.append(col['SubjectId'])
            answer_value.append(col['AnswerValue'])
            correct_answer.append(col['CorrectAnswer'])
            iscorrect.append(col['isCorrect'])
            confidence.append(col['Confidence'])
            
    return answerid, questionid, userid, organizationid, dateid, subjectid, answer_value, correct_answer, iscorrect, confidence

### USER ###
def get_user():
    userid = []
    dateid = []
    geoid = []
    gender = []
    
    with open('Tables/User.csv') as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            userid.append(col['UserId'])
            dateid.append(col['DateId'])
            geoid.append(col['GeoId'])
            gender.append(col['Gender'])
            
    return userid, dateid, geoid, gender

### ORGANIZATION ###
def get_organization():
    organizationid = []
    groupid = []
    quizid = []
    schemeofworkid = []
    
    with open('Tables/Organization.csv') as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            organizationid.append(col['OrganizationId'])
            groupid.append(col['GroupId'])
            quizid.append(col['QuizId'])
            schemeofworkid.append(col['SchemeOfWorkId'])
            
    return organizationid, groupid, quizid, schemeofworkid

### DATE ###
def get_date():
    dateid = []
    date = []
    day = []
    month = []
    year = []
    quarter = []
    
    with open('Tables/Date.csv') as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            dateid.append(col['DateId'])
            date.append(col['Date'])
            day.append(col['Day'])
            month.append(col['Month'])
            year.append(col['Year'])
            quarter.append(col['Quarter'])
            
    return dateid, date, day, month, year, quarter 

### SUBJECT ###
def get_subject():
    subjectid = []
    description = []
    
    with open('Tables/Subject.csv') as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            subjectid.append(col['SubjectId'])
            description.append(col['Description'])
            
    return subjectid, description 

### GEOGRAPHY ###
def get_geography():
    geoid = []
    region = []
    country_name = []
    continent = []
    
    with open('Tables/Geography.csv') as dataFile:
        reader = csv.DictReader(dataFile)
        for col in reader:
            geoid.append(col['GeoId'])
            region.append(col['Region'])
            country_name.append(col['CountryName'])
            continent.append(col['Continent'])
            
    return geoid, region, country_name, continent
    
# %% Populating the database

# Access info for the database
server = 'tcp:lds.di.unipi.it'
driver = '{ODBC Driver 17 for SQL Server}'
database = 'Group_3_DB'
username = 'group_3'
password = 'WE6WJR67'
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password

# Initializing the connection and cursor
cnxn = odbc.connect(connectionString)
cursor = cnxn.cursor()

# NOTE, since the database is already populated, rerunning this code will result in error due to
# repeated records being inserted into PKs, in order to run this script for a 2nd time
# it is necessary to drop foreign keys and add them again after truncating the table and repopulating it
# if populating a fresh database, the following are not necessary
cursor.execute("ALTER TABLE ANSWERS DROP CONSTRAINT FK_Answers_Date")
cursor.execute("ALTER TABLE ANSWERS DROP CONSTRAINT FK_Answers_Organization")
cursor.execute("ALTER TABLE ANSWERS DROP CONSTRAINT FK_Answers_Subject")
cursor.execute("ALTER TABLE ANSWERS DROP CONSTRAINT FK_Answers_Users")
cursor.execute("ALTER TABLE USERS DROP CONSTRAINT FK_Users_Date")
cursor.execute("ALTER TABLE USERS DROP CONSTRAINT FK_Users_Geography")
cnxn.commit()

# Populating ANSWER
answerid, questionid, userid, organizationid, dateid, subjectid, answer_value, correct_answer, iscorrect, confidence = get_answers()
sql = "INSERT INTO ANSWERS(answerid, questionid, userid, organizationid, dateid, subjectid, answer_value, correct_answer, iscorrect, confidence) VALUES(?,?,?,?,?,?,?,?,?,?)"
cursor.execute("TRUNCATE TABLE ANSWERS")
for i in range(len(answerid)):
    cursor.execute(sql, (answerid[i], questionid[i], userid[i], organizationid[i], dateid[i], subjectid[i], answer_value[i], correct_answer[i], iscorrect[i], confidence[i]))
cnxn.commit()

# Populating USER
userid, dateid, geoid, gender = get_user()
sql = "INSERT INTO USERS(userid,dateid,geoid,gender) VALUES(?,?,?,?)"
cursor.execute("TRUNCATE TABLE USERS")
for i in range(len(userid)):
    cursor.execute(sql, (userid[i],dateid[i],geoid[i],gender[i]))
cnxn.commit()

# Populating ORGANIZATION
organizationid, groupid, quizid, schemeofworkid = get_organization()
sql = "INSERT INTO ORGANIZATION(organizationid,groupid,quizid,schemeofworkid) VALUES(?,?,?,?)"
cursor.execute("TRUNCATE TABLE ORGANIZATION")
for i in range(len(organizationid)):
    cursor.execute(sql, (organizationid[i],groupid[i],quizid[i],schemeofworkid[i]))
cnxn.commit()

# Populating DATE
dateid, date, day, month, year, quarter = get_date()
sql = "INSERT INTO DATE(dateid,date,day,month,year,quarter) VALUES(?,?,?,?,?,?)"
cursor.execute("TRUNCATE TABLE DATE")
for i in range(len(dateid)):
    cursor.execute(sql, (dateid[i],date[i],day[i],month[i],year[i],quarter[i]))
cnxn.commit()

# Populating SUBJECT
subjectid, description = get_subject()
sql = "INSERT INTO SUBJECT(subjectid,description) VALUES(?,?)"
cursor.execute("TRUNCATE TABLE SUBJECT")
for i in range(len(subjectid)):
    cursor.execute(sql, (subjectid[i], description[i]))
cnxn.commit()

# Populating GEOGRAPHY
geoid, region, country_name, continent = get_geography()
sql = "INSERT INTO GEOGRAPHY(geoid,region,country_name,continent) VALUES(?,?,?,?)"
cursor.execute("TRUNCATE TABLE GEOGRAPHY")
for i in range(len(geoid)):
    cursor.execute(sql, (geoid[i],region[i],country_name[i],continent[i]))
cnxn.commit()

# Now that the tables are populated, we assign the necessary relationships with FKs
cursor.execute("ALTER TABLE ANSWERS ADD CONSTRAINT FK_Answers_Date FOREIGN KEY (dateid) REFERENCES DATE (dateid)")
cursor.execute("ALTER TABLE ANSWERS ADD CONSTRAINT FK_Answers_Organization FOREIGN KEY (organizationid) REFERENCES ORGANIZATION (organizationid)")
cursor.execute("ALTER TABLE ANSWERS ADD CONSTRAINT FK_Answers_Subject FOREIGN KEY (subjectid) REFERENCES SUBJECT (subjectid)")
cursor.execute("ALTER TABLE ANSWERS ADD CONSTRAINT FK_Answers_Users FOREIGN KEY (userid) REFERENCES USERS (userid)")
cursor.execute("ALTER TABLE USERS ADD CONSTRAINT FK_Users_Date FOREIGN KEY (dateid) REFERENCES DATE (dateid)")
cursor.execute("ALTER TABLE USERS ADD CONSTRAINT FK_Users_Geography FOREIGN KEY (geoid) REFERENCES GEOGRAPHY (geoid)")
cnxn.commit()

# %%