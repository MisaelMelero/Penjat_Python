#!/usr/bin/env python3

#Llibreries
import heapq
import datetime
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


def login():
	clear()
	username = input("Insereix el teu nom: ")
	return username


#Funció per determinar si la resposta és vàlida, i si és una lletra o una paraula
def validate(guess):

	allowed_symbols = [" ", "-"]

	if len(guess) == 1 and guess.isalpha():
		return "letter"

	elif len(guess) > 1 and all(c.isalpha() or c in allowed_symbols
	                            for c in guess):
		return "word"

	elif guess in allowed_symbols and guess != " ":
		return "symbol"

	else:
		return "invalid"


#Funció per mostrar la puntuació de l'usuari després de la partida
def stats_display(a, b, c, d, e):
	print("╔═══════════════════════════════════════════════════════════╗")
	print("║                                                           ║▒")
	print("║                  Final de la partida                      ║▒")
	print("║                                                           ║▒")
	print(f"║                  Puntuació final:       {a:03d}               ║▒")
	print("║                                                           ║▒")
	print(f"║                  Lletres correctes:      {b:02d}               ║▒")
	print(f"║                  Respostes correctes:    {d:02d}               ║▒")
	print(f"║                  Lletres incorrectes:     {c:01d}               ║▒")
	print(f"║                  Respostes incorrectes:   {e:01d}               ║▒")
	print("║                                                           ║▒")
	print("╚═══════════════════════════════════════════════════════════╝▒")
	print("  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")


