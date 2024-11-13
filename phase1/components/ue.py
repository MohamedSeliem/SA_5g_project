# ue.py

from phase1.interfaces.n1_interface import N1Interface


class UE:
    """
    User Equipment (UE) class simulating registration, authentication, and data transmission.
    """

    def __init__(self, ue_id, amf):
        self.ue_id = ue_id
        # Set up N1 interface with reference to AMF and self for bidirectional communication
        self.n1_interface = N1Interface(amf, ue=self)

    def register(self):
        """Send a registration request to the AMF over the N1 interface."""
        print(f"UE {self.ue_id}: Initiating registration.")
        self.n1_interface.send_registration_request(self.ue_id)

    def authenticate(self, credentials):
        """Send an authentication response to the AMF over the N1 interface."""
        print(f"UE {self.ue_id}: Responding with authentication credentials.")
        self.n1_interface.send_authentication_response(self.ue_id, credentials)

    def receive_authentication_request(self, nas_message):
        """Receive an authentication request from the AMF and respond."""
        print(f"UE {self.ue_id}: Received authentication request from AMF.")
        # Automatically respond with credentials (for testing purposes)
        self.authenticate(credentials="password123")

    def send_data(self, ran, data_packet):
        """Simulate sending data to the RAN, which forwards to UPF."""
        print(f"UE {self.ue_id}: Sending data packet to RAN.")
        ran.receive_data_from_ue(self.ue_id, data_packet)
