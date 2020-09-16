# Community ID Baseline Data

If you're working on a Community ID implementation, you can use the
data in this folder to verify the correctness of your
implementation. We provide two sets of data: tables for cherry-picking
specific tuples, and JSON files for programmatic verification.

## Sample results

The following three tables show correct Community ID results for basic
configurations. Regular tables render poorly on GitHub so the
following embeds them as code. You may want to refer to the source of
this README directly or look at the make-tables.py script in this
folder, which generates them.

### Default settings

    +------------+--------------+-----------------------------------------+-----------------------------------------+----------+----------+--------------------------------+----------------------------------------------------------+
    | Proto name | Proto number | Src address                             | Dst address                             | Src port | Dst port |        Community ID (defaults) | Comment                                                  |
    +------------+--------------+-----------------------------------------+-----------------------------------------+----------+----------+--------------------------------+----------------------------------------------------------+
    | TCP        |            6 | 1.2.3.4                                 | 5.6.7.8                                 |     1122 |     3344 | 1:wCb3OG7yAFWelaUydu0D+125CLM= | Bidirectional flow, out ...                              |
    | TCP        |            6 | 5.6.7.8                                 | 1.2.3.4                                 |     3344 |     1122 | 1:wCb3OG7yAFWelaUydu0D+125CLM= | ... and back                                             |
    | UDP        |           17 | 1.2.3.4                                 | 5.6.7.8                                 |     1122 |     3344 | 1:0Mu9InQx6z4ZiCZM/7HXi2WMhOg= | Bidirectional flow, out ...                              |
    | UDP        |           17 | 5.6.7.8                                 | 1.2.3.4                                 |     3344 |     1122 | 1:0Mu9InQx6z4ZiCZM/7HXi2WMhOg= | ... and back                                             |
    | SCTP       |          132 | 1.2.3.4                                 | 5.6.7.8                                 |     1122 |     3344 | 1:EKt4MsxuyaE6mL+hmrEkQ9csDD8= | Bidirectional flow, out ...                              |
    | SCTP       |          132 | 5.6.7.8                                 | 1.2.3.4                                 |     3344 |     1122 | 1:EKt4MsxuyaE6mL+hmrEkQ9csDD8= | ... and back                                             |
    | ICMP       |            1 | 1.2.3.4                                 | 5.6.7.8                                 |        8 |        0 | 1:crodRHL2FEsHjbv3UkRrfbs4bZ0= | ICMP flow treatment via types/codes: echo request ...    |
    | ICMP       |            1 | 5.6.7.8                                 | 1.2.3.4                                 |        0 |        0 | 1:crodRHL2FEsHjbv3UkRrfbs4bZ0= | ... and response                                         |
    | ICMP       |            1 | 1.2.3.4                                 | 5.6.7.8                                 |       11 |        0 | 1:f/YiSyWqczrTgfUCZlBUnvHRcPk= | Unidirectional ICMP treatment                            |
    | ICMP6      |           58 | fe80:0001:0203:0405:0607:0809:0A0B:0C0D | fe80:1011:1213:1415:1617:1819:1A1B:1C1D |      128 |        0 | 1:0bf7hyMJUwt3fMED7z8LIfRpBeo= | ICMP flow treatment via types/codes: echo request ...    |
    | ICMP6      |           58 | fe80:1011:1213:1415:1617:1819:1A1B:1C1D | fe80:0001:0203:0405:0607:0809:0A0B:0C0D |      129 |        0 | 1:0bf7hyMJUwt3fMED7z8LIfRpBeo= | ... and response                                         |
    | ICMP6      |           58 | fe80:0001:0203:0405:0607:0809:0A0B:0C0D | fe80:1011:1213:1415:1617:1819:1A1B:1C1D |      146 |        0 | 1:fYC8+pz24E+EhANP1EZhpX0Dw10= | Unidirectional treatment                                 |
    | RSVP       |           46 | 1.2.3.4                                 | 5.6.7.8                                 |        - |        - | 1:ikv3kmf89luf73WPz1jOs49S768= | Example of port-less but bidirectional protocol, out ... |
    | RSVP       |           46 | 5.6.7.8                                 | 1.2.3.4                                 |        - |        - | 1:ikv3kmf89luf73WPz1jOs49S768= | ... and back                                             |
    | RSVP       |           46 | fe80:0001:0203:0405:0607:0809:0A0B:0C0D | fe80:1011:1213:1415:1617:1819:1A1B:1C1D |        - |        - | 1:wQ/2mwrnXP4lmJcHdGL5ePjR+e0= | Port-less example for IPv6, out ...                      |
    | RSVP       |           46 | fe80:1011:1213:1415:1617:1819:1A1B:1C1D | fe80:0001:0203:0405:0607:0809:0A0B:0C0D |        - |        - | 1:wQ/2mwrnXP4lmJcHdGL5ePjR+e0= | ... and back                                             |
    +------------+--------------+-----------------------------------------+-----------------------------------------+----------+----------+--------------------------------+----------------------------------------------------------+

