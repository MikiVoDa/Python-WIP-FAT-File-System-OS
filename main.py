UA = 16 #dimensiunea unității de alocare exprimată în octeți(bytes)
Nr_UA = 4096 #numărul de unități de alocare de care dispune hard diskul
Dim_locatie_FAT = 2
Dim_ROOT = 64

# Dim_HDD = Nr_UA * UA #?
# HDD = []
# for i in range(Nr_UA):
#     HDD.append([0]*16)

#initializam hdd
HDD = [["00000000" for i in range(UA)] for j in range(Nr_UA)]

Dim_FAT = int((Nr_UA*Dim_locatie_FAT)/UA)

#initializam tabela fat
for i in range(int(Dim_FAT)):
    HDD[i] = ["00000001"] * 16

#initializam tabela root
for i in range(int(Dim_FAT), int(Dim_FAT)+int(Dim_ROOT)):
    HDD[i] = ["00000010"] * 16


#verificare daca un UA este liber
def isUAfree():
    for i in reversed(range(len(HDD))):
        if HDD[i][0] == "00000000":
            return i


#punerea filei pe hdd
def createFile(fileInfo):
    #spargem comanda in bucati cu care putem lucra
    fileInfo = fileInfo.split()
    fileName = fileInfo[1].split(".")[0]
    fileExtensie = fileInfo[1].partition(".")[2]
    fileSize = fileInfo[2]
    fileType = fileInfo[3]
    if len(fileInfo) == 5:
        fileFlag = fileInfo[4]

    #obtinem locul liber
    UALiber = isUAfree()

    #punem pe hdd fila creata
    for i in range(len(fileName)):
        HDD[UALiber][i] = fileName[i]
    for i in (range(8, 11)):
        j = i - 8
        HDD[UALiber][i] = fileExtensie[j]
    if int(fileSize) >= 10:
        for i in range(11, 13):
            j = i - 11
            HDD[UALiber][i] = fileSize[j]
    else:
        for i in range(12, 13):
            j = i - 12
            HDD[UALiber][i] = fileSize[j]
    for i in (range(13, 14)):
        HDD[UALiber][i] = UALiber
    if len(fileInfo) == 5:
        for i in (range(15, 16)):
            j = i - 15
            HDD[UALiber][i] = fileFlag[j]
    print("File created")


#stergerea filei de pe hdd
def deleteFile(fileInfo):
    #spargem comanda pentru a putea manipula numele filei
    fileInfo = fileInfo.split()
    fileName = fileInfo[1]
    #verifica daca am gasit sau nu fila
    deleteHere = 0
    for i in reversed(range(len(HDD))):
        if fileName+"0" in ''.join(HDD[i][:len(fileName)+1]):
            deleteHere = 1
    #inlocui cu 0-uri ca si cand ar fi gol
            HDD[i] = ["00000000" for i in range(UA)]
            break
    if deleteHere == 1:
        print("File deleted")
    else:
        print("File not found")


#afisare director cu toate filele
def showDirectory():
    empty = 1
    for i in reversed(range(len(HDD))):
        if "0" in HDD[i][0]:
            pass
        else:
            #daca avem o instanta atunci directory-ul nu este gol
            msg = ''.join(HDD[i][:8])
            print(f"--{msg.replace('0', '')}")
            empty = 0
    if empty == 1:
        print("Directory empty")


#procesare comenzi de la tastatura
done = 0
while not done:
    cmd = input("my_OS> ")
    if cmd == "help":
        print("help - shows commands")
        print("dir - shows directory")
        print("staus - shows the hdd")
        print("create - create a file")
        print("delete - deletes a file")
    elif cmd == "status":
            print(HDD)
    elif cmd == "dir":
        showDirectory()
    elif cmd == "help create":
        print("use 'create <name>.<exension> <size> <type> <attr>'")
    elif cmd == "create":
        print("use 'help create' to see the command")
    elif cmd.split(" ")[0] == "create":
        try:
            createFile(cmd)
        except:
            print("use 'help' to see the command list")
    elif cmd == "help delete":
        print("use 'delete <name>'")
    elif cmd == "delete":
        print("use 'help delete' to see the command")
    elif cmd.split(" ")[0] == "delete":
        try:
            deleteFile(cmd)
        except:
            print("use 'help delete' to see the command list")


    else:
        print("use 'help' to see the command list end")
