class NGAPMessage:
    """
    Represents an NGAP message structure for N2 interface communication.
    """
    def __init__(self, msg_type, ue_id, payload=None):
        self.type = msg_type
        self.ue_id = ue_id
        self.payload = payload or {}