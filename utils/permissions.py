# utils/permissions.py

def funcpermission(user, codename):
    return codename in user.permissions_codenames