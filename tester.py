import arbor

# This file is an example of how to use:

# Get Alert details by ID

alert_id = '68987'
alert = arbor.get_alert_by_id(alert_id)
if 'resource' in alert and 'cidr' in alert['resource']:
    ip = alert['resource']['cidr']
else:
    ip = '10.0.0.1'
print ip

# Get all ongoing alerts as a dictionary

ongoing_alerts = arbor.get_ongoig_alerts()

# Block mitigation - needs to send IP + Alert ID.

arbor.blackhole(ip, alert_id)  # Uncomment this to test automatic blackhole

# Stop blackhole by mitigation id

arbor.stop_blackhole(alert_id)
