def user_string_format(user):
    return user.properties.get('label', user.email)
