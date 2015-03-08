from os import system


class CreateFiles:
    def __init__(self, game, server):

        self.game = game
        self.server = server

        if game.special_name == 'cod-4':
            self.cod4_script()
            self.cod4_config()
        elif game.special_name == 'cs-go':
            self.csgo_script()
            self.csgo_config()
        elif game.special_name == 'cs-s':
            self.css_script()
            self.css_config()
        elif game.special_name == 'cs-16':  # css is same as cs1.6 so I can do this ... even if I shouldn't
            self.css_script()
            self.css_config()

    def cod4_config(self):
        hostname = self.server.hostname
        max_clients = self.server.clients
        rcon_pass = self.server.rcon_pass
        srv_pass = self.server.serv_pass
        game_type = self.server.game_type
        promod_mode = self.server.promod_mode
        mp = self.server.map

        path_to_config = self.game.path_to_folder + str(self.server.mode) + '/' + str(self.server.port) + '.cfg'

        f = open(path_to_config, 'w')
        f.write("""
// info strings
sets _Admin ""
sets _Email ""
sets _Website ""
sets _Location ""
sets _Irc ""
sets sv_hostname "%(hostname)s"

// welcome message, message of the day (motd)
seta scr_motd "Please visit"

// password settings
set rcon_password "%(rcon_pass)s"
set sv_privatePassword ""
set g_password "%(srv_pass)s"

// player slots, maxclients - privateclients = public slots
set sv_maxclients "%(max_clients)s"
set sv_privateclients ""

// client download settings
seta sv_wwwDownload "0"
seta sv_wwwBaseURL ""
seta sv_wwwDlDisconnected "0"

set sv_mapRotation gametype "%(game_type)s" map "%(map)s"

// promod settings
set promod_mode "%(promod_mode)s"
set promod_enable_scorebot "0"
""" % {'hostname': hostname, 'max_clients': max_clients, 'rcon_pass': rcon_pass,
       'srv_pass': srv_pass, 'game_type': game_type, 'map': mp, 'promod_mode': promod_mode})

    def cod4_script(self):
        path_to_script = self.game.path_to_script

        original_script = open(path_to_script + 'cod4_script.sh', 'r')
        custom_script = open(self.server.path_to_script + '', 'w')

        settings = '#!/bin/bash\n'
        settings += 'screen_name="' + str(self.server.port) + '"\n'
        settings += 'mod="' + str(self.server.mode) + '"\n'

        custom_script.write(settings + str(original_script.read()))

        system('chmod +x ' + self.server.path_to_script)

    def csgo_config(self):
        hostname = self.server.hostname
        rcon_pass = self.server.rcon_pass
        srv_pass = self.server.serv_pass

        path_to_config = self.game.path_to_folder + str(self.server.port) + '.cfg'

        f = open(path_to_config, 'w')
        f.write("""

hostname "%(hostname)s" //Nazov servera
rcon_password "%(rcon_pass)s" //rcon heslo
sv_password "%(srv_pass)s" //server heslo

mp_join_grace_time "15" //The amount of time players can join teams after a round has started
mp_match_end_restart "0" // Defines whether a map should be restarted after a game has ended

sv_cheats "0" //This should always be set, so you know it's not on
sv_lan "0" //This should always be set, so you know it's not on

//**The bot commands below are mostly default with the exception of
bot_join_after_player "0"

//**The following commands manage kicks and bans
writeid
writeip
exec banned_user.cfg
exec banned_ip.cfg

//Others
sv_pure "1"
sv_allowupload "1"
sv_allowdownload "1"
sv_hibernate_when_empty "0"
sv_forcepreload "1"
""" % {'hostname': hostname, 'rcon_pass': rcon_pass, 'srv_pass': srv_pass })

    def csgo_script(self):
        path_to_script = self.game.path_to_script

        original_script = open(path_to_script + 'csgo_script.sh', 'r')
        custom_script = open(self.server.path_to_script + '', 'w')

        settings = '#!/bin/bash\n'
        settings += 'screen_name="' + str(self.server.port) + '"\n'
        settings += 'map="' + str(self.server.map) + '"\n'

        custom_script.write(settings + str(original_script.read()))
        system('chmod +x ' + self.server.path_to_script)

    def css_config(self):
        hostname = self.server.hostname
        rcon_pass = self.server.rcon_pass
        srv_pass = self.server.serv_pass

        path_to_config = self.game.path_to_folder + str(self.server.port) + '.cfg'

        f = open(path_to_config, 'w')
        f.write("""
hostname "%(hostname)s" //Nazov servera
rcon_password "%(rcon_pass)s" //rcon heslo
sv_password "%(srv_pass)s" //server heslo
""" % {'hostname': hostname, 'rcon_pass': rcon_pass, 'srv_pass': srv_pass })

    def css_script(self):
        path_to_script = self.game.path_to_script

        original_script = open(path_to_script + 'css_script.sh', 'r')
        custom_script = open(self.server.path_to_script + '', 'w')

        settings = '#!/bin/bash\n'
        settings += 'screen_name="' + str(self.server.port) + '"\n'
        settings += 'map="' + str(self.server.map) + '"\n'
        settings += 'max_players="' + str(self.server.clients) + '"\n'

        custom_script.write(settings + str(original_script.read()))

        system('chmod +x ' + self.server.path_to_script)
