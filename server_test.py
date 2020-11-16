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

# print("Content-Type: text/html\n")
# print("Server Active")

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
    #  print("<p>" + data + "</p>")
    print(data + "<br />")


#    print("<body>")
#   print(data+"\n")
# print("<p>TEXT_2: {}</p>".format(text2))
# print("""</body>
#   print("</html>")
# print("Content-Type: text/html;charset=UTF-8\n")

# ========================Временно, хахахаха, шутка, нет (да)
# print("Content-Type: text/html\n")
# print("<!DOCTYPE HTML>")
# print("<html>")
# print('''<head>
#            <meta charset="utf-8">
#        </head>''')
# print("</html>")
# print(text1)
# print("Content-Type: text/html;charset=UTF-8\n")
print("Content-Type: application/json\n")

conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()


# hostName = socket.gethostbyname('0.0.0.0')

# serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# serv_sock.bind((hostName, 8080))
# serv_sock.listen(10)

# ================================================


def test():
    # print("Content-Type: text/html\n")
    htmlWrite("Ok\n");
    # =    client_sock.sendall(str.encode("All Ok"))

    cursor.execute("INSERT INTO componentsProject (idProject, idComponent, count) VALUES (1,1,1)")
    print("All right")

    conn.commit()


def js():
    data = {"name": "Arduino", "count": "30"}
    s = json.dumps(data) + ','
    data = {"name": "Светодиоды", "count": "1000"}
    s += json.dumps(data)
    # data_ = {"components": [s]}
    # s = json.dumps(data_)
    print('{ "components": [' + s + "]}")


def login():
    cursor.execute("SELECT * FROM users")
    row = cursor.fetchall()

    # / data = client_sock.recv(1024)
    # / login = bytes.decode(data)
    login = text4
    # / data = client_sock.recv(1024)
    # / password = bytes.decode(data)
    password = text5
    #  print(password)
    i = 0
    connect = False
    while i < len(row):
        if login == row[i][1] and password == row[i][2]:
            # /   client_sock.sendall(str.encode("true"))
            # htmlWrite("true");
            mentor = 0
            if row[i][6] == "IT":
                mentor = 1
            data = {"request": "true", "id": str(row[i][0]), "mentor": mentor, "name": str(row[i][4]), "secondname": str(row[i][3]), "vk": str(row[i][8])}
            connect = True
        i = i + 1
    if not connect:
        # / client_sock.sendall(str.encode("false"))
        # htmlWrite("false");
        data = {"request": "false", "id": None, "mentor": 0, "name": "", "secondname": ""}
    s = json.dumps(data)
    print(s)


# ================================================ Команды пользователя


def allUsers():
    cursor.execute("SELECT * FROM users")
    row = cursor.fetchall()
    i = 0

    while i < len(row):
        # data = {"name": str(row[i][1]).replace("\n", ""), "count": str(row[i][2]), "image": str(row[i][4])}
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
    # / data = client_sock.recv(1024)
    # / login = bytes.decode(data)
    login = text4
    # data = client_sock.recv(1024)
    # password = bytes.decode(data)
    password = text5
    # / data = client_sock.recv(1024)
    # / surname = bytes.decode(data)
    secondname = text6
    # / data = client_sock.recv(1024)
    # / name = bytes.decode(data)
    name = text3
    # / data = client_sock.recv(1024)
    patronymic = bytes.decode(data)
    patronymic = text7

    cursor.execute('INSERT INTO users (login , password, surname, name, patronymic) VALUES (?,?,?,?,?)',
                   (login, password, secondname, name, patronymic))
    htmlWrite("Done")
    # client_sock.sendall(str.encode("Done"))
    conn.commit()


def changeUserPassword():
    # / data = client_sock.recv(1024)
    # / id = int(bytes.decode(data))
    id = int(text2)

    # / data = client_sock.recv(1024)
    # / password = bytes.decode(data)
    password = text5

    print(id)
    print(password)
    cursor.execute("UPDATE users SET password =? WHERE id =?", (password, id))
    # / client_sock.sendall(str.encode("Done"))
    htmlWrite("Done")
    conn.commit()


