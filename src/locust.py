import random
from locust import HttpUser, between, task, tag

class WebsiteUser(HttpUser):
    wait_time = between(1, 1.5)

    def on_start(self):
        self.uid = str(random.randint(0, 100_000)).zfill(6)

    @task
    def attempt(self):
        self.client.get("/health")

    # @task
    # def sleep(self):
    #     self.client.get("/sleep/")

    # @task
    # def simulate(self):
    #     self.client.post("/simulate/", json={
    #         "uid": self.uid,
    #         "n_sim": random.randint(10, 20)
    #     })
