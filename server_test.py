#!C:\Program Files (x86)\Python36-32\python.exe
# -*- coding: utf-8 -*-
import sqlite3
import socket
import hashlib
import cgi
import html
import json
# import request

import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

form = cgi.FieldStorage()

text1 = form.getfirst("REQUEST", "")
text2 = form.getfirst("ID", "")
text3 = form.getfirst("NAME", "")
text4 = form.getfirst("LOGIN", "")
text5 = form.getfirst("PASSWORD", "")
text6 = form.getfirst("SURNAME", "")
text7 = form.getfirst("PATRONYMIC", "")
text8 = form.getfirst("COUNT", "")
text9 = form.getfirst("ALL_COUNT", "")
text10 = form.getfirst("USE_COUNT", "")
text11 = form.getfirst("DATA", "")
text12 = form.getfirst("DESCRIPTION", "")
text13 = form.getfirst("ID_2", "")
text14 = form.getfirst("CHECKED", "")

text1 = html.escape(text1)
text2 = html.escape(text2)
text3 = html.escape(text3)
text4 = html.escape(text4)
text5 = html.escape(text5)
text6 = html.escape(text6)
text7 = html.escape(text7)
text8 = html.escape(text8)
text9 = html.escape(text9)
text10 = html.escape(text10)
text11 = html.escape(text11)
text12 = html.escape(text12)
text13 = html.escape(text13)
text14 = html.escape(text14)


def htmlWrite(data):
    print(data + "<br />")

print("Content-Type: application/json\n")

conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# ================================================


def test():
    htmlWrite("Ok\n");
    cursor.execute("INSERT INTO componentsProject (idProject, idComponent, count) VALUES (1,1,1)")
    print("All right")
    conn.commit()


def js():
    data = {"name": "Arduino", "count": "30"}
    s = json.dumps(data) + ','
    data = {"name": "Светодиоды", "count": "1000"}
    s += json.dumps(data)
    print('{ "components": [' + s + "]}")


def login():
    cursor.execute("SELECT * FROM users")
    row = cursor.fetchall()
    login = text4
    password = text5
    i = 0
    connect = False
    while i < len(row):
        if login == row[i][1] and password == row[i][2]:
            mentor = 0
            if row[i][6] == "IT":
                mentor = 1
            data = {"request": "true", "id": str(row[i][0]), "mentor": mentor, "name": str(row[i][4]), "secondname": str(row[i][3]), "vk": str(row[i][8])}
            connect = True
        i = i + 1
    if not connect:
        data = {"request": "false", "id": None, "mentor": 0, "name": "", "secondname": ""}
    s = json.dumps(data)
    print(s)


# ================================================ Команды пользователя


def allUsers():
    cursor.execute("SELECT * FROM users")
    row = cursor.fetchall()
    i = 0
    while i < len(row):
        data = {"id": str(row[i][0]), "login": str(row[i][1]), "password": str(row[i][2]), "secondname": str(row[i][3]),
                "name": str(row[i][4]), "patronymic": str(row[i][5]), "role": str(row[i][6]), "class": str(row[i][7]), "vk": str(row[i][8])}
        if len(row) - 1 == i and i != 0:
            s += json.dumps(data)
        elif i == 0 and len(row) - 1 == 0:
            s = json.dumps(data)
        elif i == 0:
            s = json.dumps(data) + ','
        else:
            s += json.dumps(data) + ','

        i = i + 1
    print('{ "users": [' + s + "]}")


def getUser():
    id = int(text2)
    cursor.execute("SELECT * FROM users WHERE id=?", [id])
    row = cursor.fetchall()
    data = {"id": str(row[0][0]), "login": str(row[0][1]), "password": str(row[0][2]), "secondname": str(row[0][3]),
            "name": str(row[0][4]), "patronymic": str(row[0][5]), "role": str(row[0][6]), "class": str(row[0][7]),
            "vk": str(row[0][8])}
    s = json.dumps(data)
    print(s)