# ================================================ Комады компонентов


def addComponent():
    # / data = client_sock.recv(1024)
    # / name = bytes.decode(data)
    name = text3
    # / data = client_sock.recv(1024)
    # / allCount = bytes.decode(data)
    allCount = text8

    print(name)
    print(allCount)

    cursor.execute('INSERT INTO components (name , allCount, useCount) VALUES (?,?,?)', (name, allCount, 0))
    # / client_sock.sendall(str.encode("Done"))
    htmlWrite("Done")
    conn.commit()


def addAllComponents():
    f = open('Components.txt', 'r')

    i = 0
    name = []
    allCounts = []

    for line in f:
        #    print(line)
        if i % 2 == 0:
            name.append(line)
        else:
            allCounts.append(line)
        i = i + 1

    j = 0

    while j < len(name):
        cursor.execute("INSERT INTO components (name, allCount, useCount) VALUES (?, ?, ?)", (name[j], allCounts[j], 0))
        j = j + 1;

    # /client_sock.sendall(str.encode("Done"))
    conn.commit()


def getComponent():
    # /data = client_sock.recv(1024)
    # /id = int(bytes.decode(data))
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
    # = client_sock.sendall(str.encode(str(len(row))))
    while i < len(row):
        # =    client_sock.sendall(str.encode(str(row[i][0])))
        # =    client_sock.sendall(str.encode(row[i][1]))
        # =    client_sock.sendall(str.encode(str(row[i][2])))
        # =    client_sock.sendall(str.encode(str(row[i][3])))

        # временно htmlWrite(str(row[i][0]))
        # htmlWrite(str(row[i][1]))
        # htmlWrite(str(row[i][2]))
        # временно htmlWrite(str(row[i][3]))
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
    # data = {"components": [s]}
    # s = json.dumps(data)
    print('{ "components": [' + s + "]}")


def setImageComponent():
    image = text11
    id = int(text2)
    # cursor.execute("SELECT * FROM components WHERE id =?", [id])
    # row = cursor.fetchall()
    cursor.execute("UPDATE components SET image =? WHERE id =?", (image, id))
    htmlWrite("Done")
    conn.commit()


def changeComponent():
    # / data = client_sock.recv(1024)
    # / id = int(bytes.decode(data))
    id = int(text2)
    # / data = client_sock.recv(1024)
    # / name = bytes.decode(data)
    name = text3
    # / data = client_sock.recv(1024)
    # / allCount = int(bytes.decode(data))
    allCount = text9
    # / data = client_sock.recv(1024)
    # / useCount = int(bytes.decode(data))
    useCount = text10

    print(id)
    print(allCount)
    print(useCount)
    cursor.execute("UPDATE components SET name =?, allCount =?, useCount =? WHERE id =?",
                   (name, allCount, useCount, id))
    # / client_sock.sendall(str.encode("Done"))
    htmlWrite("Done")
    conn.commit()


def deleteComponent():
    # / data = client_sock.recv(1024)
    # / id = int(bytes.decode(data))
    id = int(text2)

    cursor.execute("DELETE FROM components WHERE id =" + str(id))
    # / client_sock.sendall(str.encode("Done"))
    htmlWrite("Done")
    conn.commit()


# ================================================ Команды компонентов проекта

# <<<<<<<<<<================================================================= ПРОВЕРИТЬ!
def addComponentProject():

    id_component = []
    count = []
    # data = client_sock.recv(1024)
    id_project = int(text2)
    # data = client_sock.recv(1024)
    id_component_ = text13
    # / data = client_sock.recv(1024)
    # / count = int(bytes.decode(data))
    count_ = text8
    # print("Search component")
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
   #print(id_component)
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
    # componentProject = cursor.fetchall()

    # if cursor.fetchall() != None:
    componentProject = cursor.fetchall()

    # print(componentProject)
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
                # print("Have component")
                haveComponent = True
            i = i + 1
        if not haveComponent:
            # print("Haven't component")
            cursor.execute("INSERT INTO componentsProject (idProject, idComponent, count) VALUES (?,?,?)",
                           (id_project, id_component[j], count[j]))

        cursor.execute("SELECT * FROM components WHERE id =?", [id_component[j]])
        component = cursor.fetchall()
        useCount = component[0][3]
        _useCount = useCount + count[j]
        cursor.execute("UPDATE components SET useCount =? WHERE id =?", (_useCount, id_component[j]))
        # print("Done")
        # / client_sock.sendall(str.encode("Done"))
        #htmlWrite("Done")
        conn.commit()
        j = j + 1
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)

