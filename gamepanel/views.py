from gamepanel.create_files import CreateFiles
from gamepanel.forms import ContactForm
from gamepanel.forms import CreateServer
from gamepanel.functions import get_first_unused_port
from gamepanel.functions import get_server_info
from gamepanel.models import Game
from gamepanel.models import Server
from gameserver_project.settings import ON_SERVER
from gameserver_project.settings import SERVER_IP

from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from os import system
from random import randint


def home(request):
    return render(request, 'gamepanel/home.html', {'title': 'Domov'})


def about(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                send_mail(request.POST['subject'], request.POST['message'], request.POST['sender'],
                          ['zoltan.onody@gmail.com', 'vservers.mail@gmail.com'], fail_silently=False)
                messages.add_message(request, messages.SUCCESS, 'Email bol odoslaný, budeme vás kontaktovať čím skôr!',
                                     extra_tags='alert-success')
            except:
                messages.add_message(request, messages.ERROR, 'Email bohužiaľ, nebol odoslaný, skúste prosím znova! '
                                                              'Ak problém pretrváva, napíšte nám na '
                                                              'vservers.mail(at)gmail.com a my vás budeme kontaktovať '
                                                              'čím skôr!',
                                     extra_tags='alert-danger')
            return HttpResponseRedirect('/about/')
    else:
        form = ContactForm()

    context = {
        'title': 'O nás',
        'form': form,
    }

    return render(request, 'gamepanel/about.html', context)


def create(request):
    list_of_games = Game.objects.filter(active=True)
    context = {
        'games': list_of_games,
        'title': 'Vytvoriť server',
    }
    return render(request, 'gamepanel/create.html', context)


def create_game(request, game_id):
    game = get_object_or_404(Game, id=int(game_id), active=True)

    if request.method == 'POST':
        form = CreateServer(game, request.POST)

        if form.is_valid():
            saver = form.save(commit=False)
            saver.game = game

            port = get_first_unused_port()
            if port == -1:
                messages.add_message(request, messages.ERROR, 'Bohužiaľ, všetky porty sú obsadené, skúste neskôr!',
                                     extra_tags='alert-danger')
                return HttpResponseRedirect(reverse('gamepanel:create'))

            saver.port = port
            saver.password = randint(10**15, (10**16)-1)
            saver.path_to_script = game.path_to_script + 'script-' + str(saver.port) + '.sh'

            saver.save()

            if ON_SERVER:
                server = get_object_or_404(Server, id=saver.id, password=saver.password)		

                CreateFiles(game, server)
                system(server.path_to_script + ' start')

            return HttpResponseRedirect(reverse('gamepanel:created_server', args=(str(saver.id), str(saver.password),)))
    else:
        form = CreateServer(g=game)

    context = {
        'form': form,
        'game': game,
        'title': game.name,
    }
    return render(request, 'gamepanel/create_game.html', context)


def created_server(request, server_id, password):
    server = get_object_or_404(Server, pk=int(server_id), password=password)

    context = {
        'server': server,
        'server_ip': SERVER_IP,
        'title': server.hostname + " - " + str(server.game)
    }

    if ON_SERVER:
        current_server_info = get_server_info(game=server.game.special_name, port=server.port, ip=SERVER_IP)
        u_context = {
            'current_server_info': current_server_info,
        }
        context.update(u_context)

    return render(request, 'gamepanel/created_server.html', context)


def command(request, server_id, password, sent_command):
    server = get_object_or_404(Server, pk=int(server_id), password=password)
    if sent_command == 'restart':
        if ON_SERVER:
            system(server.path_to_script + ' restart')
        messages.add_message(request, messages.SUCCESS, 'Server sa reštartoval!',
                             extra_tags='alert-success')
    elif sent_command == 'stop':
        if ON_SERVER:
            system(server.path_to_script + ' stop')
        messages.add_message(request, messages.SUCCESS, 'Server sa vypol a bol vymazaný z databázy! Ďakujeme!',
                             extra_tags='alert-success')

        server = get_object_or_404(Server, pk=int(server_id), password=password)
        server.delete()

        return HttpResponseRedirect(reverse('gamepanel:create'))
    elif sent_command == 'get_pb':
        if ON_SERVER:
            system(server.path_to_script + ' getscreen')
        messages.add_message(request, messages.SUCCESS, 'screens',
                             extra_tags='alert-success')
    else:
        messages.add_message(request, messages.ERROR, 'What did you do? You broke the server!!! Fatass...',
                             extra_tags='alert-danger')

    return HttpResponseRedirect(reverse('gamepanel:created_server', args=(server_id, password),))
