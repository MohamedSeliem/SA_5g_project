# test_smf.py

import unittest
from phase1.components.smf import SMF
from phase1.components.upf import UPF


class TestSMFIntegration(unittest.TestCase):

    def setUp(self):
        """Initialize SMF and UPF instances before each test."""
        self.smf = SMF()
        self.upf = UPF()

    def test_session_creation(self):
        """Test session creation in SMF and communication with UPF."""
        ue_id = "UE1"
        self.smf.create_session(ue_id, self.upf)

        # Verify session creation in SMF
        self.assertTrue(self.smf.sessions, "Session should be created in SMF.")
        self.assertIn("UE1", self.smf.sessions[1]["parameters"]["traffic_rules"]["n3_interface"],
                      "N3 interface should be assigned.")

    def test_session_modification(self):
        """Test session modification with new traffic rules."""
        # First, create a session
        ue_id = "UE1"
        self.smf.create_session(ue_id, self.upf)

        # Modify session with new parameters
        session_id = 1
        new_parameters = {"QoS": "high-priority", "traffic_rules": {"destination": "CustomDN"}}
        self.smf.modify_session(session_id, new_parameters, self.upf)

        # Verify that session parameters were updated
        session_info = self.smf.get_session_info(session_id)
        self.assertEqual(session_info["parameters"]["QoS"], "high-priority", "QoS should be updated to high-priority.")

    def test_session_deletion(self):
        """Test session deletion in SMF and UPF integration."""
        # First, create a session
        ue_id = "UE1"
        self.smf.create_session(ue_id, self.upf)

        # Delete the session
        session_id = 1
        self.smf.delete_session(session_id, self.upf)

        # Verify session deletion in SMF
        self.assertNotIn(session_id, self.smf.sessions, "Session should be deleted from SMF.")


if __name__ == "__main__":
    unittest.main()
