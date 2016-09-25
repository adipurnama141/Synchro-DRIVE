from __future__ import print_function
from random import randint
from copy import deepcopy
import math
import random

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

def hill():
	'''Menggunakan algoritma hill climbing untuk memperoleh konflik sekecil mungkin'''
	lastConflict = conflictCheck()
	for course in courses:
		print(course.name)
		lecture_available = 1
		isProbableToOptimize = 1
		while ((conflictCheck() <= lastConflict) and (isProbableToOptimize)):
			lastConflict = conflictCheck()
			lastAssignedHour = course.assignedHour
			if (course.assignedDay not in course.availDay):
					course.assignedDay = course.availDay[0]

			course.assignedHour += 1

			lecture_available = course.isLecturerAvailable()

			while (not lecture_available and course.assignedHour<=rooms[course.roomIDX].timeClosed):
				course.assignedHour += 1
				lecture_available = course.isLecturerAvailable()

			if (lecture_available) :
				'''Jika pada hari yang sama masih mungkin lebih baik sampai ruangan ditutup, coba hari berikutnya'''
				if ((conflictCheck() <= lastConflict) and (course.assignedHour+int(course.timeDuration) >= (rooms[course.roomIDX].timeClosed + 1))):
					lastConflict = conflictCheck()
					nextIdxDay = course.availDay.index(course.assignedDay)+1
					while (nextIdxDay<len(course.availDay)):
						if (course.availDay[nextIdxDay] != 1):
							nextIdxDay +=1

					if (nextIdxDay<len(course.availDay)) :
						course.assignedDay = course.availDay[nextIdxDay]
						course.assignedHour = rooms[course.roomIDX].timeOpen
						lecture_available = course.isLecturerAvailable()
						last_assignedHour1 = course.assignedHour
						while (not lecture_available and course.assignedHour<=rooms[course.roomIDX].timeClosed):
							lecture_available = course.isLecturerAvailable()
							course.assignedHour += 1
						if (not course.isLecturerAvailable()) :
							course.assignedHour = last_assignedHour1
							isProbableToOptimize=0

				'''Jika sampai hari terakhir masih mungkin ada yang lebih baik, coba ganti ruangan
				lastDay = course.availDay[-1]
				lastHour = rooms[course.roomIDX].timeClosed
				if ((conflictCheck() <= lastConflict) and (course.assignedHour+int(course.timeDuration) >= lastHour + 1) and (course.assignedDay == lastDay)) :
					lastConflict = conflictCheck()
					course.roomIDX = rooms[rooms.index(course.roomIDX)+1]

					lecture_available = course.isLecturerAvailable()
					while (not lecture_available and course.assignedHour<=rooms[couser.roomIDX].timeClosed):
						lecture_available = course.isLecturerAvailable()
						course.assignedHour += 1'''
			else:
				course.assignedHour = lastAssignedHour
				isProbableToOptimize=0

readFile("tc.txt")
hill()