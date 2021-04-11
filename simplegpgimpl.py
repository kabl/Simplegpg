import questionary
import sys
import gnupg
import pyperclip
import os
STYLE_TXT = "fg:#FFD433"
STYLE_MENU = "bold underline fg:#FFD433"
STYLE_ERR = "fg:#f44336"


class SimpleGPG:

    def __init__(self, home_dir):

        if not os.path.isdir(home_dir):
            self.not_existing_directory(home_dir)

        self.gpg = gnupg.GPG(gnupghome=home_dir)
        self.gpg.encoding = 'utf-8'

    def not_existing_directory(self, home_dir):
        question = "Directory '" + home_dir + "' does not exists. Create a directory?"
        result = questionary.confirm(question).ask()
        if result:
            try:
                os.mkdir(home_dir)
                questionary.print("Directory created. No keypairs configured.", style=STYLE_TXT)
            except OSError:
                questionary.print("Could not create directory", style=STYLE_ERR)
                sys.exit(1)
        else:
            sys.exit(0)

    def main_menu(self):
        choices = {"Key Management": self.key_management,
                   "Encrypt": self.encrypt,
                   "Encrypt and Sign": self.encrypt_and_sign,
                   "Decrypt": self.decrypt,
                   "Sign": self.sign,
                   "Verify Signature": self.verify_signature,
                   "Exit": sys.exit}
        while True:
            questionary.print("")
            questionary.print("### SIMPLEGPG - MENU ###", style=STYLE_MENU)
            questionary.print("")
            selection = questionary.select("Select your task", choices=choices.keys(), use_shortcuts=True).ask()
            if selection is None:
                return

            choices[selection]()

    def key_management(self):
        choices = {"Create Keypair": self.create_keypair,
                   "Import Public Key": self.import_public_key,
                   "Export Key": self.export_key,
                   "List Keys": self.list_keys,
                   "Back": None}
        selection = questionary.select("Select your task", choices=choices.keys(), use_shortcuts=True).ask()

        if selection == "Back":
            return

        choices[selection]()

    def create_keypair(self):
        questionary.print("Creating a new ID/Key", style=STYLE_TXT)
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
            key_id = self.gpg.gen_key(input_data)
            key_id = str(key_id)
            questionary.print("Key generated: " + key_id, style=STYLE_TXT)
            print()
            self.print_key(key_id)

    def import_public_key(self):
        key = questionary.text("Enter public key to import:", multiline=True).ask()
        if key is None:
            return

        import_result = self.gpg.import_keys(key)
        if import_result.count == 0:
            questionary.print(import_result, style=STYLE_ERR)
            questionary.print(import_result.count, style=STYLE_ERR)
            questionary.print(import_result.fingerprints, style=STYLE_ERR)
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
        self.print_key(selected_key_id)

    def encrypt_and_sign(self):
        self.encrypt(sign=True)

    def encrypt(self, sign=False):

        signer_key = None
        if sign:
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
            data = str(encrypted_ascii_data)
            questionary.print(data, style=STYLE_TXT)
            self.add_to_clipboard(data)
        else:
            questionary.print("Encryption failed. " + encrypted_ascii_data.status + ", " + encrypted_ascii_data.stderr,
                              style=STYLE_ERR)

    def decrypt(self):
        message = questionary.text("Enter message to decrypt:", multiline=True).ask()
        if message is None:
            return

        decrypted = self.gpg.decrypt(message)
        if decrypted.ok:
            questionary.print(str(decrypted), style=STYLE_TXT)
        else:
            questionary.print("Decryption failed: " + decrypted.status, style=STYLE_ERR)

    def sign(self):

        signer_key = self.select_id()
        if signer_key is None:
            return

        message = questionary.text("Enter message to sign:", multiline=True).ask()
        if message is None:
            return

        # TODO: Check OK Value after Signing
        signature = self.gpg.sign(message, keyid=signer_key)
        signature_string = str(signature)
        questionary.print(signature_string, style=STYLE_TXT)
        self.add_to_clipboard(signature_string)

    def verify_signature(self):
        message = questionary.text("Enter message to verify:", multiline=True).ask()
        if message is None:
            return

        result = self.gpg.verify(message)
        if result:
            questionary.print("Valid data", style=STYLE_TXT)
        else:
            questionary.print("Message could not be verified!", style=STYLE_ERR)

    def select_id(self):
        choices = {}
        public_keys = self.gpg.list_keys(True)
        for pub_key in public_keys:
            for uid in pub_key['uids']:
                choices[uid] = pub_key['keyid']

        if not choices.keys():
            questionary.print("No keys configured. Create a keypair.", style=STYLE_ERR)
            return

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

        if not choices.keys():
            questionary.print("No Public Keys available. Import Public Key.", style=STYLE_ERR)
            return

        selection = questionary.select("Select Recipient", choices=choices.keys(), use_shortcuts=True).ask()
        if selection is None:
            return None

        selected_key_id = choices[selection][0:16]
        return selected_key_id

    def print_key(self, key_id):
        key = self.gpg.export_keys(key_id)
        questionary.print(key, style=STYLE_TXT)
        self.add_to_clipboard(key)

    def add_to_clipboard(self, text):
        pyperclip.copy(text)
        questionary.print("Message copied to the clipboard", style=STYLE_TXT)