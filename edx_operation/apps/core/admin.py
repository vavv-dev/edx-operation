import logging

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.db.models import CharField, ManyToManyField, OneToOneField


log = logging.getLogger(__name__)

if settings.DEBUG:
    # 어드민 자동 생성

    class AdminDebugMixin(admin.ModelAdmin):
        def get_autocomplete_fields(self, request):
            """add autocomplete_fields automatically"""

            fields = super().get_autocomplete_fields(request)
            for field in self.model._meta.fields:
                if field.is_relation and field.related_model:
                    fields += (field.name,)
            for field in self.model._meta.many_to_many:
                fields += (field.name,)
            return fields

        def get_search_fields(self, request):
            """add search_fields automatically"""

            fields = super().get_search_fields(request)
            for field in self.model._meta.fields:
                if field.primary_key or isinstance(field, CharField):
                    fields += (field.name,)
            return fields

        def get_list_display(self, request):
            """add list_displays automatically"""

            fields = []
            for field in self.model._meta.fields:
                if not field.editable:
                    continue
                if field.primary_key:
                    fields.insert(0, field.name)
                    continue
                fields.append(field.name)
            return fields

        def get_list_filter(self, request):
            """add list_filter automatically"""

            fields = super().get_list_filter(request)
            for field in self.model._meta.fields:
                if field.choices and len(field.choices) < 10:
                    fields += (field.name,)
            return fields

        # def get_inlines(self, request, obj):
        #     """add inlines automatically"""

        #     inlines = super().get_inlines(request, obj)

        #     for field in self.model._meta.many_to_many:
        #         if isinstance(field, ManyToManyField):
        #             related_model = field.remote_field.through
        #             related_model_name = related_model.__name__

        #             inline_admin_name = f"{self.model.__name__}{related_model_name}Inline"
        #             inline_admin_class = type(
        #                 inline_admin_name, (admin.TabularInline,), {"model": related_model}
        #             )

        #             # inline admin autocomplete_fields
        #             autocomplete_fields = []
        #             for field in inline_admin_class.model._meta.fields:
        #                 if field.is_relation and field.related_model:
        #                     autocomplete_fields.append(field.name)
        #             inline_admin_class.autocomplete_fields = autocomplete_fields

        #             inlines += (inline_admin_class,)
        #     return inlines

        def get_actions(self, request):
            """add actions automatically"""

            actions = super().get_actions(request)

            for method_name in dir(self.model):
                method = getattr(self.model, method_name)
                if callable(method) and getattr(method, "_admin_action", False):
                    # Skip inherited method
                    if method.__module__ != self.model.__module__:
                        continue

                    def create_admin_method(name):
                        def admin_action(self, request, queryset):
                            for obj in queryset:
                                try:
                                    getattr(obj, name)()
                                except Exception as e:
                                    log.error(e, exc_info=True)

                        return admin_action

                    actions[method_name] = (
                        create_admin_method(method_name),
                        method_name,
                        f"{method_name} 실행",
                    )

            return actions

    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            try:

                @admin.register(model)
                class ModelAdmin(AdminDebugMixin):
                    pass

            except admin.sites.AlreadyRegistered:
                pass
