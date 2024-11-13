from phase1.util.messages.pfcp_message import PFCPMessage


class SMF:
    """
    SMF handles session management by communicating with the UPF over the N4 interface.
    """
    def __init__(self):
        # Session tracking
        self.sessions = {}  # Dictionary to track active sessions with session_id as key
        self.next_session_id = 1  # Simple counter for session IDs

    def create_session(self, ue_id, upf):
        """
        Creates a new session for a given UE and sends a PFCP session creation request to the UPF.
        Configures default routing rules for traffic from UE to DN.
        """
        session_id = self.next_session_id
        self.next_session_id += 1

        # Define default parameters, including routing rules and QoS
        parameters = {
            "QoS": "default",
            "routing_policy": "basic",
            "traffic_rules": {
                "destination": "DN",  # Default destination is the Data Network
                "n3_interface": f"UE_{ue_id}_N3",  # Simulated N3 address
                "n6_interface": "DN"  # Default N6 interface
            }
        }

        # Build and send PFCP session creation request to UPF
        pfcp_request = PFCPMessage(
            msg_type="SESSION_CREATION_REQUEST",
            session_id=session_id,
            ue_id=ue_id,
            parameters=parameters
        )
        print(f"SMF: Sending session creation request for UE {ue_id} with Session ID {session_id}")

        # Send request to UPF and handle response
        response = upf.handle_pfcp_message(pfcp_request)
        if response and response.type == "SESSION_CREATION_RESPONSE" and response.parameters.get("status") == "success":
            self.sessions[session_id] = {"ue_id": ue_id, "parameters": parameters}
            print(f"SMF: Session {session_id} created successfully for UE {ue_id}")
        else:
            print(f"SMF: Failed to create session for UE {ue_id}")

    def modify_session(self, session_id, new_parameters, upf):
        """
        Modifies an existing session by updating parameters and sending a PFCP modification request to the UPF.
        Ensures updated routing rules are provided if applicable.
        """
        if session_id in self.sessions:
            # Update session parameters, including any traffic rules
            self.sessions[session_id]["parameters"].update(new_parameters)
            pfcp_request = PFCPMessage(
                msg_type="SESSION_MODIFICATION_REQUEST",
                session_id=session_id,
                parameters=new_parameters
            )
            print(f"SMF: Sending session modification request for Session ID {session_id}")

            # Send modification request to UPF and handle response
            response = upf.handle_pfcp_message(pfcp_request)
            if response and response.type == "SESSION_MODIFICATION_RESPONSE" and response.parameters.get("status") == "success":
                print(f"SMF: Session {session_id} modified successfully.")
            else:
                print(f"SMF: Failed to modify session {session_id}.")
        else:
            print(f"SMF: Session {session_id} not found.")

    def delete_session(self, session_id, upf):
        """
        Deletes an active session by sending a PFCP session deletion request to the UPF.
        """
        if session_id in self.sessions:
            pfcp_request = PFCPMessage(
                msg_type="SESSION_DELETION_REQUEST",
                session_id=session_id
            )
            print(f"SMF: Sending session deletion request for Session ID {session_id}")

            # Send deletion request to UPF and handle response
            response = upf.handle_pfcp_message(pfcp_request)
            if response and response.type == "SESSION_DELETION_RESPONSE" and response.parameters.get("status") == "success":
                del self.sessions[session_id]
                print(f"SMF: Session {session_id} deleted successfully.")
            else:
                print(f"SMF: Failed to delete session {session_id}.")
        else:
            print(f"SMF: Session {session_id} not found.")

    def get_session_info(self, session_id):
        """
        Retrieves information about an active session, including UE ID and session parameters.
        """
        session_info = self.sessions.get(session_id)
        if session_info:
            print(f"SMF: Session {session_id} info - {session_info}")
            return session_info
        else:
            print(f"SMF: Session {session_id} not found.")
            return None
