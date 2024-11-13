# test_upf.py

import unittest
from phase1.components.upf import UPF
from phase1.util.messages.pfcp_message import PFCPMessage


class TestUPF(unittest.TestCase):

    def setUp(self):
        """Initialize UPF instance before each test."""
        self.upf = UPF()

    def test_session_creation(self):
        """Test UPF session creation."""
        pfcp_creation_message = PFCPMessage(
            msg_type="SESSION_CREATION_REQUEST",
            session_id=1,
            ue_id="UE1",
            parameters={
                "QoS": "default",
                "traffic_rules": {"destination": "DN"}
            }
        )
        response = self.upf.handle_pfcp_message(pfcp_creation_message)
        self.assertEqual(response.type, "SESSION_CREATION_RESPONSE", "Response should be SESSION_CREATION_RESPONSE.")
        self.assertEqual(response.parameters["status"], "success", "Session creation should succeed.")

    def test_packet_forwarding(self):
        """Test UPF packet forwarding with session setup, packet reception, and forwarding."""

        # Step 1: Create a session to set up routing rules
        pfcp_creation_message = PFCPMessage(
            msg_type="SESSION_CREATION_REQUEST",
            session_id=1,
            ue_id="UE1",
            parameters={
                "QoS": "default",
                "traffic_rules": {"destination": "DN"}
            }
        )
        creation_response = self.upf.handle_pfcp_message(pfcp_creation_message)
        self.assertEqual(creation_response.type, "SESSION_CREATION_RESPONSE", "Expected session creation response")
        self.assertEqual(creation_response.parameters["status"], "success", "Session creation should succeed.")

        # Step 2: Receive a packet on N3 interface for the created session
        self.upf.receive_on_n3(1, "Sample data packet")
        self.assertIn((1, "Sample data packet"), self.upf.n3_buffer, "Packet should be in N3 buffer after reception")

        # Step 3: Forward the packet to the destination
        forwarding_result = self.upf.forward_packet(1)
        self.assertIn("forwarded to DN", forwarding_result, "Packet should be forwarded to DN.")
        self.assertNotIn((1, "Sample data packet"), self.upf.n3_buffer,
                         "Packet should be removed from N3 buffer after forwarding")

    def test_session_modification(self):
        """Test UPF session modification."""
        # First, create a session
        pfcp_creation_message = PFCPMessage(
            msg_type="SESSION_CREATION_REQUEST",
            session_id=1,
            ue_id="UE1",
            parameters={
                "QoS": "default",
                "traffic_rules": {"destination": "DN"}
            }
        )
        self.upf.handle_pfcp_message(pfcp_creation_message)

        # Modify the session with new parameters
        pfcp_modification_message = PFCPMessage(
            msg_type="SESSION_MODIFICATION_REQUEST",
            session_id=1,
            parameters={"QoS": "high-priority", "traffic_rules": {"destination": "CustomDN"}}
        )
        response = self.upf.handle_pfcp_message(pfcp_modification_message)
        self.assertEqual(response.type, "SESSION_MODIFICATION_RESPONSE",
                         "Response should be SESSION_MODIFICATION_RESPONSE.")
        self.assertEqual(response.parameters["status"], "success", "Session modification should succeed.")

    def test_session_deletion(self):
        """Test UPF session deletion."""
        # First, create a session
        pfcp_creation_message = PFCPMessage(
            msg_type="SESSION_CREATION_REQUEST",
            session_id=1,
            ue_id="UE1",
            parameters={
                "QoS": "default",
                "traffic_rules": {"destination": "DN"}
            }
        )
        self.upf.handle_pfcp_message(pfcp_creation_message)

        # Now delete the session
        pfcp_deletion_message = PFCPMessage(
            msg_type="SESSION_DELETION_REQUEST",
            session_id=1
        )
        response = self.upf.handle_pfcp_message(pfcp_deletion_message)
        self.assertEqual(response.type, "SESSION_DELETION_RESPONSE", "Response should be SESSION_DELETION_RESPONSE.")
        self.assertEqual(response.parameters["status"], "success", "Session deletion should succeed.")


if __name__ == "__main__":
    unittest.main()
