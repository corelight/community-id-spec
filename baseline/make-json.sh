#! /bin/env bash

pcap=../pcaps/combined.pcap.gz

community-id-pcap --json $pcap >baseline_deflt.json
community-id-pcap --json --seed 1 $pcap >baseline_seed1.json
community-id-pcap --json --no-base64 $pcap >baseline_nob64.json
