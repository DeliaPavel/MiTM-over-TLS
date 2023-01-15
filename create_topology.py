from mininet.net import Containernet
from mininet.node import Controller, OVSSwitch
from mininet.nodelib import NAT
from mininet.cli import CLI

def myNetwork():
    net = Containernet(controller=Controller)

    net.addController(name='c0')

    s1 = net.addSwitch('s1', cls=OVSSwitch)

    mn_args = {
        "network_mode": "none",
        "dimage": "mitm",
        "dcmd": "./start.sh",
        "ip": "10.0.0.2/24",
    }
    H1 = net.addDocker('attacker', **mn_args)
    mn_args = {
        "network_mode": "none",
        "dimage": "mitm",
        "dcmd": "./start.sh",
        "ip": "10.0.0.3/24",
    }
    H2 = net.addDocker('victim', **mn_args)

    net.addLink( H1, s1 )
    net.addLink( H2, s1 )

    mn_args = {
        "ip": "10.0.0.1/24",
    }
    nat = net.addHost( 'nat0', cls=NAT, inNamespace=False, subnet='10.0.0.0/24', **mn_args )

    net.addLink( nat, s1 )

    net.start()
    H1.cmd('ip r a default via 10.0.0.1')
    H2.cmd('ip r a default via 10.0.0.1')

    CLI(net)
    net.stop()

if _name_ == '_main_':
    myNetwork()