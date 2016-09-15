from __future__ import print_function

class Room:
	def __init__(self,x):
		self.name = x[0]
		self.timeOpen = x[1]
		self.timeClosed = x[2]
		self.availDay = [0,0,0,0,0]
		for elmt in x[3].split(","):
			self.availDay[int(elmt)-1] = 1
		self.roomUsage = []
		for x in range(7,17):
			if ((x >= int(self.timeOpen.split(".")[0])) and (x <= int(self.timeClosed.split(".")[0]))):
				self.roomUsage.append(self.availDay)
			else:
				self.roomUsage.append([0,0,0,0,0])


	def printit(self):
		print("Ruangan : %s" %self.name)
		print("Buka dari jam %s s.d %s" %(self.timeOpen,self.timeClosed))
		for day in self.availDay:
			print(day, end="")
		print("")
		counter = 7
		for eachHour in self.roomUsage:
			if (counter < 10):
				print("%s -> %s "%("0"+str(counter),str(eachHour)))
			else:
				print("%d -> %s "%(counter,str(eachHour)))
			counter += 1


class Course:
	def __init__(self,x):
		self.name = x[0]
		self.roomID = x[1]
		self.timeOpen = x[2]
		self.timeClosed = x[3]
		self.timeDuration  = x[4]
		self.availDay = [0,0,0,0,0]
		for elmt in x[5].split(","):
			self.availDay[int(elmt)-1] = 1
		self.lecturerAvailability = []
		for x in range(7,17):
			if ((x >= int(self.timeOpen.split(".")[0])) and (x <= int(self.timeClosed.split(".")[0]))):
				self.lecturerAvailability.append(self.availDay)
			else:
				self.lecturerAvailability.append([0,0,0,0,0])


	def printit(self):
		print("Mata Kuliah : %s" %self.name)
		print("Tempat Khusus : %s" %self.roomID)
		print("Dosennya bisa ngajar dari jam %s sampai %s" %(self.timeOpen , self.timeClosed))
		print("Durasinya : %s" %self.timeDuration)
		for day in self.availDay:
			print(day, end="")
		print("")
		counter = 7
		for eachHour in self.lecturerAvailability:
			if (counter < 10):
				print("%s -> %s "%("0"+str(counter),str(eachHour)))
			else:
				print("%d -> %s "%(counter,str(eachHour)))
			counter += 1



rooms = []
courses = []


with open("tc.txt") as f:
	contents = f.readlines()

readingStatus = 0
roomCounter = 0
courseCounter = 0

for content in contents:
	
	#menghapus newline di ujung, jika ada
	if (content.endswith("\n")):
		content = content[:-1]

	if (content == "Ruangan"):
		readingStatus = 1

	elif (content == "Jadwal"):
		readingStatus = 2
	
	elif content:
		if (readingStatus == 1):
			roomCounter += 1
			preprocess = content.split(";")
			rooms.append(Room(preprocess))
		elif (readingStatus == 2):
			courseCounter += 1
			preprocess = content.split(";")
			courses.append(Course(preprocess))



print("Room : %d " %roomCounter)
print("Course :%d " %courseCounter)




for room in rooms:
	room.printit()
	print("")

for course in courses:
	course.printit()
	print("")


