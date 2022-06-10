from os import listdir, path, mkdir


class Configuration(object):
    fileTypePath = {
        'ca': '/usr/share/easy-rsa/pki/',
        'crt': '/usr/share/easy-rsa/pki/issued/',
        'key': '/usr/share/easy-rsa/pki/private/',
        'ini': '/usr/share/easy-rsa/pki/base_client_config.ini',
        'conf': '/usr/share/easy-rsa/pki/conf/',
        'reqs': '/usr/share/easy-rsa/pki/reqs/'
    }

    fileHeader = {
        'crt_begin': '-----BEGIN CERTIFICATE-----',
        'crt_end': '-----END CERTIFICATE-----',
        'key_begin': '-----BEGIN PRIVATE KEY-----',
        'key_end': '-----END PRIVATE KEY-----'
    }

    def __init__(self):
        self.list_crt_request = []

    def separate_crt(self, crt_name, file_path):
        result = ''
        try:
            with open(file_path + crt_name + '.crt', 'rt') as file:
                crt_content = file.read()
        except OSError as err:
            print('separate_crt()', err)
        else:
            copy = False
            for line in crt_content.splitlines():
                if line.strip() == self.fileHeader['crt_begin']:
                    copy = True
                elif line.strip() == self.fileHeader['crt_end']:
                    copy = False
                elif copy:
                    result = result + line + '\n'
        return result

    def separate_key(self, key_name, file_path):
        result = ''
        try:
            with open(file_path + key_name + '.key', 'rt') as file:
                key_content = file.read()
        except OSError as err:
            print('separate_key()', err)
        else:
            copy = False
            for line in key_content.splitlines():
                if line.strip() == self.fileHeader['key_begin']:
                    copy = True
                elif line.strip() == self.fileHeader['key_end']:
                    copy = False
                elif copy:
                    result = result + line + '\n'
        return result

    @staticmethod
    def read_base(file_path):
        try:
            with open(file_path, 'rt') as baseFile:
                result = baseFile.read()
        except OSError as err:
            print('read_base()', err)
            exit(1)
        else:
            return result

    def create_conf(self, client_name):
        try:
            with open(self.fileTypePath['conf'] + client_name + '.conf', 'w+') as conf_file:
                conf_file.write(self.read_base(self.fileTypePath['ini']))
                ca = self.separate_crt('ca', self.fileTypePath['ca'])
                conf_file.write('<ca>\n' + self.fileHeader['crt_begin'] + '\n' + ca + self.fileHeader['crt_end'] + '\n' + '</ca>\n')
                crt = self.separate_crt(client_name, self.fileTypePath['crt'])
                conf_file.write('<cert>\n' + self.fileHeader['crt_begin'] + '\n' + crt + self.fileHeader['crt_end'] + '\n' + '</cert>\n')
                key = self.separate_key(client_name, self.fileTypePath['key'])
                conf_file.write('<key>\n' + self.fileHeader['key_begin'] + '\n' + key + self.fileHeader['key_end'] + '\n' + '</key>\n')
        except OSError as err:
            print('create_conf()', err)

    def create_req_list(self):
        print(f'building file list from {self.fileTypePath["reqs"]} directory...')
        result = []
        try:
            reqList = listdir(self.fileTypePath['reqs'])
        except OSError as err:
            print('create_client_list()', err)
            exit(1)
        else:
            for item in reqList:
                result.append(path.splitext(item)[0])
        print(f'reqs list has {len(result)} elemnts....')
        self.list_crt_request = result

    def crete_output_dir(self):
        if path.isdir(self.fileTypePath['conf']):
            pass
        else:
            try:
                mkdir(self.fileTypePath['conf'])
            except OSError as err:
                print('crete_output_dir()', err)
                exit(1)
            else:
                print('conf directory has been created...')

    def build_conf_files(self):
        for conf in self.list_crt_request:
            print(f'creating {conf} configuration file...')
            self.create_conf(conf)