def getStudents():
    cursor.execute("SELECT * FROM users WHERE role=?", ["c"])
    row = cursor.fetchall()
    i = 0
    while i < len(row):
        data = {"id": str(row[i][0]), "login": str(row[i][1]), "password": str(row[i][2]), "secondname": str(row[i][3]),
                "name": str(row[i][4]), "patronymic": str(row[i][5]), "role": str(row[i][6]), "class": str(row[i][7])}
        if len(row) - 1 == i and i != 0:
            s += json.dumps(data)
        elif i == 0 and len(row) - 1 == 0:
            s = json.dumps(data)
        elif i == 0:
            s = json.dumps(data) + ','
        else:
            s += json.dumps(data) + ','

        i = i + 1
    print('{ "users": [' + s + "]}")


def getTimeGroup():
    id = int(text2)
    cursor.execute("SELECT * FROM groups WHERE id=?", [id])
    row = cursor.fetchall()
    data = {"time": str(row[0][1]), "day_week": str(row[0][2])}
    s = json.dumps(data)
    print(s)


def addUser():
    login = text4
    password = text5
    secondname = text6
    name = text3
    patronymic = text7

    cursor.execute('INSERT INTO users (login , password, surname, name, patronymic) VALUES (?,?,?,?,?)',
                   (login, password, secondname, name, patronymic))
    htmlWrite("Done")
    conn.commit()


def changeUserPassword():
    id = int(text2)
    password = text5

    print(id)
    print(password)
    cursor.execute("UPDATE users SET password =? WHERE id =?", (password, id))
    htmlWrite("Done")
    conn.commit()


# ================================================ Комады компонентов


def addComponent():
    name = text3
    allCount = text8

    print(name)
    print(allCount)

    cursor.execute('INSERT INTO components (name , allCount, useCount) VALUES (?,?,?)', (name, allCount, 0))
    htmlWrite("Done")
    conn.commit()


def addAllComponents():
    f = open('Components.txt', 'r')

    i = 0
    name = []
    allCounts = []

    for line in f:
        if i % 2 == 0:
            name.append(line)
        else:
            allCounts.append(line)
        i = i + 1

    j = 0

    while j < len(name):
        cursor.execute("INSERT INTO components (name, allCount, useCount) VALUES (?, ?, ?)", (name[j], allCounts[j], 0))
        j = j + 1;
    conn.commit()


def getComponent():
    id = int(text2)
    cursor.execute("SELECT * FROM components WHERE id=?", [id])
    component = cursor.fetchall()
    data = {"id": str(component[0][0]), "name": str(component[0][1]).replace("\n", ""),
            "count": int(str(component[0][2])) - int(str(component[0][3])), "image": str(component[0][4]), "description"
            : str(component[0][5]), "characteristics": str(component[0][6]), "documentation": str(component[0][7])}
    s = json.dumps(data)
    print(s)
    
    
def getComponentByComponentProject():
    id = int(text2)
    cursor.execute("SELECT * FROM componentsProject WHERE id=?", [id])
    componentProject = cursor.fetchall()
    idComponent = componentProject[0][2]
    cursor.execute("SELECT * FROM components WHERE id=?", [idComponent])
    component = cursor.fetchall()
    data = {"id": str(component[0][0]), "name": str(component[0][1]).replace("\n", ""),
            "count": int(str(component[0][2])) - int(str(component[0][3])), "image": str(component[0][4]), "description"
            : str(component[0][5]), "characteristics": str(component[0][6]), "documentation": str(component[0][7])}
    s = json.dumps(data)
    print(s)


def getAllComponents():
    cursor.execute("SELECT * FROM components")
    row = cursor.fetchall()
    i = 0
    while i < len(row):
        data = {"id": str(row[i][0]), "name": str(row[i][1]).replace("\n", ""), "count": int(str(row[i][2])) - int(str(row[i][3])), "image": str(row[i][4])}
        if len(row) - 1 == i and i != 0:
            s += json.dumps(data)
        elif i == 0 and len(row) - 1 == 0:
            s = json.dumps(data)
        elif i == 0:
            s = json.dumps(data) + ','
        else:
            s += json.dumps(data) + ','
        i = i + 1
    print('{ "components": [' + s + "]}")


def setImageComponent():
    image = text11
    id = int(text2)
    cursor.execute("UPDATE components SET image =? WHERE id =?", (image, id))
    htmlWrite("Done")
    conn.commit()


