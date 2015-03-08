from gamepanel.models import Clients
from gamepanel.models import Game
from gamepanel.models import GameMap
from gamepanel.models import GameType
from gamepanel.models import Mode
from gamepanel.models import PromodMode
from gamepanel.models import Server

from django.contrib import admin


class GameTypeInlineAdmin(admin.StackedInline):
    model = GameType
    extra = 1


class GameMapInlineAdmin(admin.StackedInline):
    model = GameMap
    extra = 1


class ClientsInlineAdmin(admin.StackedInline):
    model = Clients
    extra = 1


class ModeInlineAdmin(admin.StackedInline):
    model = Mode
    extra = 1


class PromodModeInlineAdmin(admin.StackedInline):
    model = PromodMode
    extra = 1


class GameAdmin(admin.ModelAdmin):
    inlines = [GameTypeInlineAdmin, GameMapInlineAdmin, ClientsInlineAdmin, ModeInlineAdmin, PromodModeInlineAdmin]


class ServerAdmin(admin.ModelAdmin):
    list_display = ['game', 'hostname', 'clients', 'port', 'value', 'datetime']


admin.site.register(Game, GameAdmin)
admin.site.register(Server, ServerAdmin)
