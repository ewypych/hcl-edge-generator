HCL files generator for vCloud Director [![Build Status](https://travis-ci.org/ewypych/hcl-edge-generator.png?branch=master)](https://travis-ci.org/ewypych/hcl-edge-generator)
======================================

This script generates the HCL files containing vCloud Director Provider configuration files. It comprises DNAT, SNAT and Firewall section. For proper work, script needs a valid CSV files with rules should be created. It can be useful during the Edge migration or deployment with the big amount of rules.

Example of use
--------------

```sh
chmod +x hcl_edge_gen.py
python hcl_edge_gen.py -d dnatfile.csv --snat=snatfile.csv
```
Requirements
------------

Script needs at least Python 2.7. It was not tested with the earlier version. You can check Travis CI output for more information about tested environments.

CSV files scheme
----------------------------

There are three different CSV files needed by the script:
* datadnat.csv with DNAT rules
* datasnat.csv with SNAT rules
* datafw.csv with Firewall rules

Files can have another names (you can specify them with the script arguments), but must have the following fieldnames and order:

**DNAT CSV**
Edge_Name, External_IP, Port, Internal_IP

*Please note that now there is no option to choose different source and destination port. If Terraform have this possibility, script will be adjusted to it.*

**SNAT CSV**
Edge_Name, External_IP, Internal_IP

**Firewall CSV**
Edge_Name, Description, Policy, Protocol, Destination_port, destination_IP, Source_port, Source_ip

More information
----------------------------

You can find more information in [this post](https://emilwypych.com/2017/07/02/vcloud-hcl-generator-terraform/).

License
-------

[MIT](https://tldrlegal.com/license/mit-license)

Author
------

[Emil Wypych](https://emilwypych.com) [@gmail](mailto:wypychemil@gmail.com)

