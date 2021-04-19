import sms  # import SMS Module
import dal  # import Data Access Layer

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


def send_sms_to_guest(guest_id, message_body):
    """
    Sends an SMS message to a guest with a given Id, and a message body.

    Returns True if succeeds (i.e., guest exists in the database).
    Returns False otherwise.
    """
    # get guest from database:
    target_guest = dal.get_guest_by_id(guest_id)

    if target_guest is not None:
        # get guest's phone number to be able to send the message
        target_phone_number = target_guest.PhoneNumber
        sms.send_sms(target_phone_number, message_body)
