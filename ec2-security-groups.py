#!/usr/bin/env python
# encoding: utf-8
"""
ec2-security-report.py

Created by Jeremiah Shirk on 2012-01-24.
"""

import sys
import getopt

import boto.ec2 as ec2
from boto.ec2.connection import EC2Connection

help_message = '''
ec2-security-report

Report on EC2 security groups.

Options:

    -h  This help message
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def print_report():
    '''Print report to stdout for all security groups'''
    # TODO hardcoded sane defaults for now, need to parameterize these
    us_east_1 = ec2.get_region('us-east-1')
    conn = us_east_1.connect()
    groups = conn.get_all_security_groups()
    # for group in sorted(groups, key=lambda g: g.name):
    for group in groups:
        group_name = group.name
        for ipp in group.rules:
            if ipp.from_port == ipp.to_port:
                ports = ipp.from_port
            else:
                ports = "%s-%s" % (ipp.from_port, ipp.to_port)
            ports_text =  "%s/%s" % (ports, ipp.ip_protocol)
            grants_list = list()
            for grant in ipp.grants:
                if grant.name is not None:
                    grant_text = "%s" % (grant.name)
                else:
                    grant_text = "%s" % (grant.cidr_ip)
                grants_list.append(grant_text)
            print "%s allows %s from %s" % (
                group_name, ports_text, ','.join(grants_list))
            
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hv", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
                
        print_report()
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
