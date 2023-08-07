from django.conf import settings
import requests


class BaseAPIClient(requests.Session):
    def __init__(self, headers=None, cookies=None):
        super().__init__()

        if headers:
            self.headers.update(headers)

        if cookies:
            self.cookies.update(cookies)


class LmsAPIClient(BaseAPIClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_root = f"{settings.LMS_BASE_URL}"

    def modyfy_access_create(self, course_id, data):
        api_url = f"{self.api_root}/courses/{course_id}/instructor/api/modify_access"
        response = self.post(api_url, data=data)
        response.raise_for_status()
        return response.json()