def save_user_stats(username, a, b, c, d, e):
    # Crea un diccionari amb les dades de l'usuari per guardar-les en el fitxer CSV
    game_stats = {
        'username': username,
        'player_score': a,
        'correct_letters': b,
        'incorrect_letters': c,
        'correct_words': d,
        'incorrect_words': e,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Comprova si el fitxer CSV ja existeix
    if os.path.isfile(f"{username}.csv"):
        # Si ja existeix, afegeix les dades al final del fitxer
        with open(f"{username}.csv", mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=game_stats.keys())
            writer.writerow(game_stats)
    else:
        # Si no existeix, crea el fitxer amb les dades del capçalera i la primera fila
        with open(f"{username}.csv", mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=game_stats.keys())
            writer.writeheader()
            writer.writerow(game_stats)


def save_leaderboard_stats(username, player_score):
    leaderboard_file = "leaderboard.csv"

    if not os.path.isfile(leaderboard_file):
        with open(leaderboard_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'player_score'])

    scores = []
    with open(leaderboard_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            scores.append({'username': row['username'], 'player_score': int(row['player_score'])})

    scores.append({'username': username, 'player_score': player_score})

    top_scores = heapq.nlargest(10, scores, key=lambda s: s['player_score'])

    with open(leaderboard_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'player_score'])
        for score in top_scores:
            writer.writerow([score['username'], score['player_score']])


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
def game(username):
	player_name = username
	#Barreja de preguntes
	Questions = list(range(QuestionCount))
	random.shuffle(Questions)

	#Control de temps
	timeLimit = 60
	start_time = time.time()
	end_time = start_time + timeLimit

	error_count = 0  # Comptador d'errors

	player_score = 0  # Puntuació del jugador
	correct_letters = 0  # Comptador de lletres correctes
	incorrect_letters = 0  # Comptador de lletres incorrectes
	correct_words = 0  # Comptador de paraules correctes
	incorrect_words = 0  # Comptador de paraules incorrectes

	#Bucle del joc
	i = 0
	while time.time() < end_time:
		clear()
		answer = words[Questions[i]].lower()
		word_score = int(points[Questions[i]])
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

			print("╔═══════════════════════════════════════════════════════════╗")
			print("║                                                           ║▒")
			print(
			 f"║                 Temps restant: {time_left:02d} segons                  ║▒"
			)
			print(
			 f"║                   Puntuació: {player_score:03d} punts                    ║▒"
			)
			print("║                                                           ║▒")
			print("╚═══════════════════════════════════════════════════════════╝▒")
			print("  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
			print("                                       ")

			print(f"Paraula {i+1}\n")
			print("Definició:", definitions[Questions[i]])
			print(f"\n({word_score} punts)\n")

			if error_count == 0:
				print(" ┌───┐  ")
				print(" │   │  ")
				print("     │  ")
				print("     │  ")
				print("     │  ")
				print("     │  ")
				print("─────┴──")
			elif error_count == 1:
				print(" ┌───┐  ")
				print(" │   │  ")
				print(" O   │  ")
				print("     │  ")
				print("     │  ")
				print("     │  ")
				print("─────┴──")
			elif error_count == 2:
				print(" ┌───┐  ")
				print(" │   │  ")
				print(" O   │  ")
				print(" |   │  ")
				print("     │  ")
				print("     │  ")
				print("─────┴──")
			elif error_count == 3:
				print(" ┌───┐  ")
				print(" │   │  ")
				print(" O   │  ")
				print("/|   │  ")
				print("     │  ")
				print("     │  ")
				print("─────┴──")
			elif error_count == 4:
				print(" ┌───┐  ")
				print(" │   │  ")
				print(" O   │  ")
				print("/|\  │  ")
				print("     │  ")
				print("     │  ")
				print("─────┴──")
			elif error_count == 5:
				print(" ┌───┐  ")
				print(" │   │  ")
				print(" O   │  ")
				print("/|\  │  ")
				print("/    │  ")
				print("     │  ")
				print("─────┴──")
			elif error_count == 6:
				break

			print(" ".join(lines))

			print("\nLletres provades:", guessed_letters)
			print("\nParaula o lletra:\n")
			#print("[DEBUG]", answer)

			if "_" not in lines:
				print("Resposta correcta!")
				correct_words += 1
				player_score += word_score  # Incrementar la puntiació del jugador
				time.sleep(1)
				break

			input_ready, _, _ = select.select([sys.stdin], [], [], time_left)

			if input_ready:
				guess = input().lower()
				guess_type = validate(guess)

				if guess_type == "invalid":

					print("Error: Si us plau, insereix una lletra o la paraula\n")

					time.sleep(1)
					clear()

				if guess_type == "letter" or guess_type == "symbol":

					# Evitar lletres duplicades (per estadístiques i per evitar múltiples errors)
					if guess in guessed_letters:
						print("Ja heu provat aquesta lletra.")
						time.sleep(1)

					elif guess in answer and guess not in guessed_letters:
						correct_letters += 1
						for x in range(len(answer)):
							if answer[x] == guess:
								lines[x] = guess
						guessed_letters.append(guess)

					else:
						print("Lletra incorrecta :(")
						incorrect_letters += 1
						error_count += 1  # augmenta el comptador d'errors
						player_score -= 1  # -1 punt per lletra incorrecta
						if player_score <= 0:
							player_score = 0  # Per evitar puntuacions negatives
						time.sleep(1)
						guessed_letters.append(guess)

				elif guess_type == "word":

					if guess.lower() == answer:

						print("Resposta correcta!\n")
						correct_words += 1
						player_score += word_score  # Incrementar la puntiació del jugador
						time.sleep(1)

					else:
						print("Resposta incorrecta :(\n")
						incorrect_words += 1
						error_count += 1
						player_score -= 5  # -5 punts per paraula incorrecta
						if player_score <= 0:
							player_score = 0  # Per evitar puntuacions negatives
						time.sleep(1)

					break

			else:
				clear()
				print("El temps s'ha acabat!\n\n\n")
				time.sleep(1)
				stats_display(player_score, correct_letters, incorrect_letters,
				              correct_words, incorrect_words)
				save_user_stats(player_name, player_score, correct_letters, incorrect_letters, correct_words, incorrect_words)
				save_leaderboard_stats(player_name, player_score)
				
				press_enter()
				break

		i += 1
		if i >= len(Questions):

			clear()
			print("Has respost totes les preguntes!\n\n\n")
			time.sleep(1)
			stats_display(player_score, correct_letters, incorrect_letters,
			              correct_words, incorrect_words)
			save_user_stats(player_name, player_score, correct_letters, incorrect_letters, correct_words, incorrect_words)
			save_leaderboard_stats(player_name, player_score)
			press_enter()
			break

		if error_count == 6:
			clear()
			print(" ┌───┐  ")
			print(" │   │  ")
			print(" O   │  ")
			print("/|\  │  ")
			print("/ \  │  ")
			print("     │  ")
			print("─────┴──")
			print("\nPenjat!!!\n\n\n")
			time.sleep(1)
			stats_display(player_score, correct_letters, incorrect_letters,
			              correct_words, incorrect_words)
			save_user_stats(player_name, player_score, correct_letters, incorrect_letters, correct_words, incorrect_words)
			save_leaderboard_stats(player_name, player_score)
			press_enter()
			break

def leaderboard():
	clear()
	# Comprova si el fitxer de puntuacions existeix
	scores_filename = "leaderboard.csv"
	if not os.path.isfile(scores_filename):
			print("No s'ha trobat el fitxer de puntuacions.")
			return
	
	# Llegeix les puntuacions del fitxer
	scores = []
	with open(scores_filename, mode='r', newline='') as csv_file:
			reader = csv.DictReader(csv_file)
			for row in reader:
					scores.append((int(row['player_score']), row['username']))
	
	# Ordena les puntuacions per puntuació, de més gran a més petit
	sorted_scores = sorted(scores, reverse=True)
	
	# Imprimeix les puntuacions en un tauler ASCII
	print("TOP 10 JUGADORS")
	print("================")
	
	print("|{:<4}|{:<20}|{:<10}|".format("POS.", "JUGADOR", "PUNTS"))
	print("-" * 36)
	
	for i, (score, username) in enumerate(sorted_scores[:10]):
			print("|{:<4}|{:<20}|{:<10}|".format(i + 1, username, score))
	
	print("================")

def user_scores(username):
	clear()
	try:
		with open(username + '.csv') as f:
			reader = csv.DictReader(f)
			print(f"\nPartides de {username}:")
			print('-' * 60)
			for row in reader:
				print(
				 f"Data i hora: {row['timestamp']}\n - Puntuació: {row['player_score']}\n - Lletres correctes: {row['correct_letters']}\n - Lletres incorrectes: {row['incorrect_letters']}\n - Paraules correctes: {row['correct_words']}\n - Paraules incorrectes: {row['incorrect_words']}"
				)
				print('-' * 60)
	except FileNotFoundError:
		print(f"No s'han trobat partides per {username}")

#Menú puntuacions
def scores(username):
	username = username
	while True:
		clear()
		print(
		 "╔═════════════════════════════════════════════════════════════════════════════╗"
		)
		print(
		 "║  _____  _    _ _   _ _______ _    _         _____ _____ ____  _   _  _____  ║▒"
		)
		print(
		 "║ |  __ \| |  | | \ | |__   __| |  | |  /\   / ____|_   _/ __ \| \ | |/ ____| ║▒"
		)
		print(
		 "║ | |__) | |  | |  \| |  | |  | |  | | /  \ | |      | || |  | |  \| | (___   ║▒"
		)
		print(
		 "║ |  ___/| |  | | . ` |  | |  | |  | |/ /\ \| |      | || |  | | . ` |\___ \  ║▒"
		)
		print(
		 "║ | |    | |__| | |\  |  | |  | |__| / ____ \ |____ _| || |__| | |\  |____) | ║▒"
		)
		print(
		 "║ |_|     \____/|_| \_|  |_|   \____/_/    \_\_____|_____\____/|_| \_|_____/  ║▒"
		)
		print(
		 "║                                                                             ║▒"
		)
		print(
		 "╠═════════════════════════════════════════════════════════════════════════════╣▒"
		)
		print(
		 "║                                                                             ║▒"
		)
		print(
		 "║                           1. Ranking general                                ║▒"
		)
		print(
		 "║                           2. Puntuacions personals                          ║▒"
		)
		print(
		 "║                           3. Menú principal                                 ║▒"
		)
		print(
		 "║                                                                             ║▒"
		)
		print(
		 "╚═════════════════════════════════════════════════════════════════════════════╝▒"
		)
		print(
		 "  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
		)
		print(
		 "                                                                                "
		)
	
		opcio_menu_2 = input("Selecciona una opció: ")
		if opcio_menu_2 == "1":
			leaderboard()
			press_enter()
		elif opcio_menu_2 == "2":
			user_scores(username)
			press_enter()
		elif opcio_menu_2 == "3":
			break
		else:
			print("\nOpció no vàlida. Si us plau, selecciona una opció del menú.\n")
			time.sleep(1)


#Funció per sortir del programa
def exit():
	clear()
	print("╔══════════════════════════════════╗")
	print("║           Fins aviat!            ║")
	print("╚══════════════════════════════════╝")
	time.sleep(1)
	clear()
	sys.exit()


def main():
	#Menú principal
	username = login()
	while True:
		clear()
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
		print("║                     3. Canviar usuari                     ║▒")
		print("║                     4. Sortir                             ║▒")
		print("║                                                           ║▒")
		print("╠═══════════════════════════════════════════════════════════╣▒")
		print(f"║                     MENU PRINCIPAL                        ║▒")
		print("╚═══════════════════════════════════════════════════════════╝▒")
		print("  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
		print("                                                             ")
		print(f"Benvingut, {username}!\n")

		opcio_menu_1 = input("Selecciona una opció: ")

		if opcio_menu_1 == "1":
			game(username)
		elif opcio_menu_1 == "2":
			scores(username)
		elif opcio_menu_1 == "3":
			username = login()
		elif opcio_menu_1 == "4":
			exit()
		else:
			print("\nOpció no vàlida. Si us plau, selecciona una opció del menú.\n")
			time.sleep(1)


main()