### A custom seed=1 value

    +------------+--------------+-----------------------------------------+-----------------------------------------+----------+----------+----------------------------------+----------------------------------------------------------+
    | Proto name | Proto number | Src address                             | Dst address                             | Src port | Dst port | Community ID (seed=1, w/ base64) | Comment                                                  |
    +------------+--------------+-----------------------------------------+-----------------------------------------+----------+----------+----------------------------------+----------------------------------------------------------+
    | TCP        |            6 | 1.2.3.4                                 | 5.6.7.8                                 |     1122 |     3344 |   1:HhA1B+6CoLbiKPEs5nhNYN4XWfk= | Bidirectional flow, out ...                              |
    | TCP        |            6 | 5.6.7.8                                 | 1.2.3.4                                 |     3344 |     1122 |   1:HhA1B+6CoLbiKPEs5nhNYN4XWfk= | ... and back                                             |
    | UDP        |           17 | 1.2.3.4                                 | 5.6.7.8                                 |     1122 |     3344 |   1:OShq+iKDAMVouh/4bMxB9Sz4amw= | Bidirectional flow, out ...                              |
    | UDP        |           17 | 5.6.7.8                                 | 1.2.3.4                                 |     3344 |     1122 |   1:OShq+iKDAMVouh/4bMxB9Sz4amw= | ... and back                                             |
    | SCTP       |          132 | 1.2.3.4                                 | 5.6.7.8                                 |     1122 |     3344 |   1:uitchpn5MMGAQKBJh7bIr/bAr7s= | Bidirectional flow, out ...                              |
    | SCTP       |          132 | 5.6.7.8                                 | 1.2.3.4                                 |     3344 |     1122 |   1:uitchpn5MMGAQKBJh7bIr/bAr7s= | ... and back                                             |
    | ICMP       |            1 | 1.2.3.4                                 | 5.6.7.8                                 |        8 |        0 |   1:9pr4ZGTICiuZoIh90RRYE2RyXpU= | ICMP flow treatment via types/codes: echo request ...    |
    | ICMP       |            1 | 5.6.7.8                                 | 1.2.3.4                                 |        0 |        0 |   1:9pr4ZGTICiuZoIh90RRYE2RyXpU= | ... and response                                         |
    | ICMP       |            1 | 1.2.3.4                                 | 5.6.7.8                                 |       11 |        0 |   1:1DD7cWGC/Yg91YGsQeni8du3pIA= | Unidirectional ICMP treatment                            |
    | ICMP6      |           58 | fe80:0001:0203:0405:0607:0809:0A0B:0C0D | fe80:1011:1213:1415:1617:1819:1A1B:1C1D |      128 |        0 |   1:IO27GQzPuCtNnwFvjWALMHu5tJE= | ICMP flow treatment via types/codes: echo request ...    |
    | ICMP6      |           58 | fe80:1011:1213:1415:1617:1819:1A1B:1C1D | fe80:0001:0203:0405:0607:0809:0A0B:0C0D |      129 |        0 |   1:IO27GQzPuCtNnwFvjWALMHu5tJE= | ... and response                                         |
    | ICMP6      |           58 | fe80:0001:0203:0405:0607:0809:0A0B:0C0D | fe80:1011:1213:1415:1617:1819:1A1B:1C1D |      146 |        0 |   1:Cv4IKJe56BNkF0MBW2YxQ3Nwc3s= | Unidirectional treatment                                 |
    | RSVP       |           46 | 1.2.3.4                                 | 5.6.7.8                                 |        - |        - |   1:/buhqeOmaRCopOZFy9HnoJd5XW8= | Example of port-less but bidirectional protocol, out ... |
    | RSVP       |           46 | 5.6.7.8                                 | 1.2.3.4                                 |        - |        - |   1:/buhqeOmaRCopOZFy9HnoJd5XW8= | ... and back                                             |
    | RSVP       |           46 | fe80:0001:0203:0405:0607:0809:0A0B:0C0D | fe80:1011:1213:1415:1617:1819:1A1B:1C1D |        - |        - |   1:j6EyyfBzL4vWKHFXgUqb5Az3OxM= | Port-less example for IPv6, out ...                      |
    | RSVP       |           46 | fe80:1011:1213:1415:1617:1819:1A1B:1C1D | fe80:0001:0203:0405:0607:0809:0A0B:0C0D |        - |        - |   1:j6EyyfBzL4vWKHFXgUqb5Az3OxM= | ... and back                                             |
    +------------+--------------+-----------------------------------------+-----------------------------------------+----------+----------+----------------------------------+----------------------------------------------------------+

