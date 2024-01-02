## django-comments-xtd js plugin build

https://github.com/danirus/django-comments-xtd/blob/eb2e003c15caf27fa13a045d088c712fe5dcb5a0/docs/javascript.rst#L18

settings.STATICFILES_DIRS에 static dir 추가

> npm run compile && npm run minify

jquery, react, react-dom 을 django-comments-xtd-2.9.13.js 에 bundling 함

```javascript
{% if page.allow_comments %}
    <script>
       window.comments_props = {% get_commentbox_props for page %};
       window.comments_props_override = {
         allow_comments: true,
         allow_feedback: true,
         show_feedback: true,
         allow_flagging: false,
         polling_interval: 30 * 1000,
       };
    </script>
    <script src="{% url 'javascript-catalog' %}"></script>
    <script src="{% static 'django_comments_xtd/js/django-comments-xtd-2.9.13.min.js' %}"></script>
    <script>
      document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function(tooltipTriggerEl) {
          new bootstrap.Tooltip(tooltipTriggerEl, { html: true });
        });
      });
    </script>
{% endif %}
```
