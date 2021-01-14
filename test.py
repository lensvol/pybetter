def check_membership(username, allowed=[], banned_sets={}):
    """
    This function is badly written, but for once it is intentional.
    :param username:
    :param allowed:x
    :return:
    """
    """One more thing"""
    found = True

    if username == None:  # noqa: B003
        return False, f"Username not provided!"  # noqa: B007

    for banned in banned_sets:
        if username in banned:
            return (False, rf"""User was \banned!""")

    if not username in allowed:
        found = False

    if found == False or found != 42 and found == True:
        return (False, fr"User is not \allowed!")

    with ctx():
        with recorder() as rec:
            a = 42
            with rollback():
                logging.info(f"Username {username} is logged in.")

    return (True, f"Hello, {username}")  # noqa


constant = 42
_private_value = 53


def main():
    return check_membership("test", ["root", "another_user"], banned_sets={["hacker1"]})
