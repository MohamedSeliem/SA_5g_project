# test_n3_interface.py

import unittest

from phase1.components.upf import UPF
from phase1.interfaces.n3_interface import N3Interface


class TestN3Interface(unittest.TestCase):

    def setUp(self):
        self.upf = UPF()
        self.n3_interface = N3Interface(self.upf)

    def test_establish_gtp_u_tunnel(self):
        """Test establishing a GTP-U tunnel."""
        session_id = 1
        self.n3_interface.establish_gtp_u_tunnel(session_id)
        self.assertIn(session_id, self.n3_interface.tunnels, "GTP-U tunnel should be established.")

    def test_forward_user_data(self):
        """Test forwarding user data over GTP-U."""
        session_id = 1
        data_packet = "Sample data packet"

        # Ensure the session is established first
        self.n3_interface.establish_gtp_u_tunnel(session_id)

        # Forward data packet to the UPF using N3 interface
        self.n3_interface.forward_user_data(session_id, data_packet)

        # Check if the data packet was received in the UPF's N3 buffer
        self.assertTrue(
            self.upf.has_received_data(session_id),
            "UPF should receive the forwarded data."
        )


if __name__ == "__main__":
    unittest.main()
