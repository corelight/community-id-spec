Community ID Flow Hashing
=========================

When processing flow data from a variety of monitoring applications
(such as Zeek and Suricata), it's often desirable to pivot quickly
from one dataset to another. While the required flow tuple information
is usually present in the datasets, the details of such "joins" can
be tedious, particular in corner cases. This spec describes "Community
ID" flow hashing, standardizing the production of a string identifier
representing a given network flow, to reduce the pivot to a simple
string comparison.

Pseudo code
-----------

    function community_id_v1(ipaddr saddr, ipaddr daddr, port sport, port dport, int proto, int seed=0)
    {
        # Get seed and all tuple parts into network byte order
        seed = pack_to_nbo(seed); # 2 bytes
        saddr = pack_to_nbo(saddr); # 4 or 16 bytes
        daddr = pack_to_nbo(daddr); # 4 or 16 bytes
        sport = pack_to_nbo(sport); # 2 bytes
        dport = pack_to_nbo(dport); # 2 bytes

        # Abstract away directionality: flip the endpoints as needed
        # so the smaller IP:port tuple comes first.
        saddr, daddr, sport, dport = order_endpoints(saddr, daddr, sport, dport);

        # Produce 20-byte SHA1 digest. "." means concatenation. The
        # proto value is one byte in length and followed by a 0 byte
        # for padding.
        sha1_digest = sha1(seed . saddr . daddr . proto . 0 . sport . dport)

        # Prepend version string to base64 rendering of the digest.
        # v1 is currently the only one available.
        return "1:" + base64(sha1_digest)
    }
    
    function community_id_icmp(ipaddr saddr, ipaddr daddr, int type, int code, int seed=0)
    {
        port sport, dport;

        # ICMP / ICMPv6 endpoint mapping directly inspired by Zeek
        sport, dport = map_icmp_to_ports(type, code);

        # ICMP is IP protocol 1, ICMPv6 would be 58
        return community_id_v1(saddr, daddr, sport, dport, 1, seed); 
    }


Technical details
-----------------

- The Community ID is an additional flow identifier and doesn't need to
  replace existing flow identification mechanisms already supported by
  the monitors. It's okay, however, for a monitor to be configured to
  log only the Community ID, if desirable.

- The Community ID can be computed as a monitor produces flows, or can
  also be added to existing flow records at a later stage assuming
  that said records convey all the needed flow endpoint information.

- Collisions in the Community ID, while undesirable, are not
  considered fatal, since the user should still possess flow timing
  information and possibly the monitor's native ID mechanism (hopefully
  stronger than the Community ID) for disambiguation.

- The hashing mechanism uses seeding to enable additional control over
  "domains" of Community ID usage. The seed defaults to 0, so this
  mechanism gets out of the way so it doesn't affect operation for
  operators not interested in it.

- In version 1 of the ID, the hash algorithm is SHA1. Future hash
  versions may switch it or allow additional configuration.

- The binary 20-byte SHA1 result gets base64-encoded to reduce output
  volume compared to the usual ASCII-based SHA1 representation. This
  assumes that space, not computation time, is the primary concern,
  and may become configurable in a later version.

- The resulting flow ID includes a version number to make the
  underlying Community ID implementation explicit. This allows users
  to ensure they're comparing apples to apples while supporting future
  changes to the algorithm. For example, when one monitor's version of
  the ID incorporates VLAN IDs but another's does not, hash value
  comparisons should reliably fail. A more complex form of this
  feature could allow capturing configuration settings in addition to
  the implementation version.

  The versioning scheme currently simply prefixes the hash value with
  "<version>:", yielding something like this in the current version 1:

  `1:hO+sN4H+MG5MY/8hIrXPqc4ZQz0=`

- The hash input is aligned on 32-bit-boundaries. Flow tuple
  components use network byte order (big-endian) to standardize
  ordering regardless of host hardware.

- The hash input is ordered to remove directionality in the flow
  tuple: swap the endpoints, if needed, so the numerically smaller
  IP:port tuple comes first. If the IP addresses are equal, the ports
  decide.  For example, the following netflow 5-tuples create
  identical Community ID hashes because they both get ordered into
  the sequence 10.0.0.1, 127.0.0.1, 1234, 80.

  - Proto: TCP; SRC IP: 10.0.0.1; DST IP: 127.0.0.1; SRC Port: 1234; DST Port: 80
  - Proto: TCP; SRC IP: 127.0.0.1; DST IP: 10.0.0.1; SRC Port: 80; DST Port: 1234

