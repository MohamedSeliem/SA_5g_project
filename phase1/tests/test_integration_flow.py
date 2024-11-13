# test_integration_flow.py

import unittest
from phase1.components.amf import AMF
from phase1.components.smf import SMF
from phase1.components.upf import UPF
from phase1.components.ue import UE
from phase1.components.ran import RAN
from phase1.interfaces.n1_interface import N1Interface
from phase1.interfaces.n2_interface import N2Interface
from phase1.interfaces.n3_interface import N3Interface
from phase1.interfaces.n4_interface import N4Interface


class TestIntegrationFlow(unittest.TestCase):

    def setUp(self):
        # Initialize components
        self.amf = AMF()
        self.smf = SMF()
        self.upf = UPF()
        self.ue = UE(ue_id="UE1", amf=self.amf)
        self.amf.ue = self.ue
        self.ran = RAN(self.amf, self.upf)

        # Initialize interfaces
        self.n1_interface = N1Interface(self.amf, self.ue)
        self.n2_interface = N2Interface(self.amf)
        self.n3_interface = N3Interface(self.upf)
        self.n4_interface = N4Interface(self.smf, self.upf)

    def test_registration_and_authentication_flow(self):
        """Test the complete registration and authentication flow."""
        # UE initiates registration via N1 interface
        self.ue.register()
        # Verify UE is in the AMF registry after registration
        self.assertIn("UE1", self.amf.ue_registry, "UE should be registered in AMF registry.")

        # UE responds to authentication request
        self.ue.authenticate(credentials="password123")

        # Verify authentication success
        self.assertTrue(self.amf.ue_registry["UE1"], "UE should be authenticated successfully.")

    def test_session_creation_flow(self):
        """Test the session creation flow between SMF and UPF."""
        # SMF initiates session creation request to UPF via N4 interface
        session_parameters = {"QoS": "default", "traffic_rules": {"destination": "Data Network"}}
        response = self.n4_interface.setup_session("UE1", session_parameters)

        # Verify session creation success
        self.assertEqual(response.parameters["status"], "success", "Session creation should succeed in UPF.")
        self.assertIn(1, self.upf.sessions, "Session should be created in UPF.")

    def test_data_forwarding_flow(self):
        """Test the data forwarding from UE through RAN to UPF."""
        # Ensure a session is created first
        session_parameters = {"QoS": "default", "traffic_rules": {"destination": "Data Network"}}
        self.n4_interface.setup_session("UE1", session_parameters)

        # UE sends data packet through RAN
        data_packet = "Test data packet"
        self.ue.send_data(self.ran, data_packet)

        # UPF receives data on N3
        self.assertTrue(self.upf.has_received_data(1), "UPF should have received data on N3.")

        # Forward data from UPF to Data Network
        forwarding_result = self.upf.forward_packet(1)
        self.assertIn("Packets forwarded to Data Network", forwarding_result,
                      "Packets should be forwarded to Data Network.")

    def test_end_to_end_flow(self):
        """Test the complete end-to-end flow from registration to data forwarding."""
        # Step 1: Registration and Authentication
        self.ue.register()
        self.ue.authenticate(credentials="password123")
        self.assertIn("UE1", self.amf.ue_registry, "UE should be registered and authenticated.")

        # Step 2: Session Creation
        session_parameters = {"QoS": "default", "traffic_rules": {"destination": "Data Network"}}
        session_response = self.n4_interface.setup_session("UE1", session_parameters)
        self.assertEqual(session_response.parameters["status"], "success", "Session creation should succeed.")

        # Step 3: Data Forwarding
        data_packet = "Final end-to-end test packet"
        self.ue.send_data(self.ran, data_packet)

        # Verify UPF receives and forwards the data
        self.assertTrue(self.upf.has_received_data(1), "UPF should have received data on N3.")
        final_result = self.upf.forward_packet(1)
        self.assertIn("Packets forwarded to Data Network", final_result, "Packets should be forwarded to Data Network.")


if __name__ == "__main__":
    unittest.main()
