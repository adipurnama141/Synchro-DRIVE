from __future__ import print_function
from random import randint
from copy import deepcopy
import math
import random
import json

global rooms
global courses

rooms = []
courses = []

class Room:
	def __init__(self,x):
		self.name = x[0]

		tempTime = x[1].split(".")
		self.timeOpen = int(tempTime[0]) - 6

		tempTime = x[2].split(".")
		self.timeClosed = int(tempTime[0]) - 6

		self.availDay = [-1,0,0,0,0,0]
		for elmt in x[3].split(","):
			self.availDay[int(elmt)] = 1
		
	def printit(self):
		print("Ruangan : %s" %self.name)
		print("Buka dari jam %s s.d %s" %(self.timeOpen,self.timeClosed))
		for x in range(1,6):
			print(self.availDay[x], end="")
		print("")

class Course:
	def __init__(self,x):
		self.name = x[0]
		self.roomName = x[1]

		tempTime = x[2].split(".")
		self.timeOpen = int(tempTime[0]) - 6
		
		tempTime = x[3].split(".")
		self.timeClosed = int(tempTime[0]) - 6

		self.timeDuration  = x[4]
		self.assignedHour = randint(1,11)
		self.assignedDay = randint(1,5)

		if (self.roomName == "-"):
			self.roomName = rooms[randint(0,len(rooms)-1)].name
			self.VIPRoom = 0
		else:
			self.VIPRoom = 1
		self.roomIDX = 0
		for room in rooms:
			if room.name == self.roomName:
				break
			else:
				self.roomIDX += 1

		self.conflictFlag = 0

		#parsing constraint hari
		self.availDay = [-1,0,0,0,0,0]
		for elmt in x[5].split(","):
			self.availDay[int(elmt)] = 1


	def allocate(self):
		please_execute_at_least_once = 0
		while  ((self.isLecturerAvailable() * self.isRoomAvailable() * please_execute_at_least_once) == 0) :
			please_execute_at_least_once = 1
			self.assignedHour = randint(1,11)
			self.assignedDay = randint(1,5)
			if (not self.VIPRoom):
				self.roomName = rooms[randint(0,len(rooms)-1)].name
				self.roomIDX = 0
				for room in rooms:
					if room.name == self.roomName:
						break
					else:
						self.roomIDX += 1



	def printDetail(self):
		print("Mata Kuliah : %s" %self.name)
		print("Tempat Khusus : %s" %self.roomName)
		print("Dosennya bisa ngajar dari jam %s sampai %s" %(self.timeOpen , self.timeClosed))
		print("Durasinya : %s" %self.timeDuration)
		print("Hari tersedia : ", end="")
		for x in range(1,6):
			print(self.availDay[x], end="")
		print("")


	def isLecturerAvailable(self):
		dayOK = (self.availDay[self.assignedDay] == 1)
		hourOpenOK = (self.assignedHour >= self.timeOpen)
		hourClosedOK = ((self.assignedHour+int(self.timeDuration)) <= (self.timeClosed + 1))
		if (dayOK and hourOpenOK and hourClosedOK):
			return 1
		else:
			return 0

	
	def isRoomAvailable(self):
		
		dayOK = (rooms[self.roomIDX].availDay[self.assignedDay] == 1)
		hourOpenOK = (self.assignedHour >= rooms[self.roomIDX].timeOpen)	
		hourClosedOK = (self.assignedHour+int(self.timeDuration) <= (rooms[self.roomIDX].timeClosed + 1))
		if (dayOK and hourOpenOK and hourClosedOK):
			return 1
		else:
			return 0

	def printAllocation(self):
		print("%s @%s (Hari %s Jam %s | %s SKS)" %(self.name,self.roomName,self.assignedDay , self.assignedHour, self.timeDuration ))
		print("Lecturer Available : %d" %self.isLecturerAvailable())
		print("Room Available     : %d" %self.isRoomAvailable())
		print("conflictFlag       : %d" %self.conflictFlag)
		print("")



