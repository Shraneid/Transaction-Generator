from tqdm.auto import tqdm
from random import gauss
import random
import matplotlib.pyplot as plt
import math
from enum import Enum
import pandas as pd

RANDOM_PERCENT = 10

##Classe sociale de l'individu
class TypeClasse(Enum):
    OUVRIERE = 1
    MOYENNE = 2
    AISEE = 3


##Postes de dépenses courantes
class TypeDepense(Enum):
        ALIMENTATION = 0
        LOISIRS = 1
        MULTIMEDIA = 2
        RESTAURANTS = 3
        RETRAITS = 4
        SANTE = 5
        SHOPPING = 6
        AUTRES = 7
        LOYER = 8
        ELECTRICITE = 9
        INTERNET = 10


##Jobs clients
class TypeClient(Enum):
        UNKNOWN = 0
        STUDENT = 1
        ENTREPRENEUR = 2
        HOUSEMAID = 3
        ADMIN = 4
        BLUECOLLAR = 5
        RETIRED = 6
        SERVICES = 7
        TECHNICIAN = 8
        SELFEMPLOYED = 9
        MANAGEMENT = 10
        UNEMPLOYED = 11

##Format d'une transaction
class Transaction:
    def __init__(self, valeur, type, mois, annee):
        self.valeur = valeur
        self.type = type
        self.mois = mois
        self.annee = annee


##Generateur transactions courantes
def generatorTC(yearlySalary):
    val = gauss((yearlySalary*0.75/12)*0.01, 60)
    if val < 0:
        val = gauss((yearlySalary/12)*0.001, 15)
        if val < 0:
            val = val * (-1)
    return round(val, 2)


##Generateur de type de transactions courantes
def generatorType(montant):
    rdm = random.randint(0, 115)
    if rdm < 20:
        typetransac = TypeDepense(0)
    elif 20 < rdm < 34:
        typetransac = TypeDepense(1)
    elif 34 < rdm < 47:
        typetransac = TypeDepense(2)
    elif 47 < rdm < 60:
        typetransac = TypeDepense(3)
    elif 60 < rdm < 63:
        typetransac = TypeDepense(4)
    elif 63 < rdm < 70:
        typetransac = TypeDepense(5)
    elif 70 < rdm < 85:
        typetransac = TypeDepense(6)
    elif 100 < rdm < 106:
        typetransac = TypeDepense(rdm - 100)
    else:
        typetransac = TypeDepense(7)
    if montant == -1:
        typetransac = TypeDepense(8)
    if montant == -2:
        typetransac = TypeDepense(9)
    if montant == -3:
        typetransac = TypeDepense(10)
    return typetransac


##Génère les transactions pour 1 mois
def monthGenerator(listeTransactions, mois, annee, yearSalary):
    for j in range(1,math.floor(gauss(60,15))) :
            Transac = generatorTC(yearSalary)
            transactionFinale = Transaction(Transac, generatorType(Transac), mois ,annee)
            listeTransactions.append(transactionFinale)


##Génère les transactions pour 1 an
def yearGenerator(listeTransactions, annee, yearSalary):
    for i in range(1, 13):
        monthGenerator(listeTransactions,i, annee, yearSalary)


##Ajoute les transactions régulières à la liste des transactions
def transactionsRegulieres(listeTransactions, yearlySalary, annee):
    loyer = loyerGenerator(yearlySalary)
    Internet = InternetGenerator()
    for i in range(1,13):
        transactionLoyer = Transaction(loyer, generatorType(-1), i, annee)
        listeTransactions.append(transactionLoyer)
        transactionElec=Transaction(ElecGenerator(loyer),generatorType(-2),i,annee)
        listeTransactions.append(transactionElec)
        transactionInternet=Transaction(Internet,generatorType(-3),i,annee)
        listeTransactions.append(transactionInternet)


##Génère un loyer à partir du salaire annuel
def loyerGenerator(yearlySalary):
		monthlysalary = yearlySalary/12
		loyer = gauss(monthlysalary/3, monthlysalary/12)
		return round(loyer,2)


##Génère une facture l'éléctricité à partir du loyer
def ElecGenerator(loyer):
		Elec = gauss(loyer*0.10, 10)
		return round(Elec, 2)


#Génère une facture d'internet/TV/Teléphone
def InternetGenerator():
		Internet = gauss(30, 10)
		return round(Internet, 2)


def CompteurTrans(listeTransactions):
    Repart = [0,0,0,0,0,0,0,0,0,0,0]
    Sum=0
    for t in listeTransactions:
        print("Montant : %s Type : %s Date : %s/%s"%(t.valeur,t.type,t.mois,t.annee))
        temp = t.type.value
        Repart[temp] = Repart[temp]+t.valeur
        Sum=Sum+t.valeur
    print(Sum)

