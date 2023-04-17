#Llibreries
import os
import sys
import select
import random
import time
import csv

#Funció per esborrar la pantalla
def clear():
	if os.name == "nt":
		# Windows
		os.system("cls")
	else:
		# Mac i Linux
		os.system("clear")


#Funció per pausar el programa fins que l'usuari presioni la tecla enter
def press_enter():
	print("\n\n\n")
	input("Insereix per continuar... ")
	clear()


#Funció per determinar si la resposta és vàlida, i si és una lletra o una paraula
def validate(guess):
	
	allowed_symbols = [" ", "-"]
    
	if len(guess) == 1 and guess.isalpha():
		return "letter"
    
	elif len(guess) > 1 and all(c.isalpha() or c in allowed_symbols for c in guess):
		return "word"

	elif guess in allowed_symbols and guess != " ":
		return "symbol"
		
	else:
		return "invalid"

#Matrius per emmagatzemar les dades del fitxer "penjat.csv"
words = []
definitions = []
points = []

#Parser CSV
with open('penjat.csv', newline='') as file:
	reader = csv.DictReader(file)
	QuestionCount = 0
	for row in reader:
		QuestionCount = QuestionCount + 1
		words.append(row['Paraula'])
		definitions.append(row['Definició'])
		points.append(row['Puntuació'])


#Funció principal del joc
def game():
	#Barreja de preguntes
	Questions = list(range(QuestionCount))
	random.shuffle(Questions)

	#Control de temps
	timeLimit = 60
	start_time = time.time()
	end_time = start_time + timeLimit

	#Bucle del joc
	i = 0
	while time.time() < end_time:
		clear()
		answer = words[Questions[i]].lower()
		guessed_letters = []
		lines = []
		for char in answer:
			if char == " ":
				lines.append(" ")
			else:
				lines.append("_")
		while True:
			clear()
			
			time_left = int(end_time - time.time())
			
			print("Temps restant:", time_left, "segons")
			print("-"*25, "\n")
			print("Paraula", i+1,"\n")
			print("Definició:", definitions[Questions[i]])
			print("\n(", points[Questions[i]], "punts )\n")
			print(" ".join(lines))
			print("\nLletres provades:", guessed_letters)
			print("\nParaula o lletra:\n")
			#print("[DEBUG]", answer)

			if "_" not in lines:
						print("Resposta correcta!")
						time.sleep(1)
						break
			
			input_ready, _, _ = select.select([sys.stdin], [], [], time_left)
			
			if input_ready:
				guess = input().lower()
				guess_type = validate(guess)
				
				if guess_type == "invalid":
					print("Error: Si us plau, insereix una lletra o la paraula")
					time.sleep(1)
					clear()
				
				if guess_type == "letter" or guess_type == "symbol":
					if guess in answer:
						for x in range(len(answer)):
							if answer[x] == guess:
								lines[x] = guess
								
					else:
						print("Lletra incorrecta:")
						time.sleep(1)
						
					guessed_letters.append(guess)
				
				elif guess_type == "word":
					
					if guess.lower() == answer:
						print(("Resposta correcta! "))
						time.sleep(1)
						
					else:
						print("Resposta incorrecta: ")
						time.sleep(1)
					break
			
			else:
				clear()
				print("El temps s'ha acabat!")
				press_enter()
				break

		i += 1
		if i >= len(Questions):
			
			clear()
			print("Has respost totes les preguntes!")
			press_enter()
			break
			
	scores()

def scores():
	clear()
	print("╔═════════════════════════════════════════════════════════════════════════════╗")                     
	print("║  _____  _    _ _   _ _______ _    _         _____ _____ ____  _   _  _____  ║▒")
	print("║ |  __ \| |  | | \ | |__   __| |  | |  /\   / ____|_   _/ __ \| \ | |/ ____| ║▒")
	print("║ | |__) | |  | |  \| |  | |  | |  | | /  \ | |      | || |  | |  \| | (___   ║▒")
	print("║ |  ___/| |  | | . ` |  | |  | |  | |/ /\ \| |      | || |  | | . ` |\___ \  ║▒")
	print("║ | |    | |__| | |\  |  | |  | |__| / ____ \ |____ _| || |__| | |\  |____) | ║▒")
	print("║ |_|     \____/|_| \_|  |_|   \____/_/    \_\_____|_____\____/|_| \_|_____/  ║▒")
	print("║                                                                             ║▒")
	print("╠═════════════════════════════════════════════════════════════════════════════╣▒")
	print("║                                                                             ║▒")
	print("║                              1. Ranking general                             ║▒")
	print("║                           2. Puntuacions personals                          ║▒")
	print("║                                   3. Sortir                                 ║▒")
	print("║                                                                             ║▒")
	print("╚═════════════════════════════════════════════════════════════════════════════╝▒")
	print("  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
	print("                                                                                ")
	press_enter()
	clear()


#Funció per sortir del programa
def exit():
	clear()
	print("╔══════════════════════════════════╗")
	print("║           Fins aviat!            ║")
	print("╚══════════════════════════════════╝")
	time.sleep(1)
	sys.exit()


#Menú principal
while True:
	clear()
	print("╔═══════════════════════════════════════════════════════════╗")
	print("║  ______ _        _____  ______ _   _      _      _______  ║▒")
	print("║ |  ____| |      |  __ \|  ____| \ | |    | |  /\|__   __| ║▒")
	print("║ | |__  | |      | |__) | |__  |  \| |    | | /  \  | |    ║▒")
	print("║ |  __| | |      |  ___/|  __| | . ` |_   | |/ /\ \ | |    ║▒")
	print("║ | |____| |____  | |    | |____| |\  | |__| / ____ \| |    ║▒")
	print("║ |______|______| |_|    |______|_| \_|\____/_/    \_\_|    ║▒")
	print("║                                                           ║▒")
	print("╠═══════════════════════════════════════════════════════════╣▒")
	print("║                                                           ║▒")
	print("║                         ┌───┐                             ║▒")
	print("║                         │   │                             ║▒")
	print("║                         O   │                             ║▒")
	print("║                        /|\  │                             ║▒")
	print("║                        / \  │                             ║▒")
	print("║                             │                             ║▒")
	print("║                        ─────┴──                           ║▒")
	print("║                                                           ║▒")
	print("╠═══════════════════════════════════════════════════════════╣▒")
	print("║                                                           ║▒")
	print("║                     1. Jugar                              ║▒")
	print("║                     2. Puntuacions                        ║▒")
	print("║                     3. Sortir                             ║▒")
	print("║                                                           ║▒")
	print("╠═══════════════════════════════════════════════════════════╣▒")
	print("║                         MENU                              ║▒")
	print("╚═══════════════════════════════════════════════════════════╝▒")
	print("  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
	print("                                                             ")

	opcio = input("Selecciona una opció: ")

	if opcio == "1":
		game()
	elif opcio == "2":
		scores()
	elif opcio == "3":
		exit()
	else:
		print("\nOpció no vàlida. Si us plau, selecciona una opció del menú.\n")
		time.sleep(1)