def changeComponent():
    id = int(text2)
    name = text3
    allCount = text9
    useCount = text10

    print(id)
    print(allCount)
    print(useCount)
    cursor.execute("UPDATE components SET name =?, allCount =?, useCount =? WHERE id =?",
                   (name, allCount, useCount, id))
    htmlWrite("Done")
    conn.commit()


def deleteComponent():
    id = int(text2)

    cursor.execute("DELETE FROM components WHERE id =" + str(id))
    htmlWrite("Done")
    conn.commit()


# ================================================ Команды компонентов проекта

# <<<<<<<<<<================================================================= ПРОВЕРИТЬ!
def addComponentProject():

    id_component = []
    count = []
    id_project = int(text2)
    id_component_ = text13
    count_ = text8
    i = 0
    idComp = ""
    while i < len(id_component_):
        if id_component_.find(",") == -1:
            k = 0
            while k < len(id_component_):
                idComp += id_component_[k]
                k = k + 1
            id_component.append(int(idComp))
        elif i == len(id_component_) - 1:
            idComp += id_component_[i]
            id_component.append(int(idComp))
        elif id_component_[i] != ',':
            idComp += id_component_[i]
        else:
            id_component.append(int(idComp))
            idComp = ""
        i = i + 1
    i = 0
    countComp = ""
    while i < len(count_):
        if count_.find(",") == -1:
            k = 0
            while k < len(count_):
                countComp += count_[i]
                k = k + 1
            count.append(int(countComp))
            break
        elif i == len(count_) - 1:
            countComp += count_[i]
            count.append(int(countComp))
        elif count_[i] != ',':
            countComp += count_[i]
        else:
            count.append(int(countComp))
            countComp = ""
        i = i + 1

    cursor.execute("SELECT * FROM componentsProject WHERE idProject =?", [id_project])
    componentProject = cursor.fetchall()
    j = 0
    while j < len(id_component):
        haveComponent = False
        i = 0
        while i < len(componentProject):
            if componentProject[i][2] == id_component[j]:
                countComponent = componentProject[i][3]
                _countComponent = countComponent + count[j]
                _id_component = i + 1
                print(_id_component)
                cursor.execute("UPDATE componentsProject SET count =? WHERE id=?",
                               (_countComponent, componentProject[i][0]))
                haveComponent = True
            i = i + 1
        if not haveComponent:
            cursor.execute("INSERT INTO componentsProject (idProject, idComponent, count) VALUES (?,?,?)",
                           (id_project, id_component[j], count[j]))

        cursor.execute("SELECT * FROM components WHERE id =?", [id_component[j]])
        component = cursor.fetchall()
        useCount = component[0][3]
        _useCount = useCount + count[j]
        cursor.execute("UPDATE components SET useCount =? WHERE id =?", (_useCount, id_component[j]))
        conn.commit()
        j = j + 1
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def getComponentsProject():
    id_project = int(text2)
    cursor.execute("SELECT * FROM componentsProject WHERE idProject=?", [id_project])
    componentsProject = cursor.fetchall()
    i = 0
    while i < len(componentsProject):
        cursor.execute("SELECT * FROM components WHERE id=?", [componentsProject[i][2]])
        row = cursor.fetchall()
        data = {"id": str(componentsProject[i][0]), "name": str(row[0][1]).replace("\n", ""), "count": str(componentsProject[i][3]), "image": str(row[0][4])}
        if i == len(componentsProject) - 1 and i != 0:
            s += json.dumps(data)
        elif i == 0 and len(componentsProject) - 1 == 0:
            s = json.dumps(data)
        elif i == 0:
            s = json.dumps(data) + ','
        else:
            s += json.dumps(data) + ','
        i = i + 1

    print('{ "components": [' + s + "]}")


def deleteComponentProject():
    id = int(text2)
    cursor.execute("SELECT * FROM componentsProject WHERE id=?", [id])
    componentProject = cursor.fetchall()
    idComponent = componentProject[0][2]
    numberComponent = componentProject[0][3]
    cursor.execute("SELECT * FROM components WHERE id=?", [idComponent])
    component = cursor.fetchall()
    number = component[0][3]
    number = number - numberComponent
    cursor.execute("UPDATE components SET useCount=? WHERE id =?", (number, idComponent))
    cursor.execute("DELETE FROM componentsProject WHERE id =" + str(id))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def changeNumberComponentProject():
    id = int(text2)
    count = int(text8)
    cursor.execute("SELECT * FROM componentsProject WHERE id=?", [id])
    componentProject = cursor.fetchall()
    idComponent = componentProject[0][2]
    countComponent = componentProject[0][3]
    newCount = count - countComponent
    cursor.execute("UPDATE componentsProject SET count=? WHERE id =?", (count, id))
    cursor.execute("SELECT * FROM components WHERE id=?", [idComponent])
    component = cursor.fetchall()
    countComp = component[0][3]
    countComp = countComp + newCount
    cursor.execute("UPDATE components SET useCount=? WHERE id =?", (countComp, idComponent))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


