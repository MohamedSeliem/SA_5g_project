class GTPUPacket:
    """
    Represents a GTP-U packet with encapsulated user data for N3 interface communication.
    """
    def __init__(self, session_id, data_packet):
        self.session_id = session_id
        self.data_packet = data_packet