#    cursor.execute("SELECT * projects WHERE id =?", (id_project))
#    project = cursor.fetchall()


def getComponentsProject():
    # / data = client_sock.recv(1024)
    # / id_project = int(bytes.decode(data))
    id_project = int(text2)

    #    print(id_project)
    #   cursor.execute("SELECT * componentsProject WHERE idProject =?", (id_project))
    cursor.execute("SELECT * FROM componentsProject WHERE idProject=?", [id_project])
    componentsProject = cursor.fetchall()
    #    print("...")
    # / client_sock.sendall(str.encode(str(len(componentsProject))))
   # htmlWrite(str(len(componentsProject)))
    # print(componentsProject)
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
        # /client_sock.sendall(str.encode(str(componentsProject[i][0])))
        # /client_sock.sendall(str.encode(str(componentsProject[i][1])))
        # /client_sock.sendall(str.encode(str(componentsProject[i][2])))
        # /client_sock.sendall(str.encode(str(componentsProject[i][3])))
        # htmlWrite(componentsProject[i][0])
        # htmlWrite(componentsProject[i][1])
        # htmlWrite(componentsProject[i][2])
        # htmlWrite(componentsProject[i][3])
        # print('\n')
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
    # / data = client_sock.recv(1024)
    # / name = bytes.decode(data)
    name = text3
    # data = client_sock.recv(1024)
    description = text12
    # print(name)
    # print(description)

    cursor.execute('INSERT INTO projects (id_user ,name, description, completed) VALUES (?,?,?,?)', (id_user, name, description, 0))
    # / client_sock.sendall(str.encode("Done"))
    #htmlWrite("Done")
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def getProject():
    # / data = client_sock.recv(1024)
    # / id = int(bytes.decode(data))
    id = int(text2)

    cursor.execute("SELECT * FROM projects WHERE id=?", [id])
    row = cursor.fetchall()

    data = {"id": str(row[0][0]), "id_user": str(row[0][1]), "name": str(row[0][2]), "description": str(row[0][3]), "completed": str(row[0][4])}
    s = json.dumps(data)
    print(s)
    '''
    id = int(text2)
    cursor.execute("SELECT * FROM projects WHERE id=?", [id])
    row = cursor.fetchall()
    teammates = str(row[0][4])
    id_user = []
    role = []
    st = ""
    i = 0
    k = 0

    while i < len(teammates):
        if teammates[i] == ";":
            role.append(st)
            k = 0
            st = ""
        elif teammates[i] == ",":
            if k == 0:
                id_user.append(st)
                st = ""
                k = 1
        elif k == 1 and i == len(teammates) - 1:
            st += teammates[i]
            role.append(st)
        else:
            st += teammates[i]
        i = i + 1
    i = 0
    #print(id_user)
    #print(role)
    while i < len(id_user):
        data = {"id": id_user[i], "role": role[i]}
        if len(row) - 1 == i and i != 0:
            s += json.dumps(data)
        elif i == 0 and len(row) - 1 == 0:
            s = json.dumps(data)
        elif i == 0:
            s = json.dumps(data) + ','
        else:
            s += json.dumps(data) + ','
        i = i + 1
    if i == 0:
        s = "null"
    team = s
    data = {"id": str(row[0][0]), "id_user": str(row[0][1]), "name": str(row[0][2]), "description": str(row[0][3]), "teammates": [], "completed": str(row[0][5])}
    s = json.dumps(data)
    print(s[:118])
    s.replace("[]", "["+team+"]")
    print(s)
    #  print(row[0][2])
    #  print(row[0][3])
    # / client_sock.sendall(str.encode(row[0][2]))
    # / client_sock.sendall(str.encode(row[0][3]))
    # htmlWrite(row[0][2])
    # htmlWrite(row[0][3])
    '''


