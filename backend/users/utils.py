def get_user_role(user):
    groups = user.groups.all()
    if groups.count() != 1:
        raise Exception("User must have exactly one role")
    return groups.first().name
