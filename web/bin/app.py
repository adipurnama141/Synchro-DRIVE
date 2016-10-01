import web
import alocator



urls = (
  '/', 'Index'
)

app = web.application(urls, globals())
render = web.template.render('templates/')



class Index(object):
    def GET(self):
    	alocator.readFile("tc.txt")
    	alocator.hill()
    	rooms =  alocator.generateRoomJSON()
    	courses = alocator.generateCourseJSON()
        return render.index(courses,rooms)




if __name__ == "__main__":
    app.run()