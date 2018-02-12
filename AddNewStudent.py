import os,re, time
#os to comunitcate to other pi's
#re regular expressions to find patterns in txt file
from random import randint
import json

print ("Which tool will you be testing for?\n")
print ("1 MiterSaw\n")
print ("2 ScrollSaw\n")
print ("3 DrillPress\n")

keepgoing = 0

while keepgoing == 0:
	choose_tool = input("Enter a number: ")
	keepgoing = 1
	if choose_tool == "1":
		pi_IP = "192.168.1.19"
		CSV_fid = "MiterSawID.csv"
		quiz = "MiterSawQuiz.json"
	elif choose_tool == "2":
		pi_IP = "I dunno"
		CSV_fid = "ScrollSawID.csv"
	elif choose_tool == "3":
		pi_IP = "whateves"
		CSV_fid = "DrillPressID.csv"
	else:
		print ("invalid selection!")
		keepgoing = 0

#quiz time!
q_fid = open(quiz,'r')
next_q = 0
ans = 0
correct_count = 0
q_count = 0
godmode = 0

print ("*"*80)

jobj = json.load(q_fid)
#for each line in the quiz txt file
for i, question in enumerate(jobj):
	print("{}.) {}".format(i +1 , question["header"]))

	for j, qu in enumerate(question["data"]):
		print("\t{}. {}\n".format(chr(j + ord('A')), qu))
		
	answer = -1
	while True:
		selection = input("Select your answer carfully: ")
		if selection[0].upper() in "ABCDEF" and selection != "":
			answer = ord(selection[0].upper()) - ord('A')
			break

		elif selection == "godmode":
			q_count = 1
			correct_count = 0
			godmode = 1
			os.system("clear")
			print ("\n\n\n")
			break

		else:
			print ("invalid choice! Use only the letters a - e\n")
	
	print ("\n{}\n".format('*'*80))
	# print ("Selection: {} == {} ? {}".format(answer, question["answer"], answer == question["answer"]))
	if answer == question["answer"]:
		print ("Correct!")
		correct_count = correct_count + 1
	elif godmode == 1:
		print ("-Initiate Quiz Bypass Mode-")
		break
	else:
		print ("Oops ya got it wrong.")

	print ("\n{}\n".format('*'*80))
	time.sleep(2)

if (q_count-1) - correct_count < 2:
	#grant access!
	print ("You passed!")
	appendName = input ("Enter Student Name: ")
	appendID = ""
	while len(appendID) != 9:
		appendID = input ("Scan or Enter S# (Inlcude the 'S'): ")
		if len(appendID) != 9:
			print ("thats not a valid S number")
			print ("make sure you include the S")

	os.system('scp pi@'+pi_IP+':/home/pi/Desktop/barcode/'+CSV_fid+' .')
	fid = open(CSV_fid,'r')
	file_list = []
	for line in fid:
		file_list.append(line)

	file_list.append(appendName+", "+appendID+"\r\n")
	fid.close()


	os.system('mv '+ CSV_fid + ' old' + CSV_fid )
	new_fid = open(CSV_fid, 'w')

	for s in file_list:
		new_fid.write(s)

	new_fid.close()
	os.system('scp ~/Desktop/'+CSV_fid + ' pi@'+pi_IP+':/home/pi/Desktop/barcode/')

	print ("\n User access updated.")


else:
	print ("Sorry you failed, study more and try again :(")