#rndFactor + eleve = moins random --> 0-100 (10 = 10% de random)
def randomisationTransations(listeTransactions, rndFactor):
    indicator = -1
    rdm = random.randint(0, 3)
    if rdm == 0:
        indicator = 1
    elif rdm == 1:
        indicator = 2
    elif rdm == 2:
        indicator = 3
    elif rdm == 3:
        indicator = 6
    for lt in listeTransactions:
        if lt.type.value == 1 or lt.type.value == 2 or lt.type.value == 3:
            rdm2 = random.randint(0, rndFactor)
            if rdm2 == 0:
                lt.type = TypeDepense(indicator)


def randomisationTypeClient(listeTransactions, typeClient):
    if typeClient == 0:
        randomisationTransations(listeTransactions, 5)
    elif typeClient == 1:
        rndTypeClient([TypeDepense.LOISIRS,TypeDepense.MULTIMEDIA], [TypeDepense.SANTE])
    elif typeClient == 2:
        rndTypeClient([TypeDepense.MULTIMEDIA,TypeDepense.RESTAURANTS], [TypeDepense.LOISIRS])
    elif typeClient == 3:
        rndTypeClient([TypeDepense.ALIMENTATION,TypeDepense.SHOPPING], [TypeDepense.LOISIRS, TypeDepense.MULTIMEDIA])
    elif typeClient == 4:
        rndTypeClient([TypeDepense.RESTAURANTS,TypeDepense.SHOPPING], [TypeDepense.ALIMENTATION, TypeDepense.AUTRES])
    elif typeClient == 5:
        rndTypeClient([TypeDepense.LOISIRS, TypeDepense.SHOPPING], [TypeDepense.RESTAURANTS])
    elif typeClient == 6:
        rndTypeClient([TypeDepense.LOISIRS, TypeDepense.RESTAURANTS], [TypeDepense.MULTIMEDIA])
    elif typeClient == 7:
        rndTypeClient([TypeDepense.LOISIRS, TypeDepense.RESTAURANTS, TypeDepense.SHOPPING], [TypeDepense.AUTRES])
    elif typeClient == 8:
        rndTypeClient([TypeDepense.MULTIMEDIA], [TypeDepense.SHOPPING])
    elif typeClient == 9:
        rndTypeClient([TypeDepense.MULTIMEDIA, TypeDepense.SHOPPING], [TypeDepense.RESTAURANT, TypeDepense.AUTRE])
    elif typeClient == 10:
        rndTypeClient([TypeDepense.RESTAURANT, TypeDepense.MULTIMEDIA, TypeDepense.SANTE], [TypeDepense.SHOPPING])
    elif typeClient == 11:
        rndTypeClient([], [TypeDepense.RESTAURANTS, TypeDepense.MULTIMEDIA, TypeDepense.SHOPPING])

def rndTypeClient(listePlus, listeMoins):
    for lt in listeTransactions:
        if lt.type.value in listeMoins:
            rdm = random.randint(1, 6)
            rdm2 = random.randint(0, rdm)
            if rdm2 == 0:
                rdm3 = random.choice(listePlus)
                lt.type = TypeDepense(rdm3)
"""
UNKNOWN = 0
STUDENT = 1
ENTREPRENEUR = 2
HOUSEMAID = 3
ADMIN = 4
BLUE-COLLAR = 5
RETIRED = 6
SERVICES = 7
TECHNICIAN = 8
SELF-EMPLOYED = 9
MANAGEMENT = 10
UNEMPLOYED = 11
"""

def getJob(txt):
    switch={
        'admin.':TypeClient.ADMIN,
        'blue-collar':TypeClient.BLUECOLLAR,
        'entrepreneur':TypeClient.ENTREPRENEUR,
        'housemaid':TypeClient.HOUSEMAID,
        'management':TypeClient.MANAGEMENT,
        'retired':TypeClient.RETIRED,
        'self-employed':TypeClient.SELFEMPLOYED,
        'services':TypeClient.SERVICES,
        'student':TypeClient.STUDENT,
        'technician':TypeClient.TECHNICIAN,
        'unemployed':TypeClient.UNEMPLOYED,
        'unknown':TypeClient.UNKNOWN
    }
    return switch.get(txt,"bugged")

def generateTransactions():
    user_db = pd.read_csv("D:\\WORK\\PING\\Programming\\user_db.csv")
    data = user_db[["CustomerId", "EstimatedSalary", "job"]]
    print(data.head())

    allTransactions = []

    for index, row in data.iterrows():
        cid = row['CustomerId']
        salary = row['EstimatedSalary']
        job = getJob(row['job'])
        
        listeTransactions = []
        yearGenerator(listeTransactions, 2019, salary)
        transactionsRegulieres(listeTransactions, salary, 2019)
        randomisationTransations(listeTransactions, RANDOM_PERCENT)
        randomisationTypeClient(listeTransactions, job)

        for t in listeTransactions:
            allTransactions.append([cid, t.type, t.valeur, t.mois, t.annee])

    print(allTransactions[0:5])
    df = pd.DataFrame.from_records(allTransactions, columns=["CustomerId", "TransacationType", "Value", "Month", "Year"])
    df.to_csv("D:\\WORK\\PING\\Programming\\transactions.csv", index=False)

if __name__ == "__main__":
    generateTransactions()


    