# ================================================ Команды целей


def addObjective():
    id = int(text2)
    objective = text11
    cursor.execute('INSERT INTO objectives (idProject, objective, checked) VALUES (?,?,?)', (id, objective, False))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def setCheckObjective():
    id = []
    checked = []
    id_ = text2
    checked_ = text14
    idObj = ""
    i = 0
    while i < len(id_):
        if id_.find(",") == -1:
            k = 0
            while k < len(id_):
                idObj += id_[k]
                k = k + 1
            id.append(int(idObj))
        elif i == len(id_) - 1:
            idObj += id_[i]
            id.append(int(idObj))
        elif id_[i] != ',':
            idObj += id_[i]
        else:
            id.append(int(idObj))
            idObj = ""
        i = i + 1
    i = 0
    check = ""
    while i < len(checked_):
        if checked_.find(",") == -1:
            k = 0
            while k < len(checked_):
                check += checked_[k]
                k = k + 1
            checked.append(check)
            break
        elif i == len(checked_) - 1:
            check += checked_[i]
            checked.append(check)
        elif checked_[i] != ',':
            check += checked_[i]
        else:
            checked.append(check)
            check = ""
        i = i + 1
    j = 0
    while j < len(id):
        cursor.execute("UPDATE objectives SET checked=? WHERE id =?", (eval(checked[j]), id[j]))
        conn.commit()
        j = j + 1
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def getObjective():
    id = int(text2)
    cursor.execute("SELECT * FROM objectives WHERE idProject=?", [id])
    row = cursor.fetchall()
    data = {"id": str(row[0][0]), "objective": str(row[0][2]), "checked": str(row[0][3])}
    s = json.dumps(data)
    print(s)


def getObjectivesProject():
    id = int(text2)
    cursor.execute("SELECT * FROM objectives WHERE idProject=?", [id])
    row = cursor.fetchall()
    i = 0
    while i < len(row):
        data = {"id": str(row[i][0]), "objective": str(row[i][2]), "checked": str(row[i][3])}
        if len(row) - 1 == i and i != 0:
            s += json.dumps(data)
        elif i == 0 and len(row) - 1 == 0:
            s = json.dumps(data)
        elif i == 0:
            s = json.dumps(data) + ','
        else:
            s += json.dumps(data) + ','
        i = i + 1
    print('{ "objectives": [' + s + "]}")



def changeObjective():
    id = int(text2)
    objective = text11
    cursor.execute("UPDATE objectives SET objective =? WHERE id =?", (objective, id))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def deleteObjective():
    id = int(text2)
    cursor.execute("DELETE FROM objectives WHERE id =" + str(id))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


# ================================================ Команды проектов


def addProject():
    id_user = int(text2)
    name = text3
    description = text12
    cursor.execute('INSERT INTO projects (id_user ,name, description, completed) VALUES (?,?,?,?)', (id_user, name, description, 0))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def getProject():
    id = int(text2)

    cursor.execute("SELECT * FROM projects WHERE id=?", [id])
    row = cursor.fetchall()

    data = {"id": str(row[0][0]), "id_user": str(row[0][1]), "name": str(row[0][2]), "description": str(row[0][3]), "completed": str(row[0][4])}
    s = json.dumps(data)
    print(s)


def getAllProjectsUser():
    id_user = int(text2)
    cursor.execute("SELECT * FROM projects WHERE id_user=?", [id_user])
    row = cursor.fetchall()
    i = 0
    while i < len(row):
        data = {"id": str(row[i][0]), "id_user": str(row[i][1]), "name": str(row[i][2]), "description": str(row[i][3]), "completed": str(row[i][4])}
        if len(row) - 1 == i and i != 0:
            s += json.dumps(data)
        elif i == 0 and len(row) - 1 == 0:
            s = json.dumps(data)
        elif i == 0:
            s = json.dumps(data) + ','
        else:
            s += json.dumps(data) + ','
        i = i + 1
    print('{ "projects": [' + s + "]}")