def readFile(x):
	del rooms[:]
	del courses[:]
	with open(x) as f:
		contents = f.readlines()
	readingStatus = 0
	for content in contents:
		if (content.endswith("\n")):
			content = content[:-1]
		if (content == "Ruangan"):
			readingStatus = 1
		elif (content == "Jadwal"):
			readingStatus = 2
		elif content:
			if (readingStatus == 1):
				preprocess = content.split(";")
				rooms.append(Room(preprocess))
			elif (readingStatus == 2):
				preprocess = content.split(";")
				courses.append(Course(preprocess))


def conflictCheck():
	totalConflict = 0
	stepCount = 0
	for course in courses:
		course.conflictFlag=0

	for x in range(0, len(courses)):
		y = x+1
		for y in range( y , len(courses)):
			stop = 0
			sameRoom = (courses[x].roomName == courses[y].roomName)
			sameDay = (courses[x].assignedDay == courses[y].assignedDay)
			intersectX = (courses[x].assignedHour >= courses[y].assignedHour) and ( courses[x].assignedHour < (courses[y].assignedHour + int(courses[y].timeDuration)))
			intersectY = (courses[y].assignedHour >= courses[x].assignedHour) and ( courses[y].assignedHour < (courses[x].assignedHour + int(courses[x].timeDuration)))
			intersects = intersectX or intersectY
			if (intersects and sameRoom and sameDay):
				courses[x].conflictFlag += 1
				courses[y].conflictFlag += 1
				totalConflict += 1
	return totalConflict


def isDomainCompl():
	"Mengecek apakah sebuah assignment pada sesuai dengan domain"
	
	ret = 1
	for course in courses:
#		if (course.isLecturerAvailable() * course.isRoomAvailable()) == 0:
#			course.printAllocation()
		ret *= course.isLecturerAvailable() * course.isRoomAvailable()

	
	return ret
def countTotalConflict():
	conflict = 0
	for course in courses:
		conflict += course.conflictFlag
	return conflict

def hill():
	'''Menggunakan algoritma hill climbing untuk memperoleh konflik sekecil mungkin'''
	
	#alokasi awal
	for course in courses:
		course.allocate()
	#algoritma hill
	for course in courses:
		conflictCheck()
		lastConflict = countTotalConflict()
		iterate = 0
		#menghitung hari room yang tersedia

		while (countTotalConflict() <= lastConflict and iterate < 5) :
			#selama masih mungkin digeser, geser jamnya
			lastAssignedHour = course.assignedHour
			while (course.assignedHour+int(course.timeDuration) <= course.timeClosed and course.isRoomAvailable()):
				conflictCheck()
				if (countTotalConflict() <= lastConflict) :
					lastConflict = countTotalConflict()
					#geser jam sampai lecturer ada
					lastAssignedHour = course.assignedHour
					course.assignedHour += 1
					lecture_available = course.isLecturerAvailable()
					while (not lecture_available and course.assignedHour+int(course.timeDuration) <= course.timeClosed):
						course.assignedHour +=1
					if (not lecture_available):
						course.assignedHour=lastAssignedHour
				else:
					course.assignedHour = lastAssignedHour
					break

			if (not course.isRoomAvailable()):
					course.assignedHour=lastAssignedHour

			conflictCheck()					
			if (countTotalConflict() <= lastConflict) :
				lastConflict = countTotalConflict()
				#cari hari selanjutnya
				nextday = course.assignedDay+1
				if (nextday == 6) :
						nextday = 1

				while (course.availDay[nextday]!=1 or rooms[course.roomIDX].availDay[nextday]!=1) :
					nextday += 1
					if (nextday == 6) :
						nextday = 1

				if (nextday!=course.assignedDay):
					lastAssignedDay = course.assignedDay
					course.assignedDay = nextday
					conflictCheck()
					if (countTotalConflict() <= lastConflict) :
						if (rooms[course.roomIDX].timeOpen <= course.timeOpen and rooms[course.roomIDX].timeClosed >= course.timeClosed) :
							course.assignedHour = course.timeOpen
							if (not (course.isLecturerAvailable() and course.isRoomAvailable())):
								course.assignedHour=lastAssignedHour
					else:
						course.assignedDay = lastAssignedDay


			else:
				course.assignedHour = lastAssignedHour

			iterate +=1
			conflictCheck()


