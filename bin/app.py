import web
import alocator



urls = (
  '/', 'Index',
  '/hill' , 'Hill',
  '/sa' , 'SA',
  '/genetic' , 'Genetic'
)

app = web.application(urls, globals())
render = web.template.render('templates/')



class Index(object):
    def GET(self):
    	alocator.readFile("tc.txt")
    	alocator.hill()
    	rooms =  alocator.generateRoomJSON()
    	courses = alocator.generateCourseJSON()
    	code = 1
        return render.index(courses,rooms,code)

class Hill(object):
    def GET(self):
    	alocator.readFile("tc.txt")
    	alocator.hill()
    	code = 1
    	rooms =  alocator.generateRoomJSON()
    	courses = alocator.generateCourseJSON()
        return render.index(courses,rooms,code)

class SA(object):
    def GET(self):
    	alocator.readFile("tc.txt")
    	alocator.simulatedAnneiling(10,0.9)
    	code = 2
    	rooms =  alocator.generateRoomJSON()
    	courses = alocator.generateCourseJSON()
        return render.index(courses,rooms,code)

class Genetic(object):
    def GET(self):
    	alocator.readFile("tc.txt")
    	alocator.geneticAllocate()
    	code = 3
    	rooms =  alocator.generateRoomJSON()
    	courses = alocator.generateCourseJSON()
        return render.index(courses,rooms,code)




if __name__ == "__main__":
    app.run()