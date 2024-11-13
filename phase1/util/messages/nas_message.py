class NASMessage:
    """
    Represents a NAS message structure for N1 interface communication.
    """
    def __init__(self, msg_type, ue_id, payload=None):
        self.type = msg_type
        self.ue_id = ue_id
        self.payload = payload or {}

        # If the message is an authentication response, ensure credentials are included in the payload
        if msg_type == "AUTHENTICATION_RESPONSE" and "credentials" not in self.payload:
            raise ValueError("Credentials must be provided for AUTHENTICATION_RESPONSE messages.")
