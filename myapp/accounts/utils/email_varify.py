import re
def is_valid_email(email_):
    pattern = r'^[a-zA-Z0-9]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}+$'
    return re.match(pattern, email_) is not None