def simulatedAnneiling(temperature,ratio) :
    for course in courses :
        course.allocate()
    Ep = conflictCheck()
    T = temperature
    while (T > 0.0001) :
        tempCourses = []
        tempCourses = deepcopy(courses)
        first = random.randint(0,len(courses)-1)
        second = random.randint(0,len(courses)-1)
        courses[first].allocate()
        courses[second].allocate()
        En = conflictCheck()
        if (En == 0) :
            break;
        elif (Ep < En) :
            probability = math.exp((Ep - En)/T)
            if ((random.random() - probability) > 0.0001) :
                for x in range(0, len(courses)) :
                    #print("kembali")
                    courses[x] = deepcopy(tempCourses[x])
            else :
                Ep = En
        else :
            Ep = En
        T = T*ratio


def countRoomUsed() :
	roomUsed = []
	for course in courses:
		if (course.roomName not in roomUsed) :
			roomUsed.append(course.roomName)

	return len(roomUsed)


# Algoritma Genetik
# -----------------------------------------------------------

def minTwoPower(d):
	"2^x terkecil yang lebih besar dari d"

	i = 0
	while (d > 0):
		d = d >> 1
		i = i+1
	return i

def encode(max_day,max_hour):
	"Meng encode daftar course menjadi sebuah kromosom"

	d = 0
	encoded = 0
	bit_room = minTwoPower(len(rooms))
	bit_day = minTwoPower(max_day)
	bit_hour = minTwoPower(max_hour)

	for course in courses:
		encoded += course.roomIDX << d
		d += bit_room
		encoded += course.assignedDay << d
		d += bit_day
		encoded += course.assignedHour << d
		d += bit_hour
	return encoded

def decode(encoded,max_day,max_hour):
	"Men decode kromsom menjadi daftar course"

	bit_room = minTwoPower(len(rooms))
	bit_day = minTwoPower(max_day)
	bit_hour = minTwoPower(max_hour)

	for course in courses:
		course.roomIDX = (((1 << bit_room)-1) & encoded) % len(rooms)
		encoded = encoded >> bit_room
		course.assignedDay = (((1 << bit_day)-1) & encoded) % (max_day+1)
		encoded = encoded >> bit_day
		course.assignedHour = (((1 << bit_hour)-1) & encoded) % (max_hour+1)
		encoded = encoded >> bit_hour
		course.roomName = rooms[course.roomIDX].name

def selectOne(people):
	"Memilih seseorang dari populasi dengan sistem roulette wheel"
    
	total   = sum([c[1] for c in people])
	pick    = random.uniform(0, total)
	current = 0
	for person in people:
		current += person[1]
		if current > pick:
			return person

	return people[len(people)-1]

def geneticAllocate():
	"menggunakan algoritma genetik untuk mengalokasi course dengan konflik terkecil"
	
	# Adam & Eve Generation : magic number = 160
	people = []
	ideal_population = 160
	max_hour = 11
	max_day = 5
	solusi = 0
	panjang = len(courses)*(minTwoPower(len(rooms))+minTwoPower(max_day)+minTwoPower(max_hour))
	solusi = (0,0)

	for i in range(0, ideal_population):
		for course in courses:
			course.allocate()

		conflictCheck()
		conflict = countTotalConflict()
		chance = math.exp(conflict*(-1.0))	

		if chance > solusi[1]:
			solusi = (encode(max_day,max_hour),chance)
		person = encode(max_day,max_hour)
		people.append((person,chance))
	
	#To benchmark, free these lines of code
