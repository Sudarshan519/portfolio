from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Random wait time between 1 and 3 seconds between tasks

    @task
    def index_page(self):
        self.client.get("/")

    @task(3)  # This task will be performed three times more often than index_page
    def about_page(self):
        self.client.get("/about")

if __name__ == "__main__":
    WebsiteUser().run()
