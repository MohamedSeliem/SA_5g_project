# n3_interface.py

"""
The N3 interface forwards user data packets from the RAN to the UPF using GTP-U (GPRS Tunneling Protocol - User Plane).
"""
from phase1.util.messages.gtpu_message import GTPUPacket


class N3Interface:
    """
    N3 interface for RAN-UPF communication over GTP-U protocol.
    Manages data packet forwarding with GTP-U encapsulation.
    """

    def __init__(self, upf):
        self.upf = upf  # Reference to the UPF instance
        self.tunnels = {}  # Track GTP-U tunnels by session ID

    def establish_gtp_u_tunnel(self, session_id):
        """Establish a GTP-U tunnel for user data forwarding."""
        self.tunnels[session_id] = f"GTPU_TUNNEL_{session_id}"
        print(f"N3 Interface: Established GTP-U tunnel for session {session_id}")
        # Ensure UPF session is created when the tunnel is established
        self.upf.create_forwarding_session(session_id)

    def close_gtp_u_tunnel(self, session_id):
        """Close an existing GTP-U tunnel."""
        if session_id in self.tunnels:
            del self.tunnels[session_id]
            print(f"N3 Interface: Closed GTP-U tunnel for session {session_id}")

    def forward_user_data(self, session_id, data_packet):
        """Encapsulate and forward user data packet to UPF over GTP-U."""
        if session_id not in self.tunnels:
            self.establish_gtp_u_tunnel(session_id)

        gtp_packet = GTPUPacket(session_id, data_packet)
        print(f"N3 Interface: Forwarding GTP-U packet for session {session_id} to UPF")
        self.upf.receive_on_n3(session_id, gtp_packet)
