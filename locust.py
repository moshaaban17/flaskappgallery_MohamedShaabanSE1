from locust import HttpUser, task, between
import uuid

class UserBehavior(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def register(self):
        # Generate a unique username and email for each request
        unique_id = str(uuid.uuid4())
        username = f'user_{unique_id}'
        email = f'{username}@example.com'
        password = 'password'

        self.client.post("/register", {
            "username": username,
            "email": email,
            "password": password
        })
