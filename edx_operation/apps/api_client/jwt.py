import json

from django.conf import settings
from edx_rest_api_client.client import OAuthAPIClient


class BaseAPIClient(OAuthAPIClient):
    def __init__(self, **kwargs):
        super().__init__(
            base_url=settings.BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL,
            client_id=settings.BACKEND_SERVICE_EDX_OAUTH2_KEY,
            client_secret=settings.BACKEND_SERVICE_EDX_OAUTH2_SECRET,
            **kwargs,
        )


class LmsAPIClient(BaseAPIClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_root = f"{settings.LMS_BASE_URL}/api"

    def courses_v1_courses_read(self, courserun_id):
        api_url = f"{self.api_root}/courses/v1/courses/{courserun_id}/"
        response = self.get(api_url)
        response.raise_for_status()
        return response.json()

    def courses_v2_blocks_list(self, courserun_id, params):
        api_url = f"{self.api_root}/courses/v2/blocks/"
        params = {"course_id": str(courserun_id), **params}
        response = self.get(api_url, params=params)
        response.raise_for_status()
        return response.json()

    def course_modes_v1_curses_create(self, courserun_id, course_modes):
        api_url = f"{self.api_root}/course_modes/v1/courses/{courserun_id}/"
        responses = []
        for mode in course_modes:
            response = self.post(api_url, json=mode)
            response.raise_for_status()
            responses.append(response.json())
        return responses

    def user_v1_account_registration_create(self, payload):
        api_url = f"{self.api_root}/user/v1/account/registration/"
        # not json but data
        response = self.post(api_url, data=payload)
        response.raise_for_status()
        return response.json()

    def grades_v1_policy_courses_read(self, courserun_id):
        api_url = f"{self.api_root}/grades/v1/policy/courses/{courserun_id}/"
        response = self.get(api_url)
        response.raise_for_status()
        return response.json()


class EnrollmentAPIClient(BaseAPIClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_root = f"{settings.LMS_BASE_URL}/api/enrollment"

    def v1_enrollment_create(self, payload):
        api_url = f"{self.api_root}/v1/enrollment"
        # cf. openedx/core/lib/api/permissions.py:33
        headers = {"X-EDX-API-KEY": settings.EDX_API_KEY}
        response = self.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()


class CmsAPIClient(BaseAPIClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_root = f"{settings.CMS_BASE_URL}/api"

    def v1_course_runs_create(self, payload):
        api_url = f"{self.api_root}/v1/course_runs/"
        response = self.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def v1_course_runs_rerun(self, courserun_id, payload):
        api_url = f"{self.api_root}/v1/course_runs/{courserun_id}/rerun/"
        response = self.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def courses_v0_import_create(self, courserun_id, file):
        api_url = f"{self.api_root}/courses/v0/import/{courserun_id}/"
        response = self.post(api_url, files={"course_data": file})
        response.raise_for_status()
        return response.json()

    def olx_export_v1_xblock_read(self, usage_key):
        api_url = f"{self.api_root}/olx-export/v1/xblock/{usage_key}"
        response = self.get(api_url)
        response.raise_for_status()
        return response.json()


class EnterpriseAPIClient(BaseAPIClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_root = f"{settings.LMS_BASE_URL}/enterprise/api"

    def v1_enterprise_customer_create(self, payload):
        api_url = f"{self.api_root}/v1/enterprise-customer/"
        response = self.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def v1_enterprise_customer_catalog_create(self, payload):
        api_url = f"{self.api_root}/v1/enterprise_customer_catalog/"
        response = self.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def v1_enterprise_learner_create(self, payload):
        api_url = f"{self.api_root}/v1/enterprise-learner/"
        response = self.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def v1_enterprise_course_enrollment_create(self, payload):
        api_url = f"{self.api_root}/v1/enterprise-course-enrollment/"
        response = self.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
