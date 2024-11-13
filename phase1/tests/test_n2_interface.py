# test_n2_interface.py

import unittest

from phase1.components.amf import AMF
from phase1.components.ue import UE
from phase1.interfaces.n2_interface import N2Interface


class TestN2Interface(unittest.TestCase):

    def setUp(self):
        self.amf = AMF()
        self.ue = UE(ue_id="UE1", amf=self.amf)
        self.amf.ue = self.ue
        self.n2_interface = N2Interface(self.amf)

    def test_establish_and_terminate_sctp_session(self):
        """Test SCTP session establishment and termination."""
        ue_id = "UE1"
        self.n2_interface.establish_sctp_session(ue_id)
        self.assertIn(ue_id, self.n2_interface.sctp_sessions, "SCTP session should be established.")
        self.n2_interface.terminate_sctp_session(ue_id)
        self.assertNotIn(ue_id, self.n2_interface.sctp_sessions, "SCTP session should be terminated.")

    def test_send_initial_ue_message(self):
        """Test sending an initial UE message over N2."""
        ue_id = "UE1"
        self.n2_interface.send_initial_ue_message(ue_id)
        self.assertIn(ue_id, self.amf.ue_registry, "UE should be registered in AMF registry.")


if __name__ == "__main__":
    unittest.main()