### No base64-encoding

    +------------+--------------+-----------------------------------------+-----------------------------------------+----------+----------+--------------------------------------------+----------------------------------------------------------+
    | Proto name | Proto number | Src address                             | Dst address                             | Src port | Dst port |          Community ID (seed=0, w/o base64) | Comment                                                  |
    +------------+--------------+-----------------------------------------+-----------------------------------------+----------+----------+--------------------------------------------+----------------------------------------------------------+
    | TCP        |            6 | 1.2.3.4                                 | 5.6.7.8                                 |     1122 |     3344 | 1:c026f7386ef200559e95a53276ed03fb5db908b3 | Bidirectional flow, out ...                              |
    | TCP        |            6 | 5.6.7.8                                 | 1.2.3.4                                 |     3344 |     1122 | 1:c026f7386ef200559e95a53276ed03fb5db908b3 | ... and back                                             |
    | UDP        |           17 | 1.2.3.4                                 | 5.6.7.8                                 |     1122 |     3344 | 1:d0cbbd227431eb3e1988264cffb1d78b658c84e8 | Bidirectional flow, out ...                              |
    | UDP        |           17 | 5.6.7.8                                 | 1.2.3.4                                 |     3344 |     1122 | 1:d0cbbd227431eb3e1988264cffb1d78b658c84e8 | ... and back                                             |
    | SCTP       |          132 | 1.2.3.4                                 | 5.6.7.8                                 |     1122 |     3344 | 1:10ab7832cc6ec9a13a98bfa19ab12443d72c0c3f | Bidirectional flow, out ...                              |
    | SCTP       |          132 | 5.6.7.8                                 | 1.2.3.4                                 |     3344 |     1122 | 1:10ab7832cc6ec9a13a98bfa19ab12443d72c0c3f | ... and back                                             |
    | ICMP       |            1 | 1.2.3.4                                 | 5.6.7.8                                 |        8 |        0 | 1:72ba1d4472f6144b078dbbf752446b7dbb386d9d | ICMP flow treatment via types/codes: echo request ...    |
    | ICMP       |            1 | 5.6.7.8                                 | 1.2.3.4                                 |        0 |        0 | 1:72ba1d4472f6144b078dbbf752446b7dbb386d9d | ... and response                                         |
    | ICMP       |            1 | 1.2.3.4                                 | 5.6.7.8                                 |       11 |        0 | 1:7ff6224b25aa733ad381f5026650549ef1d170f9 | Unidirectional ICMP treatment                            |
    | ICMP6      |           58 | fe80:0001:0203:0405:0607:0809:0A0B:0C0D | fe80:1011:1213:1415:1617:1819:1A1B:1C1D |      128 |        0 | 1:d1b7fb872309530b777cc103ef3f0b21f46905ea | ICMP flow treatment via types/codes: echo request ...    |
    | ICMP6      |           58 | fe80:1011:1213:1415:1617:1819:1A1B:1C1D | fe80:0001:0203:0405:0607:0809:0A0B:0C0D |      129 |        0 | 1:d1b7fb872309530b777cc103ef3f0b21f46905ea | ... and response                                         |
    | ICMP6      |           58 | fe80:0001:0203:0405:0607:0809:0A0B:0C0D | fe80:1011:1213:1415:1617:1819:1A1B:1C1D |      146 |        0 | 1:7d80bcfa9cf6e04f8484034fd44661a57d03c35d | Unidirectional treatment                                 |
    | RSVP       |           46 | 1.2.3.4                                 | 5.6.7.8                                 |        - |        - | 1:8a4bf79267fcf65b9fef758fcf58ceb38f52efaf | Example of port-less but bidirectional protocol, out ... |
    | RSVP       |           46 | 5.6.7.8                                 | 1.2.3.4                                 |        - |        - | 1:8a4bf79267fcf65b9fef758fcf58ceb38f52efaf | ... and back                                             |
    | RSVP       |           46 | fe80:0001:0203:0405:0607:0809:0A0B:0C0D | fe80:1011:1213:1415:1617:1819:1A1B:1C1D |        - |        - | 1:c10ff69b0ae75cfe259897077462f978f8d1f9ed | Port-less example for IPv6, out ...                      |
    | RSVP       |           46 | fe80:1011:1213:1415:1617:1819:1A1B:1C1D | fe80:0001:0203:0405:0607:0809:0A0B:0C0D |        - |        - | 1:c10ff69b0ae75cfe259897077462f978f8d1f9ed | ... and back                                             |
    +------------+--------------+-----------------------------------------+-----------------------------------------+----------+----------+--------------------------------------------+----------------------------------------------------------+

## JSON data

The `baseline_*.json` files in this folder contain JSON data that
summarize flow tuples and corresponding Community ID values. They're
produced by running the [`community-id-pcap`](https://github.com/corelight/pycommunityid/blob/master/scripts/community-id-pcap)
tool from the pycommunityid package on the [`pcaps/combined.pcap.gz`](../pcaps/combined.pcap.gz)
file in this repo, with the same configurations as for the above
tables. [`make-json.sh`](make-json.sh) generates them.
