from gamepanel.models import Server
from gamepanel.models import Clients
from gamepanel.models import GameType
from gamepanel.models import GameMap
from gamepanel.models import PromodMode
from gamepanel.models import Mode

from django.forms import ModelForm
from django.forms import Form
from django.forms import TextInput
from django.forms import Select
from django.forms import EmailField
from django.forms import CharField
from django.forms import Textarea
from django.forms import EmailInput

from captcha.fields import CaptchaField


class CreateServer(ModelForm):
    def __init__(self, g, *args, **kwargs):
        super(CreateServer, self).__init__(*args, **kwargs)  # populates the post

        data = [
            ('hostname', g.boolean_hostname, 'text'),
            ('serv_pass', g.boolean_serv_pass, 'text'),
            ('rcon_pass', g.boolean_rcon_pass, 'text'),
            ('clients', g.boolean_clients, 'select', Clients),
            ('game_type', g.boolean_game_type, 'select', GameType),
            ('promod_mode', g.boolean_promod_mode, 'select', PromodMode),
            ('mode', g.boolean_mode, 'select', Mode),
            ('map', g.boolean_map, 'select', GameMap),
        ]
        for row in data:
            if row[1]:
                if row[2] == 'text':
                    self.fields[row[0]].widget = TextInput(attrs={'class': 'form-control'})
                elif row[2] == 'select':
                    if row[0] != 'clients':
                        choices = row[3].objects.filter(game=g)
                        self.fields[row[0]].widget = Select(
                            attrs={'class': 'form-control'},
                            choices=((x.id, x.name) for x in choices)
                        )
                    else:
                        choices = row[3].objects.filter(game=g)
                        self.fields[row[0]].widget = Select(
                            attrs={'class': 'form-control'},
                            choices=((x.id, x.number) for x in choices)
                        )
            else:
                del self.fields[row[0]]

    class Meta:
        model = Server
        queryset = Server.objects.filter()
        fields = ['hostname', 'clients', 'rcon_pass', 'serv_pass', 'mode', 'game_type', 'promod_mode', 'map']
        labels = {
            'hostname': 'Názov servera',
            'clients': 'Počet hráčov',
            'rcon_pass': 'Rcon heslo',
            'serv_pass': 'Heslo na server',
            'game_type': 'Typ hry',
            'promod_mode': 'Promod mód',
            'mode': 'Mód',
        }
        help_texts = {
            'hostname': 'Zadajte aký názov servera chcete mť.',
            'rcon_pass': 'Heslo na server s ktorý môžete meniť nastavenia.',
        }


class ContactForm(Form):
    subject = CharField(widget=TextInput(attrs={'class': 'form-control'}), label="Predmet")
    sender = EmailField(widget=EmailInput(attrs={'class': 'form-control'}), label="Váš email")
    message = CharField(widget=Textarea(attrs={'class': 'form-control'}), label="Vaša správa")
    captcha = CaptchaField()
