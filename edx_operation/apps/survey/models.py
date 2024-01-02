from django import forms
from django.db.models import CASCADE, CharField
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import InlinePanel
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel

from edx_operation.apps.wagtail_common.models import AbstractPostHome, AbstractPostPage


class SurveyHome(AbstractPostHome):
    class Meta:
        verbose_name = "설문 조사"
        verbose_name_plural = verbose_name

    subpage_types = ["SurveyPage"]
    template = "wagtail_common/post_home.html"


class FormField(AbstractFormField):
    class Meta:
        verbose_name = "설문 항목"
        verbose_name_plural = verbose_name

    page = ParentalKey("SurveyPage", on_delete=CASCADE, related_name="form_fields")
    # fix: label over 255 length
    label = CharField(verbose_name="설문", max_length=2000)


class SurveyFormBuilder(FormBuilder):
    def create_multiline_field(self, field, options):
        attrs = {"rows": "4"}
        return forms.CharField(widget=forms.Textarea(attrs=attrs), **options)

    def create_datetime_field(self, field, options):
        attrs = {"type": "datetime-local"}
        return forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs=attrs), **options)


class SurveyPage(AbstractPostPage, AbstractForm):
    class Meta:
        verbose_name = "설문 조사"
        verbose_name_plural = verbose_name

    form_builder = SurveyFormBuilder

    parent_page_types = ["SurveyHome"]
    subpage_types = []
    template = "survey/survey_page.html"
    landing_page_template = "survey/survey_page.html"

    # panels
    content_panels = AbstractPostPage.content_panels + [
        FormSubmissionsPanel(),
        InlinePanel("form_fields", label="설문 항목"),
    ]
