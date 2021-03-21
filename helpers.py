# Helper functions:

def request_is_valid(request, keys_list):
    """
    Returns True if all keys in 'keys_list'
    are within the 'request' json body.

    Returns False otherwise.
    """
    for key in keys_list:
        if key not in request.json:
            return False
    return True
