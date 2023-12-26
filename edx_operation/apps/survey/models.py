from re import sub

from django import forms
from django.db.models import (
    BooleanField,
    CASCADE,
    Case,
    CharField,
    Count,
    DateTimeField,
    ForeignKey,
    TextField,
    Value,
    When,
)
from django.http import HttpResponseRedirect
from django.utils.dateparse import parse_datetime
from django.utils.timezone import localtime
from django_ace import AceWidget
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel
from wagtail.blocks import RawHTMLBlock, RichTextBlock
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import (
    AbstractForm,
    AbstractFormField,
    AbstractFormSubmission,
    FORM_FIELD_CHOICES,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page, TemplateResponse

from edx_operation.apps.core.models import User
from edx_operation.apps.core.utils.common import paginate


class SurveyPortal(Page):
    class Meta:
        verbose_name = "설문 조사 포털"
        verbose_name_plural = verbose_name

    template = "survey/survey_portal.html"
    subpage_types = ["SurveyPage"]
    max_count = 1

    content = StreamField(
        [
            ("image", ImageChooserBlock(label="이미지", required=False)),
            ("richtext", RichTextBlock(label="텍스트", required=False)),
            ("embed", EmbedBlock(label="임베드", required=False)),
            ("html", RawHTMLBlock(label="HTML", required=False)),
        ],
        use_json_field=True,
        verbose_name="콘텐츠",
        null=True,
        blank=True,
    )

    # panels
    content_panels = Page.content_panels + [FieldPanel("content")]

    def get_context(self, request, *args, **kwargs):
        now = localtime()
        surveys = (
            self.get_children()
            .live()  # type: ignore
            .annotate(
                submission_count=Count("formsubmission__id"),
                status=Case(
                    When(surveypage__end__lt=now, then=Value("종료")),
                    When(surveypage__start__gt=now, then=Value("시작 전")),
                    default=Value("진행 중"),
                    output_field=CharField(),
                ),
            )
            .order_by("-id")
        )

        # pagination
        page = request.GET.get("page")
        per_page = request.GET.get("per_page")
        surveys = paginate(surveys, page, per_page or 30)

        context = super().get_context(request, *args, **kwargs)
        context["surveys"] = surveys
        return context


class SuryveyField(AbstractFormField):
    class Meta:
        verbose_name = "설문 항목"
        verbose_name_plural = verbose_name

    page = ParentalKey("SurveyPage", on_delete=CASCADE, related_name="survey_fields")

    # remove single checkbox, date
    CHOICES = [l for l in FORM_FIELD_CHOICES if l[0] not in ("checkbox", "date")]
    field_type = CharField("필드 타입", max_length=16, choices=CHOICES)


class SurveyFormSubmission(AbstractFormSubmission):
    class Meta:
        verbose_name = "설문 응답"
        verbose_name_plural = verbose_name

    user = ForeignKey(User, on_delete=CASCADE, null=True, blank=True)

    def get_data(self):
        form_data = super().get_data()
        form_data.update({"username": self.user.username if self.user else ""})

        return form_data


class SurveyFormBuilder(FormBuilder):
    def create_multiline_field(self, field, options):
        attrs = {"rows": "4"}
        return forms.CharField(widget=forms.Textarea(attrs=attrs), **options)

    def create_datetime_field(self, field, options):
        attrs = {"type": "datetime-local"}
        return forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs=attrs), **options)


