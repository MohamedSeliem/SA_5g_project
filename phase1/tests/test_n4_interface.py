# test_n4_interface.py

import unittest

from phase1.components.smf import SMF
from phase1.components.upf import UPF
from phase1.interfaces.n4_interface import N4Interface


class TestN4Interface(unittest.TestCase):

    def setUp(self):
        self.smf = SMF()
        self.upf = UPF()
        self.n4_interface = N4Interface(self.smf, self.upf)

    def test_setup_session(self):
        """Test setting up a session over N4."""
        ue_id = "UE1"
        parameters = {"QoS": "default", "traffic_rules": {"destination": "DN"}}
        response = self.n4_interface.setup_session(ue_id, parameters)
        self.assertEqual(response.parameters["status"], "success", "Session setup should succeed.")


if __name__ == "__main__":
    unittest.main()
