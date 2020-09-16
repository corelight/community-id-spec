#! /bin/env python3
"""
This produces a reference table for correct Community ID values, as seen at:
https://github.com/corelight/community-id-spec/blob/master/baseline/README.md
"""
import collections
import sys

try:
    import communityid
except ImportError:
    print('This needs the pycommunityid package:')
    print('pip install communityid')
    sys.exit(1)

try:
    import tabulate
except ImportError:
    print('This needs the tabulate package:')
    print('pip install tabulate')
    sys.exit(1)

Args = collections.namedtuple(
    'Args', ['pname', 'p', 'saddr', 'daddr', 'sport', 'dport', 'comment'],
    defaults=(None, None, None))

def v2s(val):
    """Turn possibly missing value into string"""
    return val if val is not None else '-'

def get_table(args, seed=0, use_base64=True):

    cid = communityid.CommunityID(seed=seed, use_base64=use_base64)
    detail = '(defaults)'

    if seed != 0 or not use_base64:
        word = 'w/' if use_base64 else 'w/o'
        detail = '(seed=%d, %s base64)' % (seed, word)

    headers = ['Proto name', 'Proto number', 'Src address', 'Dst address',
               'Src port', 'Dst port', 'Community ID %s' % detail, 'Comment']
    table = []

    for a in args:
        tpl = communityid.FlowTuple(a.p, a.saddr, a.daddr, a.sport, a.dport)
        table.append([a.pname, a.p, a.saddr, a.daddr, v2s(a.sport), v2s(a.dport),
                      cid.calc(tpl), a.comment])

    return headers, table

def main():

    sip4, dip4 = '1.2.3.4', '5.6.7.8'
    sip6 = 'fe80:0001:0203:0405:0607:0809:0A0B:0C0D'
    dip6 = 'fe80:1011:1213:1415:1617:1819:1A1B:1C1D'

    sport = 1122
    dport = 3344

    args = [
        Args('TCP', communityid.PROTO_TCP, sip4, dip4, sport, dport, 'Bidirectional flow, out ...'),
        Args('TCP', communityid.PROTO_TCP, dip4, sip4, dport, sport, '... and back'),
        Args('UDP', communityid.PROTO_UDP, sip4, dip4, sport, dport, 'Bidirectional flow, out ...'),
        Args('UDP', communityid.PROTO_UDP, dip4, sip4, dport, sport, '... and back'),
        Args('SCTP', communityid.PROTO_SCTP, sip4, dip4, sport, dport, 'Bidirectional flow, out ...'),
        Args('SCTP', communityid.PROTO_SCTP, dip4, sip4, dport, sport, '... and back'),
        Args('ICMP', communityid.PROTO_ICMP, sip4, dip4, 8, 0, 'ICMP flow treatment via types/codes: echo request ...'),
        Args('ICMP', communityid.PROTO_ICMP, dip4, sip4, 0, 0, '... and response'),
        Args('ICMP', communityid.PROTO_ICMP, sip4, dip4, 11, 0, 'Unidirectional ICMP treatment'),
        Args('ICMP6', communityid.PROTO_ICMP6, sip6, dip6, 128, 0, 'ICMP flow treatment via types/codes: echo request ...'),
        Args('ICMP6', communityid.PROTO_ICMP6, dip6, sip6, 129, 0, '... and response'),
        Args('ICMP6', communityid.PROTO_ICMP6, sip6, dip6, 146, 0, 'Unidirectional treatment'),
        Args('RSVP', 46, sip4, dip4, None, None, 'Example of port-less but bidirectional protocol, out ...'),
        Args('RSVP', 46, dip4, sip4, None, None, '... and back'),
        Args('RSVP', 46, sip6, dip6, None, None, 'Port-less example for IPv6, out ...'),
        Args('RSVP', 46, dip6, sip6, None, None, '... and back'),
    ]

    fmt = 'pretty'
    colalign = ('left', 'right', 'left', 'left', 'right', 'right', 'right', 'left')

    headers, table = get_table(args)
    print(tabulate.tabulate(table, headers=headers, tablefmt=fmt, colalign=colalign) + '\n\n')

    headers, table = get_table(args, seed=1)
    print(tabulate.tabulate(table, headers=headers, tablefmt=fmt, colalign=colalign) + '\n\n')

    headers, table = get_table(args, use_base64=False)
    print(tabulate.tabulate(table, headers=headers, tablefmt=fmt, colalign=colalign))

if __name__ == '__main__':
    sys.exit(main())