def changeProject():
    id = int(text2)
    name = text3
    description = text12
    cursor.execute("UPDATE projects SET name =?, description =? WHERE id =?", (name, description, id))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def setCompleteProject():
    id = text2
    completed = text14
    cursor.execute("UPDATE projects SET completed=? WHERE id =?", (eval(completed), id))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def deleteProject():
    id = int(text2)

    cursor.execute("DELETE FROM projects WHERE id =" + str(id))
    # / client_sock.sendall(str.encode("Done"))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


# ================================================ Команды наставников


def getMentors():
    cursor.execute("SELECT * FROM users WHERE role=?", ["IT"])
    mentors = cursor.fetchall()
    i = 0
    while i < len(mentors):
        data = {"id": str(mentors[i][0]), "secondname": mentors[i][3], "name": mentors[i][4], "patronymic": mentors[i][5], "role": str(mentors[i][6])}
        if len(mentors) - 1 == i and i != 0:
            s += json.dumps(data)
        elif i == 0 and len(mentors) - 1 == 0:
            s = json.dumps(data)
        elif i == 0:
            s = json.dumps(data) + ','
        else:
            s += json.dumps(data) + ','
        i = i + 1
    print('{ "mentors": [' + s + "]}")




# ================================================ Команды сокомандников


def addTeammate():
    id_project = int(text2)
    id_user = int(text13)
    cursor.execute('INSERT INTO teammates (idUser, idProject, role) VALUES (?,?,?)', (id_user, id_project, None))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def getTeammates():
    id = int(text2)
    cursor.execute("SELECT * FROM teammates WHERE idProject=?", [id])
    row = cursor.fetchall()
    i = 0
    while i < len(row):
        cursor.execute("SELECT * FROM users WHERE id=?", [int(str(row[i][1]))])
        teammates = cursor.fetchall()
        data = {"id": str(row[i][0]), "secondname": teammates[0][3], "name": teammates[0][4], "role": str(row[i][3]), "vk": str(teammates[i][8])}
        if len(row) - 1 == i and i != 0:
            s += json.dumps(data)
        elif i == 0 and len(row) - 1 == 0:
            s = json.dumps(data)
        elif i == 0:
            s = json.dumps(data) + ','
        else:
            s += json.dumps(data) + ','
        i = i + 1
    print('{ "teammates": [' + s + "]}")


# ================================================ Команды тестов


