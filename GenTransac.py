from random import gauss
import random
import matplotlib.pyplot as plt
import math
from enum import Enum


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
        SHOPPPING = 6
        AUTRES = 7
        LOYER = 8
        ELECTRICITE = 9
        INTERNET = 10


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
def monthGenerator(listeTransactions,mois, annee, yearSalary):
    for j in range(1,math.floor(gauss(60,15))) :
            Transac = generatorTC(yearSalary)
            transactionFinale = Transaction(Transac, generatorType(Transac), mois ,annee)
            listeTransactions.append(transactionFinale)


##Génère les transactions pour 1 an
def yearGenerator(listeTransactions,annee, yearSalary):
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

    for i in range(len(Repart)):
        print("%s : %s"%(i,round(Repart[i],2)))

    labels='Alimentation','Loisirs','Multimedia','Restaurant','Retraits','Sante','Shoppping','Autres','Loyer','Electricité','Internet'
    sizes=[Repart[0]/Sum,Repart[1]/Sum,Repart[2]/Sum,Repart[3]/Sum,Repart[4]/Sum,Repart[5]/Sum,Repart[6]/Sum,Repart[7]/Sum,Repart[8]/Sum,Repart[9]/Sum,Repart[10]/Sum]

    plt.pie(sizes,labels=labels, autopct='%1.1f%%',shadow=True,startangle=90)

    plt.axis('equal')

    plt.savefig('PieChart01.png')
    plt.show()

#rndFactor + eleve = moins random --> 0-100 (10 = 10% de random)
def randomisationTransations(listeTransactions, rndFactor):
    indicator = -1
    rdm = random.randint(0, 4)
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
        rndTypeClient([TypeDepense.ALIMENTATION,TypeDepense.SHOPPPING], [TypeDepense.LOISIRS, TypeDepense.MULTIMEDIA])
    elif typeClient == 4:
        rndTypeClient([TypeDepense.RESTAURANTS,TypeDepense.SHOPPPING], [TypeDepense.ALIMENTATION, TypeDepense.AUTRES])
    elif typeClient == 5:
        rndTypeClient([TypeDepense.LOISIRS, TypeDepense.SHOPPPING], [TypeDepense.RESTAURANTS])
    elif typeClient == 6:
        rndTypeClient([TypeDepense.LOISIRS, TypeDepense.RESTAURANTS], [TypeDepense.MULTIMEDIA])
    elif typeClient == 7:
        rndTypeClient([TypeDepense.LOISIRS, TypeDepense.RESTAURANTS, TypeDepense.SHOPPPING], [TypeDepense.AUTRES])
    elif typeClient == 8:
        rndTypeClient([TypeDepense.MULTIMEDIA], [TypeDepense.SHOPPPING])

def rndTypeClient(listePlus, listeMoins):
    for lt in listeTransactions:
        if lt.type.value in listeMoins:
            rdm = random.randint(1, 6)
            rdm2 = random.randint(0, rdm)
            if rdm2 == 0:
                rdm3 = random.choice(listePlus)
                lt.type = TypeDepense(rdm3)
"""
0=unknown
1=student           +loisir, multimedia             -restaurant
2=entrepreneur      +restaurant, multimedia         -loisir
3=housemaid         +alimentation, shopping         -multimdeia, loisir
4=cadre             +restaurant, shopping           -autres, alimentation    
5=blue-collar       +loisir, shopping               -restaurant
6=retired           +loisir, restaurant             -multimedia
7=services          +loisir, restaurant, shopping   -autres
8=technician        +multimedia                     -shopping
"""



listeTransactions = []
yearGenerator(listeTransactions, 2019, 30000)
transactionsRegulieres(listeTransactions, 30000, 2019)
randomisationTransations(listeTransactions, 9)
randomisationTypeClient(listeTransactions, 8)

"""
for t in listeTransactions:
    print("Montant : %s Type : %s Date : %s/%s" % (t.valeur, t.type, t.mois, t.annee))
"""
CompteurTrans(listeTransactions)




#Affiche les dépense du mois ainsi que leur poste de dépense
'''for i in range(1,math.floor(gauss(60,15))) :
		Transac = generatorTC(30000)
		print("Montant : %s Type : %s"% (Transac, generatorType(Transac)))
'''

#Total des dépenses par mois puis par an
"""
totalYear = 0
for i in range(1, 13):
    totalMonth = 0
    for j in range(1,math.floor(gauss(60,15))) :
        totalMonth += generatorTC(30000)
    print(totalMonth)
    totalYear += totalMonth
print(totalYear)
"""
