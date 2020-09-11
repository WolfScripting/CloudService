
def add_uid_to_user(backend, user, response, uid, *args, **kwargs):

    # Adds the users Steam ID to the User object

    if backend.name == 'steam':
        user.steam_id = uid
        user.save()
        