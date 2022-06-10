#!/usr/bin/python3

import sys, Key, Configuration


def main():
    # Build client .crt & .key files
    key = Key.Key(path='/usr/share/easyrsa/listToGenerate', pass_phase='password123')
    # key = Key.Key(path=argv[0], pass_phase=argv[1])
    key.load_key_list()
    # key.build_crt_files()

    # Generate .conf files for OpenVPN client
    conf = Configuration.Configuration()
    conf.crete_output_dir()
    conf.create_req_list()
    conf.build_conf_files()


if __name__ == '__main__':
    main()