def createTest():
    name = text3
    data = text11
    questions = []
    answers = []
    correct = []
    data_ = ""
    j = 0
    i = 0
    answers_ = []
    correct_ = []
    while i < len(data):
        if data[i] != '/':
            data_ += data[i]
        else:
            if data[i + 1] == '/' and data[i + 2] == '/' and j == 2:
                correct_.append(data_)
                answers.append(answers_)
                correct.append(correct_)
                answers_ = []
                correct_ = []
                data_ = ""
                j = 0
                i = i + 2
            elif data[i + 1] == '/':
                if j == 0:
                    questions.append(data_)
                    data_ = ""
                    j = 1
                elif j == 1:
                    answers_.append(data_)
                    data_ = ""
                    j = 2
                elif j == 2:
                    correct_.append(data_)
                    data_ = ""
                    j = 1
                i = i + 1
        i = i + 1
    id = []
    id_ = ""
    for answer, corr in zip(answers, correct):
        for index in range(len(answer)):
            cursor.execute("INSERT INTO answers (answer, correct) VALUES (?,?)", (answer[index], corr[index]))
            id_ = id_ + str(cursor.lastrowid) + ','
        id_ = id_[:-1]
        id.append(id_)
        id_ = ""
    id_questions = ""
    for question, id_answers in zip(questions, id):
        cursor.execute("INSERT INTO questions (question, id_answers) VALUES (?,?)", (question, id_answers))
        id_questions = id_questions + str(cursor.lastrowid) + ','
    id_questions = id_questions[:-1]
    cursor.execute("INSERT INTO tests (name, id_questions) VALUES (?,?)", (name, id_questions))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def getTestsUser():
    id = text2
    cursor.execute("SELECT * FROM user_tests WHERE id_user=?", [id])
    tests = cursor.fetchall()
    i = 0
    while i < len(tests):
        id_answers = []
        id_answers_ = tests[i][4]
        idAnswers = ""
        l = 0
        while l < len(id_answers_):
            if id_answers_.find(",") == -1:
                k = 0
                while k < len(id_answers_):
                    idAnswers += id_answers_[k]
                    k = k + 1
                id_answers.append(int(idAnswers))
            elif l == len(id_answers_) - 1:
                idAnswers += id_answers_[l]
                id_answers.append(int(idAnswers))
            elif id_answers_[l] != ',':
                idAnswers += id_answers_[l]
            else:
                id_answers.append(int(idAnswers))
                idAnswers = ""
            l = l + 1
        progress = 0
        cursor.execute("SELECT * FROM tests WHERE id=?", [tests[i][2]])
        test = cursor.fetchall()

        id_question = []
        id_ = test[i][2]
        idQuest = ""
        l = 0
        while l < len(id_):
            if id_.find(",") == -1:
                k = 0
                while k < len(id_):
                    idQuest += id_[k]
                    k = k + 1
                id_question.append(int(idQuest))
            elif l == len(id_) - 1:
                idQuest += id_[l]
                id_question.append(int(idQuest))
            elif id_[l] != ',':
                idQuest += id_[l]
            else:
                id_question.append(int(idQuest))
                idQuest = ""
            l = l + 1
        l = 0
        while l < len(id_question):
            cursor.execute("SELECT * FROM questions WHERE id=?", [id_question[l]])
            question = cursor.fetchall()
            id_answer = []
            id_ = question[0][2]
            idAnsw = ""
            j = 0
            while j < len(id_):
                if id_.find(",") == -1:
                    k = 0
                    while k < len(id_):
                        idAnsw += id_[j]
                        k = k + 1
                    id_answer.append(int(idAnsw))
                elif j == len(id_) - 1:
                    idAnsw += id_[j]
                    id_answer.append(int(idAnsw))
                elif id_[j] != ',':
                    idAnsw += id_[j]
                else:
                    id_answer.append(int(idAnsw))
                    idAnsw = ""
                j = j + 1
            p = 0
            while p < len(id_answer):
                cursor.execute("SELECT * FROM answers WHERE id=?", [id_answer[p]])
                answer = cursor.fetchall()
                if len(id_answers) > 0:
                    if answer[0][2] == 1 and id_answers[l] == answer[0][0]:
                        progress = progress + 1
                p = p + 1
            l = l + 1
        if len(id_answers) > 0:
            progress = progress / len(id_answers) * 100
        data = {"id": str(test[0][0]), "name": test[0][1],
                "completed": tests[i][3], "progress": str(int(progress))}
        if len(tests) - 1 == i and i != 0:
            s += json.dumps(data)
        elif i == 0 and len(tests) - 1 == 0:
            s = json.dumps(data)
        elif i == 0:
            s = json.dumps(data) + ','
        else:
            s += json.dumps(data) + ','
        i = i + 1
    print('{ "tests": [' + s + "]}")

