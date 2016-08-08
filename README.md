# ArborAutomation
This library is for Arbor Networks TMS automation

Tested on python 2.7.10 
See tester.py for an examples how to use
To start copy or move config_sample.py to config.py and change the parameters.

This has few functionalities:
1. Use the arbor API to retrieve alerts (by id, last alerts, ongoing)
2. Start or stop blackhole by mitigation ID
3. Add or start blackhole by alert ID and IP

This is my pip freeze (most of them are for Scrapy, you can just pip install requests && pip install Scrapy)

attrs==16.0.0
cffi==1.7.0
cryptography==1.4
cssselect==0.9.2
enum34==1.1.6
idna==2.1
ipaddress==1.0.16
lxml==3.6.1
parsel==1.0.3
pyasn1==0.1.9
pyasn1-modules==0.0.8
pycparser==2.14
PyDispatcher==2.0.5
pyOpenSSL==16.0.0
queuelib==1.4.2
requests==2.10.0
Scrapy==1.1.1
service-identity==16.0.0
six==1.10.0
Twisted==16.3.0
w3lib==1.15.0
wheel==0.24.0
zope.interface==4.2.0

