# n2_interface.py

"""
The N2 interface handles control plane signaling between the RAN and AMF using
NGAP (Next Generation Application Protocol) over SCTP (Stream Control Transmission Protocol).
"""
from phase1.util.messages.ngap_message import NGAPMessage


class N2Interface:
    """
    N2 interface for RAN-AMF communication over NGAP protocol with SCTP.
    Manages control signaling for registration and handovers.
    """

    def __init__(self, amf):
        self.amf = amf  # Reference to the AMF instance
        self.sctp_sessions = {}  # Track SCTP sessions by UE ID

    def establish_sctp_session(self, ue_id):
        """Establish an SCTP session for NGAP communication with the AMF."""
        self.sctp_sessions[ue_id] = f"SCTP_SESSION_{ue_id}"
        print(f"N2 Interface: Established SCTP session for UE {ue_id}")

    def terminate_sctp_session(self, ue_id):
        """Terminate an SCTP session."""
        if ue_id in self.sctp_sessions:
            del self.sctp_sessions[ue_id]
            print(f"N2 Interface: Terminated SCTP session for UE {ue_id}")

    def send_initial_ue_message(self, ue_id):
        """Send an initial UE message to the AMF over NGAP/SCTP."""
        self.establish_sctp_session(ue_id)
        ngap_message = NGAPMessage(msg_type="INITIAL_UE_MESSAGE", ue_id=ue_id)
        print(f"N2 Interface: Sending Initial UE Message for UE {ue_id} to AMF")
        self.amf.handle_n2_message(ngap_message)

    def send_handover_request(self, ue_id):
        """Send a handover request to the AMF."""
        print(f"N2 Interface: Sending Handover Request for UE {ue_id}")
        # Implement handover logic if needed
