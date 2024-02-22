from google.auth.transport.requests import AuthorizedSession
from google.oauth2.service_account import Credentials
from google.auth import jwt, crypt


class Generic:
    """Demo class for creating and managing Generic passes in Google Wallet.

    Attributes:
        key_file_path: Path to service account key file from Google Cloud
            Console. Environment variable: GOOGLE_APPLICATION_CREDENTIALS.
        base_url: Base URL for Google Wallet API requests.
    """

    def __init__(self):
        self.key_file_path = "KEY.json"
        self.base_url = 'https://walletobjects.googleapis.com/walletobjects/v1'
        self.batch_url = 'https://walletobjects.googleapis.com/batch'
        self.class_url = f'{self.base_url}/genericClass'
        self.object_url = f'{self.base_url}/genericObject'

        # Set up authenticated client
        self.auth()

    def auth(self):
        """Create authenticated HTTP client using a service account file."""
        self.credentials = Credentials.from_service_account_file(
            self.key_file_path,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer'])

        self.http_client = AuthorizedSession(self.credentials)

    def create_class(self, issuer_id: str, class_suffix: str) -> str:
        """Create a class.

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for this pass class.

        Returns:
            The pass class ID: f"{issuer_id}.{class_suffix}"
        """

        # Check if the class exists
        response = self.http_client.get(
            url=f'{self.class_url}/{issuer_id}.{class_suffix}')

        if response.status_code == 200:
            print(f'Class {issuer_id}.{class_suffix} already exists!')
            return f'{issuer_id}.{class_suffix}'
        elif response.status_code != 404:
            # Something else went wrong...
            print(response.text)
            return f'{issuer_id}.{class_suffix}'

        # See link below for more information on required properties
        # https://developers.google.com/wallet/generic/rest/v1/genericclass
        new_class = {'id': f'{issuer_id}.{class_suffix}'}

        response = self.http_client.post(url=self.class_url, json=new_class)

        print(response.text)

        return response.json().get('id')

    def create_jwt_new_objects(self, issuer_id: str, class_suffix: str,
                               object_suffix: str, properties: dict,
                               modules: list[[str, str]]) -> str:
        """Generate a signed JWT that creates a new pass class and object.

        When the user opens the "Add to Google Wallet" URL and saves the pass to
        their wallet, the pass class and object defined in the JWT are
        created. This allows you to create multiple pass classes and objects in
        one API call when the user saves the pass to their wallet.

        Properties list:

        * logo: image_url
        * title: text
        * subheader: text
        * header: text
        * qr_code_content: text
        * show_qr_code_content: bool
        * hex_background_color: hex_code e.g.: "#ffffff"
        * image: image_url

        Args:
            issuer_id (str): The issuer ID being used for this request.
            class_suffix (str): Developer-defined unique ID for the pass class.
            object_suffix (str): Developer-defined unique ID for the pass object.
            properties (dict): Properties of the pass.
            modules (list): A list of list with two texts (NAME: content) to show inside the pass.

        Returns:
            An "Add to Google Wallet" link.
        """

        # See link below for more information on required properties
        # https://developers.google.com/wallet/generic/rest/v1/genericclass
        new_class = {'id': f'{issuer_id}.{class_suffix}'}

        # See link below for more information on required properties
        # https://developers.google.com/wallet/generic/rest/v1/genericobject
        new_object = {
            "id": f"{issuer_id}.{object_suffix}",
            "classId": f"{issuer_id}.{class_suffix}",
            "cardTitle": {
                "defaultValue": {
                    "language": "en-US",
                    "value": f"{properties['title']}"
                }
            },
            "header": {
                "defaultValue": {
                    "language": "en-US",
                    "value": f"{properties['header']}"
                }
            },
            "barcode": {
                "type": "QR_CODE",
                "value": f"{properties['qr_code_content']}",
                "alternateText": f"{properties['qr_code_content'] if properties['show_qr_code_content'] else ''}"
            },
            "hexBackgroundColor": f"{properties['hex_background_color']}",
        }

        if len(properties["logo"].strip()) > 0:
            new_object["logo"] = {
                "sourceUri": {
                    "uri": f"{properties['logo']}"
                },
                "contentDescription": {
                    "defaultValue": {
                        "language": "en-US",
                        "value": "LOGO_IMAGE_DESCRIPTION"
                    }
                }
            }

        if len(properties["subheader"].strip()) > 0:
            new_object["subheader"] = {
                "defaultValue": {
                    "language": "en-US",
                    "value": f"{properties['subheader']}"
                }
            }

        if len(properties["image"].strip()) > 0:
            new_object["heroImage"] = {
                "sourceUri": {
                    "uri": f"{properties['image']}"
                },
                "contentDescription": {
                    "defaultValue": {
                        "language": "en-US",
                        "value": "HERO_IMAGE_DESCRIPTION"
                    }
                }
            }

        if len(modules) > 0:
            new_object["textModulesData"] = [
                {
                    "id": f"{module[0].lower()}",
                    "header": f"{module[0].upper()}",
                    "body": f"{module[1]}"
                } for module in modules
            ]

        # Create the JWT claims
        claims = {
            'iss': self.credentials.service_account_email,
            'aud': 'google',
            'origins': ['https://custompasses.vercel.app/'], WARNING # This url should be changed to your website
            'typ': 'savetowallet',
            'payload': {
                # The listed classes and objects will be created
                'genericClasses': [new_class],
                'genericObjects': [new_object]
            }
        }

        # The service account credentials are used to sign the JWT
        signer = crypt.RSASigner.from_service_account_file(self.key_file_path)
        token = jwt.encode(signer, claims).decode('utf-8')

        return f'https://pay.google.com/gp/v/save/{token}'
