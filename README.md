Community ID Flow Hashing
=========================

This spec describes a "community ID" flow hashing algorithm allowing
the consumers of output from multiple traffic monitors to link each
system's flow information.

Technical details
-----------------

- The community ID is an additional flow identifier and doesn't need to
  replace existing flow identification mechanisms already supported by
  the monitors. It's okay, however, for a monitor to be configured to
  log only the community ID, if desirable.

- Collisions in the community ID, while undesirable, are not
  considered fatal, since the user should still possess the monitor's
  native ID mechanism (hopefully stronger than the community ID)
  output available for disambiguation.

- The hashing mechanism uses seeding to enable additional control;
  this mechanism gets out of the way so it doesn't affect operation
  for operators not interested in it.

- The hash algorithm is SHA1. Future hash versions may switch it or
  allow additional configuration. The overall hashed flow tuple data
  align on 32-bit boundary.

- The SHA1 result gets base64-encoded to reduce output volume compared
  to the usual ASCII-based SHA1 representation.

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


Reference implementation
------------------------

The community-id.py Python script implements the above, including the
byte layout of the hashed values (see packet_get_comm_id()). See
--help and make.sh to get started:

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
