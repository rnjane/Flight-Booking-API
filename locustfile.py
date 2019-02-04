from locust import HttpLocust, TaskSet, task
import tempfile
from PIL import Image
import json

class UserBehavior(TaskSet):
    def __init__(self, parent):
       super(UserBehavior, self).__init__(parent)

       self.token = ""
       self.headers = {}

    def on_start(self):
      self.token = self.login()
      self.headers = {'Authorization': 'Token ' + self.token}

    def get_temporary_image(self):
        '''create a temporary image for testing purposes'''
        image = Image.new('RGB', (200, 200))
        temporary_image = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(temporary_image, 'jpeg')
        temporary_image.seek(0)
        return temporary_image

    def login(self):
        response = self.client.post("/login/", data={"username":"robertnjane", "password":"roba2017"})
        return json.loads(response._content)['token']

    @task(1)
    def index(self):
        self.client.get("/flights")

    @task(2)
    def profile(self):
        self.client.get("/bookings/", headers=self.headers)

    @task(3)
    def uploadpassport(self):
        self.client.post("/upload-passport/", headers=self.headers, files={"image": self.get_temporary_image()})

    @task(4)
    def updatepassport(self):
        self.client.get("/update-passport/", headers=self.headers, files={"image": self.get_temporary_image()})

    @task(5)
    def deletepassport(self):
        self.client.get("/remove-passport/", headers=self.headers)

    @task(6)
    def flightsreport(self):
        self.client.get("/flights-report/", headers=self.headers)

    @task(7)
    def createbooking(self):
        self.client.post("/create-booking/KQAB22341/", headers=self.headers)
    
    @task(8)
    def checkstatus(self):
        self.client.get("/check-status/KQABA21041/", headers=self.headers)

    @task(9)
    def pay(self):
        self.client.post("/pay/KQAB21041/", headers=self.headers)

    @task(10)
    def reserve(self):
        self.client.post("/reserve/KQAB21041/", headers=self.headers)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000