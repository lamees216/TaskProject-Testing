from locust import HttpUser, task, between

class TaskUser(HttpUser):
    # محاكاة وقت انتظار المستخدم بين الطلبات (من ثانية إلى ثانيتين)
    wait_time = between(1, 2)

    # 1. اختبار استجابة الصفحة الرئيسية
    @task
    def get_root(self):
        self.client.get("/")

    # 2. اختبار جلب المهام (وزن 3 يعني يتكرر أكثر)
    @task(3)
    def get_tasks(self):
        self.client.get("/tasks/")

    # 3. اختبار إضافة مهمة (وزن 1)
    @task(1)
    def create_task(self):
        # لاحظي: هنا نرسل title تجريبي لضمان نجاح العملية
        self.client.post("/tasks/?title=LoadTestTask")