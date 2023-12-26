from wagtail import hooks


@hooks.register("insert_global_admin_js", order=-1)
def global_admin_js():
    """global admin javascript"""

    return """
        <script>
            window.addEventListener("DOMContentLoaded", function () {
              // fix wagtail's URLify
              // https://github.com/wagtail/wagtail/blob/2b061ac96e5ffdad2759e39bfdbca0fc242ae854/client/src/utils/urlify.ts#L13
              window.URLify = function() {return;};
            });
        </script>
    """
