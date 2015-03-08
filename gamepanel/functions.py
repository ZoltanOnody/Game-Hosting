from gamepanel.models import Server
from gameserver_project.settings import FIRST_PORT
from gameserver_project.settings import MAX_PORTS
from gameserver_project.settings import SERVER_IP

from valve.source.a2s import ServerQuerier

import socket
from os import system


def get_my_ip():
    return socket.gethostbyname(socket.gethostname())


def get_first_unused_port():
    used_ports_object = Server.objects.all()

    used_ports = []
    for server in used_ports_object:
        used_ports.append(server.port)

    boolean_list = [False]*MAX_PORTS
    for port in used_ports:
        boolean_list[port-FIRST_PORT] = True

    for i in range(MAX_PORTS):
        if boolean_list[i] is False:
            return i + FIRST_PORT

    return -1


def change_server_info_to_valve(properties):
    items = dict()

    items['server_name'] = properties['sv_hostname']
    items['map'] = properties['mapname']
    items['game'] = properties['gamename']
    items['player_count'] = properties['players']
    items['max_players'] = properties['sv_maxclients']
    items['bot_count'] = None
    items['server_type'] = properties['fs_game']
    items['vac_enabled'] = None
    items['version'] = properties['shortversion']

    return items


def change_server_info(properties):
    items = dict()

    items['server_name'] = ['Názov servera', properties['server_name']]
    items['map'] = ['Mapa', properties['map']]
    items['player_count'] = ['Počet hráčov', str(properties['player_count']) + '/' + str(properties['max_players'])]
    items['server_type'] = ['Typ servera', properties['server_type']]
    items['version'] = ['Verzia', properties['version']]

    if properties['bot_count'] is not None:
        items['bot_count'] = ['Počet botov', properties['bot_count']]
    if properties['vac_enabled'] is not None:
        items['vac_enabled'] = ['VAC', properties['vac_enabled']]

    return items


def get_server_info(game, port, ip=SERVER_IP):
    if game == 'cod-4':
        ###############################
        # Stats Receiver Function     #
        # by NeckCracker.de aka Kurbl #
        ###############################

        # init socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.connect((ip, port))

        # send "handshake" and status request
        sock.send(b"\xFF\xFF\xFF\xFFgetstatus\x00")

        # receive data
        try:
            msg = sock.recv(5000)

            last = msg

            if len(msg) == 5000:
                while last != '':
                    last = sock.recv(5000)
                    if last == '':
                        break
                    else:
                        msg = msg + last

            # parse properties
            raw_properties = msg.split(b'\\')
            properties = {}

            raw_properties = raw_properties[1:]
            items = range(len(raw_properties))

            for i in items:
                if i % 2 == 0:
                    if raw_properties[i] != b'mod':
                        properties[raw_properties[i].decode('ascii')] = raw_properties[i+1].decode('ascii')
                    else:
                        t = raw_properties[i+1].split(b'\n')
                        properties[raw_properties[i]] = t[0]
                        del t[0]
                        properties['players'] = str(len(t)-1)

            # close socket
            sock.close()

            # return properties
            return change_server_info(change_server_info_to_valve(properties))

        except:
            return -1

    elif game == 'cs-go' or game == 'cs-s' or game == 'cs-16':
        try:
            server = ServerQuerier((ip, port))
            return change_server_info(server.get_info())
        except:
            return -1


def shut_down():
    servers = Server.objects.all()

    for server in servers:

        server_info = get_server_info(server.game.special_name, server.port)
        if server_info == -1 or server_info['player_count'][1][0] == '0':
            server.value -= 1
        else:
            server.value += 1
            server.value = min(server.value, 3)

        server.save()

        if server.value == 0:
            system(server.path_to_script + ' stop')
            server.delete()
