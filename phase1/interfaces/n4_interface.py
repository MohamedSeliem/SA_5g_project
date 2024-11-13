# n4_interface.py
from phase1.util.messages.pfcp_message import PFCPMessage


class N4Interface:
    """
    N4 interface for SMF-UPF communication over PFCP protocol.
    Manages session setup, modification, deletion, and policy updates.
    """

    def __init__(self, smf, upf):
        self.smf = smf  # Reference to the SMF instance
        self.upf = upf  # Reference to the UPF instance

    def setup_session(self, ue_id, parameters):
        """Set up a new session by sending a PFCP session creation request."""
        session_id = self.smf.next_session_id
        pfcp_request = PFCPMessage(
            msg_type="SESSION_CREATION_REQUEST",
            session_id=session_id,
            ue_id=ue_id,
            parameters=parameters
        )
        print(f"N4 Interface: Setting up session for UE {ue_id}")
        response = self.upf.handle_pfcp_message(pfcp_request)
        return response

    def modify_session(self, session_id, parameters):
        """Modify an existing session by updating PFCP rules."""
        pfcp_request = PFCPMessage(
            msg_type="SESSION_MODIFICATION_REQUEST",
            session_id=session_id,
            parameters=parameters
        )
        print(f"N4 Interface: Modifying session {session_id}")
        response = self.upf.handle_pfcp_message(pfcp_request)
        return response

    def update_policy_rules(self, session_id, policy_rules):
        """Send policy updates to the UPF for traffic management."""
        pfcp_request = PFCPMessage(
            msg_type="POLICY_UPDATE_REQUEST",
            session_id=session_id,
            parameters={"policy_rules": policy_rules}
        )
        print(f"N4 Interface: Updating policy rules for session {session_id}")
        response = self.upf.handle_pfcp_message(pfcp_request)
        return response

    def delete_session(self, session_id):
        """Delete an existing session."""
        pfcp_request = PFCPMessage(
            msg_type="SESSION_DELETION_REQUEST",
            session_id=session_id
        )
        print(f"N4 Interface: Deleting session {session_id}")
        response = self.upf.handle_pfcp_message(pfcp_request)
        return response
