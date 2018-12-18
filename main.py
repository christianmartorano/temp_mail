BANNER = '''
#    dBBBBBBP dBBBP  dBBBBBBb dBBBBBb     dBBBBBBb dBBBBBb     dBP dBP
#                     '   dB'     dB'      '   dB'      BB
#     dBP   dBBP   dB'dB'dB'  dBBBP'    dB'dB'dB'   dBP BB   dBP dBP
#    dBP   dBP    dB'dB'dB'  dBP       dB'dB'dB'   dBP  BB  dBP dBP
#   dBP   dBBBBP dB'dB'dB'  dBP       dB'dB'dB'   dBBBBBBB dBP dBBBBP
#                                                                     '''

import argparse

from controller import mail_controller

import os

def main():
    parser = argparse.ArgumentParser(prog="Email Temporário")
    parser.add_argument("--seg", help="Qtd. segundos para refresh.", default=15, type=int)

    args = parser.parse_args()

    print(BANNER)

    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    mail_controller.mail_capture(args)

main()