- This version includes the following protocols and fields:

  - TCP / UDP / SCTP:

    IP src / IP dst / IP proto / source port / dest port 

  - ICMPv4 / ICMPv6:

    IP src / IP dst / IP proto / ICMP type + "counter-type" or code

    The exact handling of ICMP type & code is taken from Zeek; see
    implementations here:

    - https://github.com/corelight/pycommunityid/blob/master/communityid/icmp.py
    - https://github.com/corelight/pycommunityid/blob/master/communityid/icmp6.py
    - https://github.com/zeek/zeek/blob/master/src/analyzer/protocol/icmp/ICMP.cc#L860

  - Other IP-borne protocols:

    IP src / IP dst / IP proto

  The above does not currently cover how to handle nesting (IP in IP,
  v6 over v4, etc) as well as encapsulations such as VLAN and MPLS.

- If a network monitor doesn't support any of the above protocol
  constellations, it can safely report an empty string (or another
  non-colliding value) for the flow ID.

- Consider v1 a prototype. Feedback from the community, particularly
  implementers and operational users of the ID, is _greatly_
  appreciated. Please create issues directly in the GitHub project at
  https://github.com/corelight/community-id-spec, or contact Christian
  Kreibich (christian@corelight.com).

- Many thanks for helpful discussion and feedback to Victor Julien,
  Johanna Amann, and Robin Sommer, and to all implementors and
  supporters.

Reference implementation
------------------------

A complete implementation is available in the
[pycommunityid](https://github.com/corelight/pycommunityid) package.
It includes a range of tests to verify correct computation for the
various protocols. We recommend it to guide new implementations.

A smaller implementation is also available via the community-id.py
script in this repository, including the byte layout of the hashed
values (see packet_get_comm_id()). See --help and make.sh to get
started:

```
  $ ./community-id.py --help
  usage: community-id.py [-h] [--seed NUM] PCAP [PCAP ...]

  Community flow ID reference

  positional arguments:
    PCAP         PCAP packet capture files

  optional arguments:
    -h, --help   show this help message and exit
    --seed NUM   Seed value for hash operations
    --no-base64  Don't base64-encode the SHA1 binary value
    --verbose    Show verbose output on stderr
```

For troubleshooting, the implementation supports omitting the base64
operation, and can provide additional detail about the exact sequence
of bytes going into the SHA1 hash computation.

Reference data
--------------

The [`baseline`](baseline) directory in this repo contains datasets to
help you verify that your implementation of Community ID functions
correctly.

Reusable modules/libraries
--------------------------

- C: https://github.com/corelight/c-community-id
- Golang: https://github.com/satta/gommunityid
- Java: https://github.com/rapid7/community-id-java
- Python: https://github.com/corelight/pycommunityid

Sought-after implementations (please get in touch if you're considering writing one of these!):

- JavaScript

Production implementations
--------------------------

- Arkime (1.7.0+): https://github.com/arkime/arkime/issues/966
- Elastic Beats: e.g. https://www.elastic.co/guide/en/beats/packetbeat/master/community-id.html
- Elastic Common Schema: https://github.com/elastic/ecs/blob/master/schemas/network.yml
- HELK: https://github.com/Cyb3rWard0g/HELK (with [Ruby implementation](https://github.com/Cyb3rWard0g/HELK/commit/e81a98a745a4d02acc9d346865aeb312b3ee599d#diff-81497c6343ac648c68637062cf1ba082))
- MISP: https://www.misp-project.org/2019/07/19/MISP.2.4.111.released.html
- Osquery (4.2.0+): https://osquery.readthedocs.io/en/latest/introduction/sql/#sql-additions, [blog post](https://dactiv.llc/blog/correlate-osquery-network-connections/)
- Security Onion (2.0+): https://docs.securityonion.net/en/2.3/community-id.html
- Suricata (4.1+): https://suricata.readthedocs.io/en/suricata-4.1.2/output/eve/eve-json-output.html#community-flow-id
- VAST: https://github.com/vast-io/vast/pull/525
- Wireshark (3.3.1+): https://www.wireshark.org/news/20201001.html
- Zeek package (2.5+): https://github.com/corelight/zeek-community-id

Intent to support
-----------------

- https://www.d4-project.org

Feature requests in other projects
----------------------------------

- https://github.com/MicrosoftDocs/sysinternals/issues/219

Talks
-----

- [SuriCon 2018](http://icir.org/christian/talks/2018-11-suricon-communityid.pdf)
- [FOSDEM 2021](http://icir.org/christian/talks/2021-02-fosdem-communityid.pdf)

Discussion
----------

Feel free to discuss aspects of the Community ID via GitHub here:
https://github.com/corelight/community-id-spec/issues
