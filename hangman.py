import json
import random
# personal prefixes: words,scrabble
prefix = "scrabble"
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
# if true, takes a json file named prefix_dictonary.json that is a list of words and converts into prefix_alphadata.json which contains all the data needed to run the game efficently
# if false takes a json file named prefix_alphadata.json which is used to play hangman
if False:
	with open(prefix+'_dictionary.json') as json_file: 
	    data = json.load(json_file)
	    # data structure
	    # a
	    	# length of word
	    		# letter contained
	    			# position of letter within word (ie. 0001100 for letter t and words flutter and clutter)
	    				# word
	    # b
	    	# length of word
	    		# position of letter
	    			# letter
	    				# word
	    alphadata = {"a":{},"b":{}}
	    for i in data:
	    	if len(i) not in alphadata["a"]:
	    		alphadata["a"][len(i)] = {"a":{},"b":{},"c":{},"d":{},"e":{},"f":{},"g":{},"h":{},"i":{},"j":{},"k":{},"l":{},"m":{},"n":{},"o":{},"p":{},"q":{},"r":{},"s":{},"t":{},"u":{},"v":{},"w":{},"x":{},"y":{},"z":{}}
	    		alphadata["b"][len(i)] = {}
	    		for j in range(len(i)):
	    			alphadata["b"][len(i)][j] = {"a":[],"b":[],"c":[],"d":[],"e":[],"f":[],"g":[],"h":[],"i":[],"j":[],"k":[],"l":[],"m":[],"n":[],"o":[],"p":[],"q":[],"r":[],"s":[],"t":[],"u":[],"v":[],"w":[],"x":[],"y":[],"z":[]}
	    	for j in alphabet:
	    		tally = ""
	    		count = 0
	    		for k in i:
	    			if j==k:
	    				tally+="1"
	    				count+=1
	    			else:
	    				tally+="0"
	    		if count>0:
	    			if tally not in alphadata["a"][len(i)][j]:
	    				alphadata["a"][len(i)][j][tally] = []
	    			alphadata["a"][len(i)][j][tally].append(i)
	    	for j,v in enumerate(i):
	    		alphadata["b"][len(i)][j][v].append(i)
	    with open(prefix+'_alphadata.json', 'w') as fp:
	    	json.dump(alphadata, fp)
else:
	with open(prefix+'_alphadata.json') as json_file:
		data = json.load(json_file)
		length = input("choose a word length ")
		while length not in data["a"]:
			length = input("that word length doesn't exist, try again ")
		print("word selected")
		# either False or True where False is easy and True is hard
		difficulty = input("choose a difficulty: easy or hard ")
		while difficulty!="easy" and difficulty!="hard":
			difficulty = input("not recognized, try again ")
		difficulty = difficulty=="hard"
		current = ["_" for i in range(int(length))]
		failures = []
		print(current)
		print(failures)
		guess = input("guess a letter ")
		if difficulty:
			possibilities = {}
			for i in data["a"][length]:
				for j in data["a"][length][i]:
					for k in data["a"][length][i][j]:
						possibilities[k]=1
			while(True):
				if guess in failures or guess in current:
					guess = input("you already guessed that letter, try again ")
					continue
				if guess in alphabet:
					besti = ""
					bestrand = 0
					bestattempt = {}
					for i in data["a"][length][guess]:
						attempt = possibilities.copy()
						rand = random.random()
						for j in data["a"][length][guess]:
							if j == i:
								continue
							for k in data["a"][length][guess][j]:
								if k in attempt:
									attempt.pop(k)
						for j,v in enumerate(i):
							if v=="1":
								for k in data["b"][length][str(j)]:
									if k == guess:
										continue
									for l in data["b"][length][str(j)][k]:
										if l in attempt:
											attempt.pop(l)
						if len(attempt)+rand>len(bestattempt)+bestrand:
							besti = i
							bestrand = rand
							bestattempt = attempt.copy()
					attempt = possibilities.copy()
					for i in data["a"][length][guess]:
						for j in data["a"][length][guess][i]:
							if j in attempt:
								attempt.pop(j)
					if len(attempt)>len(bestattempt)+bestrand:
						possibilities=attempt.copy()
						failures.append(guess)
						print(current)
						print(failures)
					else:
						possibilities = bestattempt.copy()
						for i,v in enumerate(besti):
							if v=="1":
								current[i]=guess
						print(current)
						print(failures)
						for i in current:
							if i == "_":
								break
						else:
							print("you won with only "+str(len(failures))+" incorrect guesses")
							final = ""
							for i in current:
								final+=i
							print("The word was "+final)
							break
				else:
					print("that wasn't a letter")
					#print(possibilities)
				guess = input("guess a letter ")
		else:
			path = [length]
			count = len(data["a"][path[0]])-1
			for i in data["a"][path[0]]:
				if random.randint(0,count)==0:
					path.append(i)
					break
				count-=1
			count = len(data["a"][path[0]][path[1]])-1
			for i in data["a"][path[0]][path[1]]:
				if random.randint(0,count)==0:
					path.append(i)
					break
				count-=1
			count = len(data["a"][path[0]][path[1]][path[2]])-1
			for i in data["a"][path[0]][path[1]][path[2]]:
				if random.randint(0,count)==0:
					word = i
					break
				count-=1
			while(True):
				if guess in failures or guess in current:
					guess = input("you already guessed that letter, try again ")
					continue
				if guess in alphabet:
					if guess in word:
						for i,v in enumerate(word):
							if v==guess:
								current[i]=guess
						print(current)
						print(failures)
						for i in current:
							if i == "_":
								break
						else:
							print("you won with only "+str(len(failures))+" incorrect guesses")
							final = ""
							for i in current:
								final+=i
							print("The word was "+final)
							break
					else:
						failures+=guess
						print(current)
						print(failures)
				else:
					print("that wasn't a letter")
				guess = input("guess a letter ")