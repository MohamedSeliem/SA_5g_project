# ran.py

from phase1.interfaces.n2_interface import N2Interface
from phase1.interfaces.n3_interface import N3Interface


class RAN:
    """
    Radio Access Network (RAN) class simulating control signaling and user data forwarding.
    """

    def __init__(self, amf, upf):
        self.n2_interface = N2Interface(amf)
        self.n3_interface = N3Interface(upf)

    def initiate_registration(self, ue_id):
        """Send an initial UE message to the AMF to initiate registration."""
        print(f"RAN: Sending Initial UE Message for UE {ue_id}.")
        self.n2_interface.send_initial_ue_message(ue_id)

    def receive_data_from_ue(self, ue_id, data_packet):
        """Receive data from UE and forward it to UPF."""
        print(f"RAN: Receiving data from UE {ue_id} and forwarding to UPF.")
        session_id = 1  # Example session ID, this should be managed based on established sessions
        self.n3_interface.forward_user_data(session_id, data_packet)
