import pexpect


class Key(object):
    ENV_PATH = '/bin/bash'
    gen_req = "/usr/share/easy-rsa/easyrsa gen-req {name} nopass"
    sign_req = "/usr/share/easy-rsa/easyrsa sign-req client {name} nopass"
    phase = "{0}\r"

    def __init__(self, path, pass_phase):
        self.path = path
        self.pass_phase = pass_phase
        self.key_list = []

    def load_key_list(self):
        try:
            with open(self.path, 'rt') as keyList:
                list_content = keyList.read()
        except OSError as err:
            print('load_key_list()', err)
            exit(1)
        else:
            for item in list_content.splitlines():
                self.key_list.append(item)
        print(f'{len(self.key_list)} client CRT & KEY to generate....')

    def generate_key_and_crt(self, client_name):
        try:
            process_child = pexpect.spawn(self.ENV_PATH, ['-c', self.gen_req.format(name=client_name)], timeout=-1)

            process_child.expect("Common Name")
            process_child.send("\r")
            process_child = pexpect.spawn(self.ENV_PATH, ['-c', self.sign_req.format(name=client_name)], timeout=-1)
            process_child.expect("  Confirm request details:")
            process_child.send("yes\r")
            process_child.expect("Enter pass phrase for /usr/share/easy-rsa/pki/private/ca.key:")
            process_child.send(self.phase.format(self.pass_phase))
            process_child.expect(pexpect.EOF)
        except OSError as err:
            print('generate_key_and_crt()', err)
            exit(1)

    def build_crt_files(self):
        for crt in self.key_list:
            print(f'creating {crt} configuration file...')
            self.generate_key_and_crt(crt)

