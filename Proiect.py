from numpy import random
import statistics
import matplotlib.pyplot as plt



#Functie pentru calcularea fitnessului
def fitness(crom):
    fitness=0
    for i in range(n-1):
        fitness+=1/distanta[crom[i]][crom[i+1]]
    fitness += 1 / distanta[crom[0]][crom[n-1]]
    return fitness

#Functie pentru selectarea stohastica universala a unui parinte
def stohastica_universala(populatie):
    suma_fitness=0
    for i in range(nrPopulatie):
        suma_fitness+=fitness(populatie[i])
    segment=[]
    start=0
    for i in range(nrPopulatie):
        sfarsit = round((start+fitness(populatie[i])/suma_fitness),4)
        segment.append((start,sfarsit))
        start=sfarsit

    nr=random.random()
    for i,zona in enumerate(segment):
        if zona[0] <= nr < zona[1]:
            #print(populatie[i])
            return populatie[i]

#Functie pentru selectarea stohastica a listei de parinti
def selectie_stohastica_universala(populatie,nrParinti):
    lista_parinti=[]
    for i in range(nrParinti):
        parinte=stohastica_universala(populatie)
        lista_parinti.append(parinte)
    return lista_parinti

#Funtii pentru realizarea selectiilor turnir
def castigator_turneu(turneu):
    best=0
    for i in range(len(turneu)):
        if fitness(turneu[best])<fitness(turneu[i]):
            best=i
    #populatie.remove(turneu[best])
    #print(turneu[best])
    return turneu[best]

def selectia_turnir(marime):
    turneu=[]
    for i in range(marime):
        nr=random.randint(len(populatie))
        turneu.append(populatie[nr])
    return castigator_turneu(turneu)

#Functia pentru calcularea mediei si dispersiei

def desen_media_dispersia(media, dispersia):
    plt.scatter(media, dispersia)
    plt.xlabel('Media')
    plt.ylabel('Dispersia')
    plt.suptitle('Media si dispersia')
    plt.show()

def media_dispersia(populatie):
    valori_fitness=[]
    for i in range(nrPopulatie):
        valori_fitness.append(fitness(populatie[i]))
    media=sum(valori_fitness)/nrPopulatie
    dispersie = statistics.stdev(valori_fitness)
    return media,dispersie


#Lista oraselor
orase=["Craiova","Ramnicu Valcea","Slatina","Caracal"
    ,"Calafat","Targu Jiu","Turnu Severin","Dragasani","Filiasi"]

#Matricea cu distantele dintre orase
distanta=[
[0,127,50,54,89,108,111,72,37],
[127,0,89,120,215,115,207,48,136],
[50,89,0,41,137,159,162,33,87],
[54,120,41,0,138,161,164,64,89],
[89,215,137,138,0,195,99,159,124],
[108,115,159,161,195,0,95,133,72],
[111,207,162,164,99,95,0,184,75],
[72,48,33,64,159,133,184,0,109],
[37,136,87,89,124,72,75,109,0]
]

#Initializarea populatiei
populatie=[]
nrPopulatie=100
n=len(orase)
l_medie=[]
l_dispersie=[]

for i in range(nrPopulatie):
    crom=list(range(n))
    random.shuffle(crom)
    populatie.append(crom)

for k in range(100):
    #Selectia stohastica universala a parintilor
    nrParinti=20
    lista_parinti=selectie_stohastica_universala(populatie,nrParinti)

    #Incrucisarea parintilor folosind incrucisarea de ordine
    copii=[]
    i=0
    while i<(len(lista_parinti)-1):
        copil1=[]
        copil2=[]

        ok=1
        while ok:
               t1=random.randint(0,n-2)
               t2=random.randint(0,n-2)
               if t1!=t2:
                      ok=0

        if t1>t2:
               t1=t1+t2
               t2=t1-t2
               t1=t1-t2

        j=0
        while j < n:
            if j<t1 or j>t2:
                copil1.append('*')
                copil2.append('*')
            else:
                copil1.append(lista_parinti[i][j])
                copil2.append(lista_parinti[i+1][j])

            j+=1

        aux1=[]
        aux2=[]
        for j in range(t2,n):
               aux1.append(lista_parinti[i][j])
               aux2.append(lista_parinti[i+1][j])
        for j in range(t2):
               aux1.append(lista_parinti[i][j])
               aux2.append(lista_parinti[i+1][j])

        j=t2+1
        capat=n
        while j<capat:
            while (aux2[0] in copil1):
                aux2.pop(0)
            while (aux1[0] in copil2):
                aux1.pop(0)
            copil1[j]=aux2[0]
            copil2[j]=aux1[0]
            aux1.pop(0)
            aux2.pop(0)
            if(j==n-1):
                j=-1
                capat=t1
            j+=1

        copii.append(copil1)
        copii.append(copil2)
        i+=2


    #Mutatia specifica prin schimbare

    pb_mutatie=0.2

    for i in range(len(copii)):
        pb_mutatie_copil=random.uniform(0,1)
        if pb_mutatie_copil<pb_mutatie:
            gena1=random.randint(n)
            gena2=random.randint(n)
            while gena1==gena2:
                gena1 = random.randint(n)
                gena2 = random.randint(n)
            t=copii[i][gena1]
            copii[i][gena1]=copii[i][gena2]
            copii[i][gena2]=t

    #Adaugam copiii in populatie

    while copii:
        populatie.append(copii[0])
        copii.pop(0)

    #Formam populatia noua utilizand selectia turninr

    populatie_noua=[]
    marime_turnir=3
    for i in range(nrPopulatie):
        populatie_noua.append(selectia_turnir(marime_turnir))

    populatie=[]
    populatie.extend(populatie_noua)

    #Afisarea mediei si a dispersiei
    medie,dispersie=media_dispersia(populatie)
    l_medie.append(medie)
    l_dispersie.append(dispersie)
    print("Media: ",medie)
    print("Dispersia: ",dispersie,end='\n\n')

desen_media_dispersia(l_medie,l_dispersie)