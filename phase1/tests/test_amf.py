# test_amf.py

import unittest
from phase1.components.amf import AMF
from phase1.components.ue import UE
from phase1.util.authenticator import NASMessage
from phase1.util.messages.ngap_message import NGAPMessage


class TestAMF(unittest.TestCase):

    def setUp(self):
        """Initialize AMF instance before each test."""
        self.amf = AMF()
        self.ue = UE(ue_id="UE1", amf=self.amf)

    def test_registration_and_successful_authentication(self):
        """Test AMF registration and successful authentication."""
        self.amf.ue = self.ue
        # Simulate an initial UE message from the RAN
        initial_ue_message = NGAPMessage(msg_type="INITIAL_UE_MESSAGE", ue_id="UE1")
        self.amf.handle_n2_message(initial_ue_message)

        # Simulate a registration request from UE1 to AMF
        registration_request = NASMessage(msg_type="REGISTRATION_REQUEST", ue_id="UE1")
        self.amf.handle_n1_message(registration_request)

        # Simulate an authentication response from UE1 (successful case)
        auth_response_success = NASMessage(
            msg_type="AUTHENTICATION_RESPONSE",
            ue_id="UE1",
            payload={"credentials": "password123"}
        )
        self.amf.handle_n1_message(auth_response_success)

        # Verify that UE1 is registered
        self.assertTrue(self.amf.ue_registry.get("UE1"), "UE1 should be registered successfully.")

    def test_failed_authentication(self):
        """Test AMF registration with failed authentication."""

        # Simulate an initial UE message from the RAN
        initial_ue_message = NGAPMessage(msg_type="INITIAL_UE_MESSAGE", ue_id="UE1")
        self.amf.handle_n2_message(initial_ue_message)

        # Simulate a registration request from UE1 to AMF
        registration_request = NASMessage(msg_type="REGISTRATION_REQUEST", ue_id="UE1")
        self.amf.handle_n1_message(registration_request)

        # Simulate an authentication response from UE1 (failure case)
        auth_response_failure = NASMessage(
            msg_type="AUTHENTICATION_RESPONSE",
            ue_id="UE1",
            payload={"credentials": "wrongpassword"}
        )
        self.amf.handle_n1_message(auth_response_failure)

        # Verify that UE1 is not registered due to failed authentication
        self.assertIsNone(self.amf.ue_registry.get("UE1"), "UE1 should not be registered.")


if __name__ == "__main__":
    unittest.main()
