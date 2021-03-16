import questionary
import sys
import gnupg

STYLE_TXT = "fg:#FFD433"
STYLE_MENU = "bold underline fg:#FFD433"
STYLE_ERR = "fg:#f44336"


class SimpleGPG:

    def __init__(self, home_dir):
        self.gpg = gnupg.GPG(gnupghome=home_dir)
        # self.gpg = gnupg.GPG(gnupghome="./id1")

        self.gpg.encoding = 'utf-8'

    def main_menu(self):
        choices = {"Key Management": self.key_management,
                   "Encrypt and Sign": self.encrypt,
                   "Decrypt": self.decrypt,
                   "Exit": sys.exit}
        while True:
            questionary.print("")
            questionary.print("### SIMPLEGPG - MENU ###", style=STYLE_MENU)
            questionary.print("")
            selection = questionary.select("Select your task", choices=choices.keys(), use_shortcuts=True).ask()
            choices[selection]()

    def key_management(self):
        choices = {"Create Keypair": self.create_keypair,
                   "Import Public Key": self.import_public_key,
                   "Export Key": self.export_key,
                   "List Keys": self.list_keys,
                   "Back": None}
        selection = questionary.select("Select your task", choices=choices.keys(), use_shortcuts=True).ask()

        if selection is "Back":
            return

        choices[selection]()

    def create_keypair(self):
        print("Creating a new ID/Key")
        name = questionary.text("What's your fullname?").ask()
        email = questionary.text("What's your e-mail address?").ask()
        length_options = ["1024", "2048", "4096"]
        key_length = questionary.select("Key Length", choices=length_options, use_shortcuts=True).ask()

        input_data = self.gpg.gen_key_input(key_type="RSA",
                                            key_length=int(key_length),
                                            name_real=name,
                                            name_email=email)
        proceed = questionary.confirm("Generate?").ask()
        if proceed:
            key = self.gpg.gen_key(input_data)
            questionary.print("Key generated: " + key, style=STYLE_TXT)

    def import_public_key(self):
        key = questionary.text("Enter public key to import:", multiline=True).ask()
        import_result = self.gpg.import_keys(key)
        if import_result.count == 0:
            print(import_result)
            print(import_result.count)
            print(import_result.fingerprints)
            questionary.print("Import Failed", style=STYLE_ERR)
        else:
            questionary.print("Import Succeed", style=STYLE_TXT)

    def list_keys(self):
        public_keys = self.gpg.list_keys(False)

        is_empty = True
        for pub_key in public_keys:
            for uid in pub_key['uids']:
                questionary.print(pub_key['keyid'] + "\t" + uid, style=STYLE_TXT)
                is_empty = False

        if is_empty:
            questionary.print("No keys configured", style=STYLE_TXT)

    def export_key(self):
        choices = {}
        public_keys = self.gpg.list_keys(False)
        for pub_key in public_keys:
            for uid in pub_key['uids']:
                choices[uid] = pub_key['keyid']

        choices["Back"] = None

        selection = questionary.select("Select Public Key to export", choices=choices.keys(), use_shortcuts=True).ask()

        if selection == "Back":
            return

        selected_key_id = choices[selection][0:16]
        key = self.gpg.export_keys(selected_key_id)
        questionary.print(key, style=STYLE_TXT)

    def encrypt(self):
        signer_key = self.select_id()

        if signer_key is None:
            return

        recipient = self.select_recipient()

        if recipient is None:
            return

        message = questionary.text("Enter message to encrypt:", multiline=True).ask()

        if message is None:
            return

        encrypted_ascii_data = self.gpg.encrypt(message, recipient, sign=signer_key, always_trust=True)
        if encrypted_ascii_data.ok:
            questionary.print(str(encrypted_ascii_data), style=STYLE_TXT)
        else:
            questionary.print("Encryption failed. " + encrypted_ascii_data.status + ", " + encrypted_ascii_data.stderr,
                              style=STYLE_ERR)

    def decrypt(self):
        message = questionary.text("Enter message to decrypt:", multiline=True).ask()

        if message is None:
            return

        decrypted = self.gpg.decrypt(message)
        if decrypted.ok:
            questionary.print(decrypted, style=STYLE_TXT)
        else:
            questionary.print("Decryption failed: " + decrypted.status, style=STYLE_ERR)

    def select_id(self):
        choices = {}
        public_keys = self.gpg.list_keys(True)
        for pub_key in public_keys:
            for uid in pub_key['uids']:
                choices[uid] = pub_key['keyid']

        selection = questionary.select("Which ID do you want to use?", choices=choices.keys(), use_shortcuts=True).ask()

        if selection is None:
            return None

        selected_key_id = choices[selection][0:16]
        return selected_key_id

    def select_recipient(self):
        choices = {}
        public_keys = self.gpg.list_keys(False)
        for pub_key in public_keys:
            for uid in pub_key['uids']:
                choices[uid] = pub_key['keyid']

        selection = questionary.select("Select Recipient", choices=choices.keys(), use_shortcuts=True).ask()

        if selection is None:
            return None

        selected_key_id = choices[selection][0:16]
        return selected_key_id

