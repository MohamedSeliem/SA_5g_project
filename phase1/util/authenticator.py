# authenticator.py

from phase1.util.messages.nas_message import NASMessage

class Authenticator:
    def __init__(self):
        # Simple dictionary-based credential storage for illustration
        self.credentials_store = {"UE1": "password123"}  # Replace with real authentication logic

    def create_auth_request(self, ue_id):
        """Generate an authentication request message for the UE."""
        print(f"Authenticator: Generating authentication request for UE {ue_id}")
        return NASMessage(msg_type="AUTHENTICATION_REQUEST", ue_id=ue_id)

    def verify_response(self, nas_message):
        """
        Verify the response by checking credentials provided in NASMessage payload.
        This method assumes that the credentials are provided in the payload dictionary.
        """
        ue_id = nas_message.ue_id
        provided_credentials = nas_message.payload.get("credentials")
        return self.verify_credentials(ue_id, provided_credentials)

    def verify_credentials(self, ue_id, credentials):
        """
        Verifies if the provided credentials match the stored credentials.
        Called directly from AMF during the authentication process.
        """
        stored_credentials = self.credentials_store.get(ue_id)
        if credentials == stored_credentials:
            print(f"Authenticator: Authentication successful for UE {ue_id}")
            return True
        print(f"Authenticator: Authentication failed for UE {ue_id}")
        return False
