from requests import get

urlCode = open("code.txt", "r")
code = urlCode.read()
entriesNo = int(input("Enter number of entries :"))
reponse = get(f"http://app.objco.com:8099/?account={code}&limit={min([entriesNo, 5])}")
donneesJson = reponse.json()

tabMesures = []

capteurs = ["62182233", "06182660"]


def rendreTableau(hex, date, capteur):
    nouvTableau = [] # date, capteur, temperature, humidité, batterie, RSSI
    index = hex.find(capteur)

    nouvTableau.append(date)
    nouvTableau.append(int(capteur))
    nouvTableau.append(decryptHex(hex[index + 14:index + 18]))  # temperature
    nouvTableau.append(decryptHex(hex[index + 18:index + 20]))  # humidite
    nouvTableau.append(decryptHex(hex[index + 10:index + 14]))  # batterie
    nouvTableau.append(decryptHex(hex[index + 20:index + 22]))  # RSSI

    return nouvTableau


def decryptHex(hexerpt):  # convertir l'hexadecimal en decimal
    return int(hexerpt, 16)


def printMesureInfo(tab):
    print(f"Mesure prise le {tab[0]}, par le capteur {tab[1]} :")
    print(f"Température: {float(tab[2]) / 10} C")
    if tab[3] != 255:  # 255 = valeur nul
        print(f"Humidité: {tab[3]} %")
    print(f"Batterie: {tab[4] / 1000} V")
    print(f"RSSI: {tab[5]} DB")
    print("")


for element in donneesJson: #pour chaque string hexadecimal
    for capteur in capteurs: #créez une mesure pour chaque capteur proposé
        tabMesures.append(rendreTableau(element[1], element[2], capteur))


for mesure in tabMesures:
    printMesureInfo(mesure)
