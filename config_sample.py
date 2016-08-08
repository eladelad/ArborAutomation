# Change this file to config.py and edit settings

ArborSettings = dict(
    ip='192.168.0.1',
    api_key='a23abcDeFgHIGklM',
    user='admin',
    password='admin'
)

ArborBlackholeParams = dict(
    offramp_id='',
    router_gids='206:1',
    __start_panel='',
    blob_gid='',
    ip_version='4',
    nexthop_type='offramp',
    customized_nexthop='',
    filter1_textarea='Router-Name: RR (1.2.3.4)',  # Define this as you do in the add mitigation text area
    bgp_communities='65555:330',  # Change to your blackhole community
    duration='120',  # Time for the blackhole in minutes
    save='Save'
)

