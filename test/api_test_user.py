# from locust import HttpUser, task, between
# url='https://basedjangoapp.vercel.app/api/v1/contacts/'
# url2='http://127.0.0.1:8000/employer/api/v1/users'
# url3='https://jobsserach-oulrun22v-sudarshan519.vercel.app/employer/api/v1/users'
# class APITestUser(HttpUser):
#     wait_time = between(1, 2)  # Random wait time between 1 and 3 seconds between tasks

#     @task
#     def get_user_info(self):
#         response = self.client.get(url3)
#         if response.status_code == 200:
#             print("API response:", response.json())
#         else:
#             print("API request failed:", response.status_code)

#     # @task(2)  # This task will be performed twice as often as get_user_info
#     # def post_data(self):
#     #     # payload = {"key": "value"}
#     #     response = self.client.get("http://127.0.0.1:8000/employer/api/v1/get-employee-by-id?id=1")#, json=payload)
#     #     if response.status_code == 200:
#     #         print("API response:", response.json())
#     #     else:
#     #         print("API request failed:", response.status_code)

# if __name__ == "__main__":
#     APITestUser().run()