#	decode(solusi[0],max_day,max_hour)
#	conflictCheck()
#	print(countTotalConflict())

	step = 1
	while (solusi[1] != 1) and (step < 20):
	#	print("step = ",step)
		valedictorian = 9999
		print('.', end="")
		new_people = []
		
		while (len(new_people) < ideal_population):
			# Selection Process
			children1 = selectOne(people)[0]
			children2 = selectOne(people)[0]
			
			# Crossover Process
			crossover_chance = 0.7
			for i in range(0,panjang):
				isSwap = random.uniform(0, 1)
				if isSwap < crossover_chance:
					temp1 = (children1 >> i) & 1
					temp2 = (children2 >> i) & 1
					if temp1 != temp2:
						children1 = children1 - (temp1 << i) + (temp2 << i)
						children2 = children2 - (temp2 << i) + (temp1 << i)
#					children1 = ((children1 >> (i+1)) << (i+1)) + (temp2 << i) + (children1 & ((1 << (i+1))-1))
#					children2 = ((children2 >> (i+1)) << (i+1)) + (temp1 << i) + (children2 & ((1 << (i+1))-1)) 

			# Mutation Process
			mutation_chance = 0.001
			for i in range(0,panjang):
				isMutate = random.uniform(0, 1)
				if isMutate < mutation_chance:
					temp1 = (children1 >> i) & 1
					temp2 = (temp1 ^ 1) & 1 
					children1 = children1 - (temp1 << i) + (temp2 << i)
				#	children1 = ((children1 >> (i+1)) << (i+1)) + ((((children1 >> i) + 1) & 1) << i) + (children1 & (1 << (i+1)-1))

			for i in range(0,panjang):
				isMutate = random.uniform(0, 1)
				if isMutate < mutation_chance:
					temp1 = (children2 >> i) & 1
					temp2 = (temp1 ^ 1) & 1 
					children2 = children2 - (temp1 << i) + (temp2 << i)
				#	children2 = ((children2 >> (i+1)) << (i+1)) + ((((children2 >> i) + 1) & 1) << i) + (children2 & (1 << (i+1)-1))

			# Registration of new citizen
			decode(children1,max_day,max_hour)
			if isDomainCompl():
				conflictCheck()
				conflict = countTotalConflict()
				if valedictorian > conflict:
					valedictorian = conflict
				chance = math.exp(conflict*(-1.0))
			else:
				chance = 0

			if chance > solusi[1]:
				solusi = (children1,chance)
			new_people.append((children1,chance))

			decode(children2,max_day,max_hour)
			if isDomainCompl():
				conflictCheck()
				conflict = countTotalConflict()
				if valedictorian > conflict:
					valedictorian = conflict
				chance = math.exp(conflict*(-1.0))
			else:
				chance = 0

			if chance > solusi[1]:
				solusi = (children2,chance)
			new_people.append((children2,chance))
			# Repeat until certain new population reached
			
		# The King is dead, long live the King
		people = new_people

		step = step+1
	#	print(valedictorian)
		# If the Hero doesn't come the world will end in 1000000 days

	decode(solusi[0],max_day,max_hour)
	conflictCheck()
	print("")

def countRoomUsed() :
	roomUsed = []
	for course in courses:
		if (course.roomName not in roomUsed) :
			roomUsed.append(course.roomName)

	return len(roomUsed)

#--------------------#












# Untuk keperluan output ke web
#-------------------------------------------------------------
def generateCourseJSON():
	dump = json.dumps([course.__dict__ for course in courses])
	print("di bawah saya dump \n")
	print(dump)
	return dump

def generateRoomJSON():
	dump = json.dumps([room.__dict__ for room in rooms])
	print("di bawah saya dump \n")
	print(dump)
	print("di bawah saya objek benerannya\n")
	print(len(rooms))

	return dump
	
