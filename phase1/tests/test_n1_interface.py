# test_n1_interface.py

import unittest

from phase1.components.amf import AMF
from phase1.components.ue import UE
from phase1.interfaces.n1_interface import N1Interface
from phase1.util.messages.nas_message import NASMessage


class TestN1Interface(unittest.TestCase):

    def setUp(self):
        self.amf = AMF()
        self.ue = UE(ue_id="UE1", amf=self.amf)
        self.amf.ue = self.ue
        self.n1_interface = N1Interface(self.amf, self.ue)

    def test_send_registration_request(self):
        """Test sending a registration request over N1."""
        ue_id = "UE1"
        self.n1_interface.send_registration_request(ue_id)
        self.assertIn(ue_id, self.amf.ue_registry, "UE should be registered in AMF registry.")

    def test_verify_authentication_success(self):
        """Test successful authentication for a UE."""
        ue_id = "UE1"
        credentials = "password123"

        # Create a NASMessage with the correct credentials
        nas_message = NASMessage(
            msg_type="AUTHENTICATION_RESPONSE",
            ue_id=ue_id,
            payload={"credentials": credentials}
        )

        # Call verify_authentication with both ue_id and nas_message
        self.assertTrue(
            self.amf.verify_authentication(ue_id, nas_message),
            "Authentication should succeed."
        )

    def test_verify_authentication_failure(self):
        """Test failed authentication due to incorrect credentials."""
        ue_id = "UE1"
        incorrect_credentials = "wrongpassword"

        # Create a NASMessage with incorrect credentials
        nas_message = NASMessage(
            msg_type="AUTHENTICATION_RESPONSE",
            ue_id=ue_id,
            payload={"credentials": incorrect_credentials}
        )

        # Call verify_authentication with both ue_id and nas_message
        self.assertFalse(
            self.amf.verify_authentication(ue_id, nas_message),
            "Authentication should fail with incorrect credentials."
        )


if __name__ == "__main__":
    unittest.main()
