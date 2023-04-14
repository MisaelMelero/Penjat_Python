import csv
import random

paraules = []
definicions = []
puntuacions = []
with open("/media/apolo/PortableSSD/Arian/2nSMIX/M12/PYTHON/Projecte PYTHON/penjat.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        paraules.append(row[0])
        definicions.append(row[1])
        puntuacions.append(int(row[2]))

puntuacio_global = 0 # Inicialitzar la puntuació global a zero

def jugar():
    global puntuacio_global # Utilitzar la variable global

    index = random.randint(0, len(paraules) - 1)
    paraula = paraules[index]
    definicio = definicions[index]
    puntuacio = puntuacions[index]

    print(f'Definició: {definicio}')
    resposta = input('Quina és la paraula? ')

    if resposta.lower() == paraula.lower():
        puntuacio_global += puntuacio # Afegir puntuació a la puntuació global
        print(f'Correcte! Puntuació: {puntuacio}\n')
        print(f'Puntuació global: {puntuacio_global}\n') # Imprimir la puntuació global
        jugar()
    else:
        resposta = input('Incorrecte. Vols intentar-ho de nou? (sí/no) ')
        if resposta.lower() == 'sí':
            jugar()
        else:
            print(f'La teva puntuació final és: {puntuacio_global}\n')
            print('Fins la pròxima!')

jugar()
