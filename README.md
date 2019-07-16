Community ID Flow Hashing
=========================

This spec describes a "community ID" flow hashing algorithm allowing
the consumers of output from multiple traffic monitors to link each
system's flow records more easily.

Technical details
-----------------

- The community ID is an additional flow identifier and doesn't need to
  replace existing flow identification mechanisms already supported by
  the monitors. It's okay, however, for a monitor to be configured to
  log only the community ID, if desirable.

- The community ID can be computed as a monitor produces flows, or can
  also be added to existing flow records at a later stage assuming
  that said records convey all the needed flow endpoint information.

- Collisions in the community ID, while undesirable, are not
  considered fatal, since the user should still possess the monitor's
  native ID mechanism (hopefully stronger than the community ID)
  for disambiguation.

- The hashing mechanism uses seeding to enable additional control;
  this mechanism gets out of the way so it doesn't affect operation
  for operators not interested in it.

- The hash algorithm is SHA1. Future hash versions may switch it or
  allow additional configuration.

- The binary 20-byte SHA1 result gets base64-encoded to reduce output
  volume compared to the usual ASCII-based SHA1 representation. This
  assumes that space, not computation time, is the primary concern,
  and may become configurable in a later version.

- The resulting flow ID includes a version number to make the
  underlying community ID implementation explicit. This allows users
  to ensure they're comparing apples to apples while supporting future
  changes to the algorithm. For example, when one monitor's version of
  the ID incorporates VLAN IDs but another's does not, hash value
  comparisons should reliably fail. A more complex form of this
  feature could allow capturing configuration settings in addition to
  the implementation version.

  The versioning scheme currently simply prefixes the hash value with
  "<version>:", yielding something like this in the current version 1:

  1:hO+sN4H+MG5MY/8hIrXPqc4ZQz0=

- The hash input is aligned on 32-bit-boundaries. Flow tuple
  components use network byte order (big-endian) to standardize
  ordering regardless of host hardware.

- This version includes the following protocols and fields:

  - TCP / UDP / SCTP:

    IP src / IP dst / IP proto / source port / dest port 

  - ICMPv4 / ICMPv6:

    IP src / IP dst / IP proto / ICMP type + "counter-type" or code

  - Other IP-borne protocols:

    IP src / IP dst / IP proto

  The above does not currently cover how to handle nesting (IP in IP,
  v6 over v4, etc) as well as encapsulations such as VLAN and MPLS.

- If a network monitor doesn't support any of the above protocol
  constellations, it can safely report an empty string (or another
  non-colliding value) for the flow ID. Absence of a flow ID value
  simply means that flow correlation with other tools that support
  such constellations.

- All of the above is preliminary and feedback from the community,
  particularly implementers, is greatly appreciated. Please contact
  Christian Kreibich (christian@corelight.com).

- Many thanks for helpful discussion and feedback to Victor Julien,
  Johanna Amann, and Robin Sommer.

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

Production implementations
--------------------------

- Elastic Beats: e.g. https://www.elastic.co/guide/en/beats/packetbeat/master/community-id.html
- Elastic Common Schema: https://github.com/elastic/ecs/blob/master/schemas/network.yml
- HELK: https://github.com/Cyb3rWard0g/HELK (with [Ruby implementation](https://github.com/Cyb3rWard0g/HELK/commit/e81a98a745a4d02acc9d346865aeb312b3ee599d#diff-81497c6343ac648c68637062cf1ba082))
- MISP: https://www.misp-project.org/objects.html#_netflow
- Moloch (1.7.0+): https://github.com/aol/moloch/issues/966
- Suricata (4.1+): https://suricata.readthedocs.io/en/suricata-4.1.2/output/eve/eve-json-output.html#community-flow-id
- Zeek package (2.5+): https://github.com/corelight/bro-community-id

Intent to support
-----------------

- https://www.d4-project.org

Feature requests in other projects
----------------------------------

- https://github.com/MicrosoftDocs/sysinternals/issues/219

Talks
-----

- SuriCon 2018: http://icir.org/christian/talks/2018-11-suricon-communityid.pdf

Discussion
----------

Feel free to discuss aspects of the Community ID via GitHub here:
https://github.com/corelight/community-id-spec/issues
