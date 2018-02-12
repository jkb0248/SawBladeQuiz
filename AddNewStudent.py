import os,re, time
#os to comunitcate to other pi's
#re regular expressions to find patterns in txt file
from random import randint

print "Which tool will you be testing for?\n"
print "1 MiterSaw\n"
print "2 ScrollSaw\n"
print "3 DrillPress\n"

keepgoing = 0

while keepgoing == 0:
	choose_tool = raw_input("Enter a number: ")
	keepgoing = 1
	if choose_tool == "1":
		pi_IP = "192.168.1.19"
		CSV_fid = "MiterSawID.csv"
		quiz = "MiterSawQuiz.txt"
	elif choose_tool == "2":
		pi_IP = "I dunno"
		CSV_fid = "ScrollSawID.csv"
	elif choose_tool == "3":
		pi_IP = "192.168.1.16"
		CSV_fid = "DrillPressID.csv"
		quiz = "DrillPressQuiz.txt"
	else:
		print "invalid selection!"
		keepgoing = 0

#quiz time!
q_fid = open(quiz,'r')
next_q = 0
ans = 0
correct_count = 0
q_count = 0
godmode = 0

print "*******************************************"

#for each line in the quiz txt file
for line in q_fid:
	nl = re.match("^\s",line) #search for a blank line
	if next_q == 0 and nl == None:
		print "\n\n"
		#gets question number
		q_num = re.search("\d*\.",line)
		q_num = q_num.group(0)[:-1]
		#gets number of  possible answer choices
		ans_num = re.search("\.\d*\.",line)
		ans_num = int(ans_num.group(0)[1:-1])
		#gets correct answer
		ans_loc = re.search("\..#",line)
		ans_loc = ans_loc.group(0)[1:-1]
		print q_num + ".) ",               #print question number
		question = re.search("#.+",line) 
		question = question.group(0)
		print question[1:] + "\n"  	   #print question
		next_q = 1
		q_count = q_count + 1

	elif next_q == 1 and nl == None:
		#print answer choices
		ans = ans + 1
		if ans < ans_num:
			print "      " + line
		elif ans == ans_num:
			print "      " + line
			ans = 0
			next_q = 0
	elif nl:
		validletter = 0
		while validletter == 0:
			selection = raw_input("Select your answer carfully: ")
			print " "
			if selection in "aAbBcCdDeE" and selection != "":
				validletter = 1
			elif selection == "godmode":
				q_count = 1
				correct_count = 0
				godmode = 1
				os.system("clear")
				for i in range(0,100000):
					print str(randint(0,1)),
				print "\n\n\n"
				break
			else:
				print "invalid choice! Use only the letters a - e\n"

		print "*******************************************\n"

		if selection == ans_loc:
			print "Correct!"
			correct_count = correct_count + 1
		elif godmode == 1:
			print "-Initiate Quiz Bypass Mode-"
		else:
			print "Oops ya got it wrong."

		print "\n*******************************************\n"
		time.sleep(2)

	if godmode == 1:
		break

if (q_count-1) - correct_count < 2:
	#grant access!
	print "You passed!"
	appendName = raw_input ("Enter Student Name: ")
	appendID = ""
	while len(appendID) != 9:
		appendID = raw_input ("Scan or Enter S# (Inlcude the 'S'): ")
		if len(appendID) != 9:
			print "thats not a valid S number"
			print "make sure you include the S"

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

	print "\n User access updated."


else:
	print "Sorry you failed, study more and try again :("
