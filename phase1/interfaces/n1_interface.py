# n1_interface.py

"""
The N1 interface will handle registration and authentication signaling between the UE and AMF.
This interface typically uses NAS (Non-Access Stratum) over IP to carry signaling messages.
"""
from phase1.util.messages.nas_message import NASMessage


class N1Interface:
    """
    N1 interface for UE-AMF communication over NAS protocol.
    Supports registration, authentication, and session management.
    """

    def __init__(self, amf=None, ue=None):
        # Reference to AMF and UE instances
        self.amf = amf
        self.ue = ue

    def send_registration_request(self, ue_id):
        """Send a registration request from the UE to the AMF."""
        nas_message = NASMessage(msg_type="REGISTRATION_REQUEST", ue_id=ue_id)
        print(f"N1 Interface: Sending registration request from UE {ue_id} to AMF")
        self.amf.handle_n1_message(nas_message)

    def send_authentication_response(self, ue_id, credentials):
        """Send an authentication response from the UE to the AMF."""
        # Pass credentials as part of the payload for the authentication response
        nas_message = NASMessage(
            msg_type="AUTHENTICATION_RESPONSE",
            ue_id=ue_id,
            payload={"credentials": credentials}
        )
        print(f"N1 Interface: Sending authentication response from UE {ue_id} to AMF")
        self.amf.handle_n1_message(nas_message)

    def send_authentication_request_to_ue(self, ue_id):
        """Send an authentication request from AMF to UE."""
        auth_request = NASMessage(msg_type="AUTHENTICATION_REQUEST", ue_id=ue_id)
        print(f"N1 Interface: Sending authentication request to UE {ue_id}")
        self.ue.receive_authentication_request(auth_request)

    def send_deregistration_request(self, ue_id):
        """Send a deregistration request from the UE to the AMF."""
        nas_message = NASMessage(msg_type="DEREGISTRATION_REQUEST", ue_id=ue_id)
        print(f"N1 Interface: Sending deregistration request from UE {ue_id} to AMF")
        self.amf.handle_n1_message(nas_message)
