#!/usr/bin/python

# This script generates the HCL configuration files for Terraform
# which can be used for vCloud Director NAT/Firewall rules.
# Check "python hcl_edge_gen.py --help" for more details.
#
# Created by: Emil Wypych (https://emilwypych.com)

import sys
import csv
import os
import getopt

class CSVInput():
    def __init__(self, filename):
        with open(filename, "r") as filedata:
            csvfile = csv.reader(filedata)
            self.data = list(csvfile)
            self.count = len(self.data)
    ## end of __init__

    def get_data(self, col, row):
        return self.data[row][col-1]
    ## end of get_data
## end of class CSVInput

def AddDNAT(data):
    """
    Remove any existing dnat.tf files and
    create a new one.
    """
    __terradnat = "dnat.tf"
    if os.path.exists(__terradnat):
        os.remove(__terradnat)
    instance = open(__terradnat,"a")
    for row in range(1,data.count):
        """
        Rows order in the CSV file:
        edge_name, exip, port, intip
        """
        instance.write("resource \"vcd_dnat\" \"rule" + str(row) + "\" {\n")
        instance.write("  edge_gateway     = \"" + data.get_data(1, row) + "\"\n")
        instance.write("  external_ip      = \"" + data.get_data(2, row) + "\"\n")
        instance.write("  port             = " + data.get_data(3, row) + "\n")
        instance.write("  internal_ip      = \"" + data.get_data(4, row) + "\"\n")
        instance.write("  translated_port  = " + data.get_data(5, row) + "\n\n")
    instance.close()
## end of AddDNAT

def AddSNAT(data):
    """
    Remove any existing snat.tf files and
    create a new one.
    """
    __terrasnat = "snat.tf"
    if os.path.exists(__terrasnat):
        os.remove(__terrasnat)
    instance = open(__terrasnat,"a")
    for row in range(1,data.count):
        """
        Rows order in the CSV file:
        edge_name, exip, intip
        """
        instance.write("resource \"vcd_snat\" \"rule" + str(row) + "\" {\n")
        instance.write("  edge_gateway = \"" + data.get_data(1, row) + "\"\n")
        instance.write("  external_ip  = \"" + data.get_data(2, row) + "\"\n")
        instance.write("  internal_ip  = \"" + data.get_data(3, row) + "\"\n\n")
    instance.close()
## end of AddSNAT

def AddFirewall(data):
    """
    Remove any existing firewall.tf files and
    create a new one.
    """
    __terrafw = "firewall.tf"
    if os.path.exists(__terrafw):
        os.remove(__terrafw)
    instance = open(__terrafw,"a")
    instance.write("resource \"vcd_firewall_rules\" \"fw\" {\n")
    instance.write("  edge_gateway = \"" + data.get_data(1, 1) + "\"\n")
    instance.write("  default_action = \"drop\"\n\n")
    for row in range(1,data.count):
        """
        Rows order in the CSV file:
        edge_name, descr, policy, protocol, dest_port, dest_ip, src_port, src_ip
        """
        instance.write("  rule {\n")
        instance.write("    description = \"" + data.get_data(2, row) + "\"\n")
        instance.write("    policy = \"" + data.get_data(3, row) + "\"\n")
        instance.write("    protocol = \"" + data.get_data(4, row) + "\"\n")
        instance.write("    destination_port = \"" + data.get_data(5, row) + "\"\n")
        instance.write("    destination_ip = \"" + data.get_data(6, row) + "\"\n")
        instance.write("    source_port = \"" + data.get_data(7, row) + "\"\n")
        instance.write("    source_ip = \"" + data.get_data(8, row) + "\"\n")
        instance.write("  }\n\n")
    instance.close()
## end of AddFirewall

def non_empty_file(filename):
    return os.path.exists(filename) and os.stat(filename).st_size > 0
## end of non_empty_file

def usage():
    print('\033[1m' + 'NAME' + '\033[0m')
    print('\t' + '\033[1m' +sys.argv[0]+ '\033[0m' + ' create Terraform HCL files for vCD Provider (NAT/Firewall)\n')
    print('\033[1m' + 'SYNOPSIS' + '\033[0m')
    print('\t' + '\033[1m' +sys.argv[0]+ '\033[0m' + ' [OPTIONS] ...\n')
    print('\033[1m' + 'DESCRIPTION' + '\033[0m')
    print('\t' + 'Generate Terraform configuration files for vCloud Director provider. ' \
    + 'It generates NAT and Firewall .tf files based on the CSV files.\n')
    print('\t' + '\033[1m' + '-d, --dnat=F'+ '\033[0m')
    print('\t\t' + 'specify the CSV file named F containing the DNAT table. If not specified, default is "datadnat.csv"\n')
    print('\t' + '\033[1m' + '-s, --snat=F'+ '\033[0m')
    print('\t\t' + 'specify the CSV file named F containing the SNAT table. If not specified, default is "datasnat.csv"\n')
    print('\t' + '\033[1m' + '-f, --firewall=F'+ '\033[0m')
    print('\t\t' + 'specify the CSV file named F containing the FIREWALL table. If not specified, default is "datafw.csv"\n')
    print('\t' + '\033[1m' + '-h'+ '\033[0m')
    print('\t\t' + 'print help\n')
    print('\033[1m' + 'AUTHOR' + '\033[0m')
    print('\t Written by Emil Wypych [https://emilwypych.com]\n')
## end of usage

def create(dnatfile,snatfile,fwfile):
    if non_empty_file(dnatfile):
        AddDNAT(CSVInput(dnatfile))

    if non_empty_file(snatfile):
        AddSNAT(CSVInput(snatfile))

    if non_empty_file(fwfile):
        AddFirewall(CSVInput(fwfile))
## end of create

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:s:f:", ["help", "dnat=", "snat=", "firewall="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))
        usage()
        sys.exit(2)
    dnat = None
    snat = None
    firewall = None
    for o, arg in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--dnat"):
            dnat = arg
        elif o in ("-s", "--snat"):
            dnat = arg
        elif o in ("-f", "--firewall"):
            dnat = arg
        else:
            assert False, "unhandled option"
    if not dnat:
        dnat = "datadnat.csv"
    if not snat:
        snat = "datasnat.csv"
    if not firewall:
        firewall = "datafw.csv"
    
    # run function which will create the HCL config files
    create(dnat,snat,firewall)
## end of main

if __name__ == "__main__":
    main()
