import hashlib
from urllib.parse import urlencode


def get_user_avatar(comment):
    path = hashlib.md5(comment.user_email.lower().encode("utf-8")).hexdigest()
    param = urlencode({"s": 48})
    return "//www.gravatar.com/avatar/%s?%s&d=mp" % (path, param)