def getAllProjectsUser():
    # / data = client_sock.recv(1024)
    # / id_user = int(bytes.decode(data))
    id_user = int(text2)
    cursor.execute("SELECT * FROM projects WHERE id_user=?", [id_user])
    row = cursor.fetchall()
    i = 0
    # /  client_sock.sendall(str.encode(str(len(row))))
    while i < len(row):
        # / client_sock.sendall(str.encode(str(row[i][0])))
        # / client_sock.sendall(str.encode(str(row[i][1])))
        # / client_sock.sendall(str.encode(row[i][2]))
        # / client_sock.sendall(str.encode(row[i][3]))

        # htmlWrite(row[i][0])
        # htmlWrite(row[i][1])
        # htmlWrite(row[i][2])
        # htmlWrite(row[i][3])
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
    # / data = client_sock.recv(1024)
    # / id = int(bytes.decode(data))
    id = int(text2)
    # / data = client_sock.recv(1024)
    # / name = bytes.decode(data)
    name = text3
    # data = client_sock.recv(1024)
    description = text12
    # print(id)
    # print(name)
    # print(description)
    cursor.execute("UPDATE projects SET name =?, description =? WHERE id =?", (name, description, id))
    # / client_sock.sendall(str.encode("Done"))
    # htmlWrite("Done")
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def setCompleteProject():
    id = text2
    completed = text14
    cursor.execute("UPDATE objectives SET checked=? WHERE id =?", (eval(completed), id))
    conn.commit()
    data = {"request": "ok"}
    s = json.dumps(data)
    print(s)


def deleteProject():
    # / data = client_sock.recv(1024)
    # / id = int(bytes.decode(data))
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



'''
def getTeammates():
    id_project = int(text2)
    cursor.execute("SELECT * FROM projects WHERE id =" + str(id_project))
    row = cursor.fetchall()
    teammates = str(row[0][4])
    i = 0
    while i < len(teammates):
        data = {"id": str(row[i][0]), "id_user": str(row[i][1]), "name": str(row[i][2]), "description": str(row[i][3])}
        if len(row) - 1 == i and i != 0:
            s += json.dumps(data)
        elif i == 0 and len(row) - 1 == 0:
            s = json.dumps(data)
        elif i == 0:
            s = json.dumps(data) + ','
        else:
            s += json.dumps(data) + ','
        i = i + 1
        if teammates[i] == ";":
 '''



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

"""

while True:

    # Бесконечно обрабатываем входящие подключения
    client_sock, client_addr = serv_sock.accept()
   # print("Content-Type: text/html\n")
    print('Connected by', client_addr)
    userLogin = False

    try:
        while True:
            # Пока клиент не отключился, читаем передаваемые
            # им данные и отправляем их обратно
            data = client_sock.recv(1024)
            data = bytes.decode(data)
            data = text1
            print(data)
            if not data:
                # Клиент отключился
                break
            if data == "test":
                test()
                break
            if data == "login":
                login()
                break
            if data == "allUsers":
                allUsers()
                break
            if data == "addUser":
                addUser()
                break
            if data == "changeUserPassword":
                changeUserPassword()
                break

            if data == "addComponent":
                addComponent()
                break
            if data == "addAllComponents":
                addAllComponents()
                break
            if data == "getComponent":
                getComponent()
                break
            if data == "getAllComponents":
                getAllComponents()
                break
            if data == "changeComponent":
                changeComponent()
                break
            if data == "deleteComponent":
                deleteComponent()
                break

            if data == "addComponentProject":
                addComponentProject()
                break
            if data == "getComponentsProject":
                getComponentsProject()
                break

            if data == "addProject":
                addProject()
                break
            if data == "getProject":
                getProject()
                break
            if data == "getAllProjectsUser":
                getAllProjectsUser()
                break
            if data == "changeProject":
                changeProject()
                break
            if data == "deleteProject":
                deleteProject()
                break
    except:
        print("User disconnected")
        # client_sock.sendall(str.encode(data))

    client_sock.close()
    print('Client disconnected', client_addr)
    """
