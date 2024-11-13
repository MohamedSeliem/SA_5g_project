# upf.py

from phase1.util.messages.pfcp_message import PFCPMessage


class UPF:
    """
    UPF simulates the User Plane Function, handling sessions, traffic rules,
    and data forwarding using N3 and N6 interfaces.
    """

    def __init__(self):
        # Store active sessions with session_id as the key
        self.sessions = {}
        self.n3_buffer = []  # Buffer to simulate data packets received on N3
        self.n6_interface = "Data Network (DN)"  # Simplified placeholder for the DN connection

    def handle_pfcp_message(self, pfcp_message):
        """Processes incoming PFCP messages from the SMF and handles session creation, modification, and deletion."""
        if pfcp_message.type == "SESSION_CREATION_REQUEST":
            return self.create_session(pfcp_message)
        elif pfcp_message.type == "SESSION_MODIFICATION_REQUEST":
            return self.modify_session(pfcp_message)
        elif pfcp_message.type == "SESSION_DELETION_REQUEST":
            return self.delete_session(pfcp_message)
        else:
            print("UPF: Received unknown PFCP message type.")
            return None

    def create_session(self, pfcp_message):
        """Creates a new session in the UPF based on PFCP session creation request."""
        session_id = pfcp_message.session_id
        ue_id = pfcp_message.ue_id
        parameters = pfcp_message.parameters

        # Store session with basic traffic rules
        self.sessions[session_id] = {
            "ue_id": ue_id,
            "parameters": parameters,
            "status": "active",
            "traffic_rules": parameters.get("traffic_rules", {}),
            "n3_address": f"UE_{ue_id}_N3"  # Simulated N3 address for the session
        }

        print(f"UPF: Created session {session_id} for UE {ue_id} with parameters {parameters}")

        # Send a successful response to SMF
        return PFCPMessage(
            msg_type="SESSION_CREATION_RESPONSE",
            session_id=session_id,
            parameters={"status": "success"}
        )

    def create_forwarding_session(self, session_id):
        """Initialize a session in UPF to allow data forwarding."""
        print(f"UPF: Creating session {session_id}")
        self.sessions[session_id] = {"status": "active"}  # Session setup with default properties

    def modify_session(self, pfcp_message):
        """Modifies an existing session based on PFCP session modification request."""
        session_id = pfcp_message.session_id
        if session_id in self.sessions:
            # Update session parameters
            new_parameters = pfcp_message.parameters
            self.sessions[session_id]["parameters"].update(new_parameters)
            self.sessions[session_id]["traffic_rules"].update(new_parameters.get("traffic_rules", {}))

            print(f"UPF: Modified session {session_id} with new parameters {new_parameters}")

            # Send a successful modification response
            return PFCPMessage(
                msg_type="SESSION_MODIFICATION_RESPONSE",
                session_id=session_id,
                parameters={"status": "success"}
            )
        else:
            print(f"UPF: Session {session_id} not found for modification.")
            return PFCPMessage(
                msg_type="SESSION_MODIFICATION_RESPONSE",
                session_id=session_id,
                parameters={"status": "failure"}
            )

    def delete_session(self, pfcp_message):
        """Deletes an existing session based on PFCP session deletion request."""
        session_id = pfcp_message.session_id
        if session_id in self.sessions:
            # Remove session from active sessions
            del self.sessions[session_id]
            print(f"UPF: Deleted session {session_id}")

            # Send a successful deletion response
            return PFCPMessage(
                msg_type="SESSION_DELETION_RESPONSE",
                session_id=session_id,
                parameters={"status": "success"}
            )
        else:
            print(f"UPF: Session {session_id} not found for deletion.")
            return PFCPMessage(
                msg_type="SESSION_DELETION_RESPONSE",
                session_id=session_id,
                parameters={"status": "failure"}
            )

    def receive_on_n3(self, session_id, data_packet):
        """Receives a data packet on the N3 interface, simulating GTP-U packet reception."""
        if session_id in self.sessions:
            print(f"UPF: Received packet on N3 for session {session_id}. Queuing for forwarding.")
            self.n3_buffer.append((session_id, data_packet))  # Queue packet for forwarding
        else:
            print(f"UPF: Session {session_id} not found. Packet dropped.")

    def forward_packet(self, session_id):
        """Forwards a packet from the N3 buffer to the N6 interface based on session rules."""
        if session_id not in self.sessions:
            print(f"UPF: Session {session_id} not found. Unable to forward packet.")
            return "Packet dropped - no active session"

        # Process each packet for the session from the N3 buffer
        packets = [pkt for pkt in self.n3_buffer if pkt[0] == session_id]
        for _, data_packet in packets:
            # Forward packet based on traffic rules
            traffic_rules = self.sessions[session_id].get("traffic_rules", {})
            destination = traffic_rules.get("destination", self.n6_interface)
            print(f"UPF: Forwarding packet for session {session_id} to {destination}")
            self.n3_buffer.remove((session_id, data_packet))  # Remove packet from buffer after forwarding

        return f"Packets forwarded to {destination}" if packets else "No packets to forward"

    def has_received_data(self, session_id):
        """
        Check if there are any data packets in the N3 buffer for the given session_id.
        Returns True if data is found, otherwise False.
        """
        # Check if any packet in n3_buffer belongs to the specified session_id
        return any(packet[0] == session_id for packet in self.n3_buffer)
