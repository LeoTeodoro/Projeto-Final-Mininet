from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI

def custom_topology():
    net = Mininet(controller=Controller, switch=OVSSwitch, link=TCLink)

    # Adicionando controlador
    controller = net.addController('c0', controller=Controller)

    # Adicionando switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')
    s7 = net.addSwitch('s7')

    # Adicionando hosts
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')
    h7 = net.addHost('h7')

    # Criando links entre switches
    net.addLink(s1, s2)
    net.addLink(s2, s4)
    net.addLink(s3, s4)
    net.addLink(s4, s5)
    net.addLink(s5, s6)
    net.addLink(s3, s7)

    # Conectando switches aos hosts
    net.addLink(s2, h1)
    net.addLink(s6, h3)
    net.addLink(s5, h4)
    net.addLink(s4, h5)
    net.addLink(s3, h6)
    net.addLink(s7, h7)
    net.addLink(s6, h2)

    # Iniciando a topologia
    # a)
    net.build()
    controller.start()
    net.start()

    # Executar os comandos diretamente no Mininet
    execute_mininet_commands(net)

    # Finaliza a topologia após os testes
    net.stop()

def execute_mininet_commands(net):
    # Inspecionar informações das interfaces (endereços MAC e IP)
    # b)
    for host in net.hosts:
        host.cmd("ifconfig")

    # Testes de conectividade (ping)
    # d)
    net.pingAll()

    # Configurar regras de fluxo em switches
    # e)
    s4 = net.get('s4')
    mac_h1 = net.get('h1').MAC()
    mac_h4 = net.get('h4').MAC()
    s4.cmd(f"ovs-ofctl add-flow s4 priority=100,dl_src={mac_h1},dl_dst={mac_h4},actions=output:3")

    # Testar novamente com as regras implementadas
    # f)
    net.get('h1').cmd("ping -c 4 h4")

    # Remover as regras adicionadas
    s4.cmd("ovs-ofctl del-flows s4")

    # Testar conectividade após remoção das regras
    net.get('h1').cmd("ping -c 4 h4")

if __name__ == '__main__':
    custom_topology()