class SurveyPage(AbstractForm):
    class Meta:
        verbose_name = "설문 조사"
        verbose_name_plural = verbose_name

    form_builder = SurveyFormBuilder
    template = "survey/survey_page.html"
    parent_page_types = ["SurveyPortal"]
    subpage_types = []

    login_required = BooleanField("로그인 필요", default=True)
    start = DateTimeField("시작", db_index=True)
    end = DateTimeField("종료", db_index=True)
    description = StreamField(
        [
            ("image", ImageChooserBlock(label="이미지", required=False)),
            ("richtext", RichTextBlock(label="텍스트", required=False)),
            ("embed", EmbedBlock(label="임베드", required=False)),
            ("html", RawHTMLBlock(label="HTML", required=False)),
        ],
        use_json_field=True,
        verbose_name="설문 조사 안내",
    )
    outro = RichTextField("설문 종료 안내")
    chart_script = TextField("chart javascript", null=True, blank=True)
    css = TextField("CSS 추가 하기", null=True, blank=True)

    # panels
    content_panels = AbstractForm.content_panels + [
        FieldRowPanel(
            [
                FieldPanel("start"),
                FieldPanel("end"),
            ]
        ),
        FieldPanel("login_required"),
        FieldPanel("description", classname="collapsed"),
        InlinePanel("survey_fields", label="설문"),
        FieldPanel("outro"),
        FieldPanel(
            "chart_script",
            widget=AceWidget(mode="javascript", width="100%", toolbar=True),
            heading="chart javascript",
            classname="collapsed",
        ),
        FieldPanel(
            "css",
            widget=AceWidget(mode="css", width="100%", toolbar=True),
            classname="collapsed",
        ),
    ]

    def get_data_fields(self):
        data_fields = [("username", "제출자")]
        data_fields += super().get_data_fields()

        return data_fields

    def get_submission_class(self):
        return SurveyFormSubmission

    def process_form_submission(self, form):
        user = form.user if form.user.is_authenticated else None
        return self.get_submission_class().objects.create(
            form_data=form.cleaned_data, page=self, user=user
        )

    def get_form_fields(self):
        return self.survey_fields.all()  # type: ignore

    def get_context(self, request, *args, **kwargs):
        return super().get_context(request, *args, **kwargs)

    def serve(self, request, *args, **kwargs):
        form = None
        message = ""

        if self.login_required and not request.user.is_authenticated:
            message = "이 설문 조사는 로그인 후에 참여할 수 있습니다."

        if not (self.start <= localtime() <= self.end):
            message = "설문 조사 기간이 아닙니다."

        if request.method == "POST":
            # submit form
            form = self.get_form(request.POST, request.FILES, page=self, user=request.user)

            if form.is_valid():
                # save form
                self.process_form_submission(form)
                return HttpResponseRedirect("?chart=true")
        else:
            if request.user.is_authenticated:
                submission = (
                    self.get_submission_class()
                    .objects.filter(page=self, user__pk=request.user.pk)
                    .last()
                )
                if submission:
                    message = "응답을 제출했습니다."

                    # submission을 form으로 복원
                    form_data = submission.form_data
                    for k, v in form_data.items():
                        try:
                            # fix django datetime widget format
                            parse_datetime(v)
                            form_data[k] = sub("\\+.*", "", v)
                        except Exception:
                            pass

                    form = self.get_form_class()(
                        user=request.user, page=self, initial=submission.form_data
                    )

            if not form:
                # new form
                form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context.update(form=form, message=message)

        # show results
        if request.GET.get("chart") == "true":
            results = dict()
            survey_fields = [(field.clean_name, field.label) for field in self.get_form_fields()]
            submissions = self.get_submission_class().objects.filter(page=self)

            for submission in submissions:
                data = submission.get_data()

                for name, label in survey_fields:
                    answer = data.get(name)
                    if answer is None:
                        continue

                    if type(answer) is list:
                        # fix duplicate
                        answer.sort()
                        answer = ", ".join(answer)

                    question_stats = results.get(label, {})
                    question_stats[answer] = question_stats.get(answer, 0) + 1
                    results[label] = question_stats

            # merge empty choices
            form_builder = self.form_builder(self.get_form_fields())
            for field in self.get_form_fields():
                question_stats = results.get(field.label, {})

                for name, _ in form_builder.get_formatted_field_choices(field):
                    if name not in question_stats:
                        question_stats[name] = 0

            context.update(
                results=results,
                submission_count=self.get_submission_class().objects.filter(page=self).count(),
            )

        return TemplateResponse(request, self.get_template(request), context)
