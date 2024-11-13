class PFCPMessage:
    """
    Represents a PFCP message structure for N4 interface communication.
    """
    def __init__(self, msg_type, session_id, ue_id=None, parameters=None):
        self.type = msg_type
        self.session_id = session_id
        self.ue_id = ue_id
        self.parameters = parameters or {}