def getTest():
    id = text2
    cursor.execute("SELECT * FROM tests WHERE id=?", [id])
    test = cursor.fetchall()
    q = ""
    t = ""
    id_question = []
    id_ = test[0][2]
    idQuest = ""
    i = 0
    while i < len(id_):
        if id_.find(",") == -1:
            k = 0
            while k < len(id_):
                idQuest += id_[k]
                k = k + 1
            id_question.append(int(idQuest))
        elif i == len(id_) - 1:
            idQuest += id_[i]
            id_question.append(int(idQuest))
        elif id_[i] != ',':
            idQuest += id_[i]
        else:
            id_question.append(int(idQuest))
            idQuest = ""
        i = i + 1
    i = 0
    while i < len(id_question):
        cursor.execute("SELECT * FROM questions WHERE id=?", [id_question[i]])
        question = cursor.fetchall()
        id_answer = []
        id_ = question[0][2]
        idAnsw = ""
        j = 0
        while j < len(id_):
            if id_.find(",") == -1:
                k = 0
                while k < len(id_):
                    idAnsw += id_[j]
                    k = k + 1
                id_answer.append(int(idAnsw))
            elif j == len(id_) - 1:
                idAnsw += id_[j]
                id_answer.append(int(idAnsw))
            elif id_[j] != ',':
                idAnsw += id_[j]
            else:
                id_answer.append(int(idAnsw))
                idAnsw = ""
            j = j + 1
        p = 0
        while p < len(id_answer):
            cursor.execute("SELECT * FROM answers WHERE id=?", [id_answer[p]])
            answer = cursor.fetchall()
            data = {"id": str(answer[0][0]), "answer": answer[0][1],
                    "correct": answer[0][2]}
            if len(id_answer) - 1 == p and p != 0:
                s += json.dumps(data)
            elif p == 0 and len(id_answer) - 1 == 0:
                s = json.dumps(data)
            elif p == 0:
                s = json.dumps(data) + ','
            else:
                s += json.dumps(data) + ','
            p = p + 1
        q += '{"id": ' + str(question[0][0]) + ', "question": "' + question[0][1] + '", "answers": [' + s + ']}'
        if i != len(id_question) - 1:
            q += ','
        i = i + 1
    q = '{"tests": [{"id": ' + str(test[0][0]) + ', "name": "' + test[0][1] + '", "questions": [' + q + "]}]}"
    print(q)


def sendTest():
    id_user = text2
    id_test = text13
    id_answers = text11
    cursor.execute("UPDATE user_tests SET id_answers=?, completed=? WHERE id_user=? AND id_test=?", (id_answers, 1, id_user, id_test))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


# ================================================

# Клиент отключился

data = text1

if data == "test":
    test()
if data == "js":
    js()
if data == "login":
    if text4 != "" and text5 != "":
        login()
    else:
        htmlWrite("Error")
if data == "allUsers":
    allUsers()
if data == "getUser":
    getUser()
if data == "getStudents":
    getStudents()
if data == "getTimeGroup":
    getTimeGroup()
if data == "addUser":
    if text3 != "" and text4 != "" and text5 != "" and text6 != "":
        addUser()
    else:
        htmlWrite("Error")
if data == "changeUserPassword":
    if text2 != "" and text5 != "":
        changeUserPassword()
    else:
        htmlWrite("Error")

if data == "addComponent":
    if text3 != "" and text8 != "":
        addComponent()
    else:
        htmlWrite("Error")
if data == "addAllComponents":
    addAllComponents()
if data == "getComponent":
    if text2 != "setCheckObjective":
        getComponent()
    else:
        htmlWrite("Error")
if data == "getComponentByComponentProject":
    getComponentByComponentProject()
if data == "getAllComponents":
    getAllComponents()
if data == "changeComponent":
    if text2 != "" and text3 != "" and text9 != "" and text10 != "":
        changeComponent()
    else:
        htmlWrite("Error")
if data == "setImageComponent":  # ДОПИСАТЬ
    setImageComponent()
if data == "deleteComponent":
    if text2 != "":
        deleteComponent()
    else:
        htmlWrite("Error")

if data == "addComponentProject":
    addComponentProject()
if data == "getComponentsProject":
    getComponentsProject()
if data == "deleteComponentProject":
    deleteComponentProject()
if data == "changeNumberComponentProject":
    changeNumberComponentProject()

if data == "addObjective":
    addObjective()
if data == "setCheckObjective":
    setCheckObjective()
if data == "getObjective":
    getObjective()
if data == "getObjectivesProject":
    getObjectivesProject()
if data == "changeObjective":
    changeObjective()
if data == "deleteObjective":
    deleteObjective()

if data == "addProject":
    addProject()
if data == "getProject":
    getProject()
if data == "getAllProjectsUser":
    getAllProjectsUser()
if data == "changeProject":
    changeProject()
if data == "setCompleteProject":
    setCompleteProject()
if data == "deleteProject":
    deleteProject()

if data == "getMentors":
    getMentors()

if data == "addTeammate":
    addTeammate()
if data == "getTeammates":
    getTeammates()

if data == "createTest":
    createTest()
if data == "getTestsUser":
    getTestsUser()
if data == "getTest":
    getTest()
if data == "sendTest":
    sendTest()