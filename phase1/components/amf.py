# amf.py
from phase1.util.authenticator import Authenticator
from phase1.util.messages.nas_message import NASMessage


class AMF:
    def __init__(self, ue=None):
        # Initialize AMF states and interfaces
        self.ue_registry = {}  # Dictionary to track registered UEs
        self.authenticator = Authenticator()  # Authentication handler
        self.ue = ue

    # N1 interface - Handle NAS messages from UE
    def handle_n1_message(self, nas_message):
        if nas_message.type == "REGISTRATION_REQUEST":
            self.process_registration_request(nas_message)
        elif nas_message.type == "AUTHENTICATION_RESPONSE":
            self.process_authentication_response(nas_message)
        # Add more NAS message types as needed

    # N2 interface - Handle NGAP messages from RAN
    def handle_n2_message(self, ngap_message):
        if ngap_message.type == "INITIAL_UE_MESSAGE":
            # Start registration/authentication for new UE
            self.initiate_registration(ngap_message)
        # Add additional NGAP message types as necessary

    def process_registration_request(self, nas_message):
        ue_id = nas_message.ue_id
        print(f"AMF: Processing registration request from UE {ue_id}")

        # Initiate authentication for the UE
        auth_request = self.authenticator.create_auth_request(ue_id)
        self.send_n1_message(auth_request)

    def process_authentication_response(self, nas_message):
        """Verifies the authentication response and completes registration if valid."""
        ue_id = nas_message.ue_id
        print(f"AMF: Received AUTHENTICATION_RESPONSE from UE {ue_id}")
        if self.verify_authentication(ue_id, nas_message):
            self.complete_registration(ue_id)
            print(f"UE {ue_id} registered successfully.")
        else:
            print(f"Authentication failed for UE {ue_id}.")

    def verify_authentication(self, ue_id, nas_message):
        """
        Verify the UE's authentication response by checking credentials.
        """
        # Verify the response using the authenticator
        return self.authenticator.verify_credentials(ue_id, nas_message.payload.get("credentials"))

    def initiate_registration(self, ngap_message):
        # Extract UE ID and initiate NAS messaging
        ue_id = ngap_message.ue_id
        print(f"AMF: Received initial UE message from RAN for UE {ue_id}")

        # Send registration request to UE
        registration_request = NASMessage(msg_type="REGISTRATION_REQUEST", ue_id=ue_id)
        self.handle_n1_message(registration_request)

    def send_n1_message(self, nas_message):
        """Send a NAS message to the UE, triggering the UE's response as needed."""
        print(f"AMF: Sending NAS message {nas_message.type} to UE {nas_message.ue_id}")

        # Directly call the UE's response method based on the message type
        if nas_message.type == "AUTHENTICATION_REQUEST" and self.ue:
            self.ue.receive_authentication_request(nas_message)

    def complete_registration(self, ue_id):
        # Mark the UE as registered
        self.ue_registry[ue_id] = True
        print(f"AMF: Registration complete for UE {ue_id}")
