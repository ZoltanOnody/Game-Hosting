from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=128)
    special_name = models.CharField(max_length=128, default="")
    active = models.BooleanField(default=True)
    path_to_folder = models.CharField(max_length=256)
    path_to_script = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    cover = models.CharField(max_length=256, blank=True)

    boolean_hostname = models.BooleanField(default=False)
    boolean_serv_pass = models.BooleanField(default=False)
    boolean_rcon_pass = models.BooleanField(default=False)
    boolean_clients = models.BooleanField(default=False)
    boolean_game_type = models.BooleanField(default=False)
    boolean_promod_mode = models.BooleanField(default=False)
    boolean_mode = models.BooleanField(default=False)
    boolean_map = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hra'
        verbose_name_plural = 'Hry'
        ordering = ['-active', 'name']


class Clients(models.Model):
    game = models.ForeignKey(Game)
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)


class GameMap(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=128)
    special_name = models.CharField(max_length=64)

    def __str__(self):
        return self.special_name


class GameType(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=64)
    special_name = models.CharField(max_length=64)

    def __str__(self):
        return self.special_name


class PromodMode(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=64)
    special_name = models.CharField(max_length=64)

    def __str__(self):
        return self.special_name


class Mode(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=64)
    special_name = models.CharField(max_length=64)

    def __str__(self):
        return self.special_name


class Server(models.Model):
    game = models.ForeignKey(Game)

    # requirement depends on game
    clients = models.ForeignKey(Clients, null=True)
    game_type = models.ForeignKey(GameType, null=True)
    promod_mode = models.ForeignKey(PromodMode, null=True)
    mode = models.ForeignKey(Mode, null=True)
    map = models.ForeignKey(GameMap, null=True)

    # Info about server
    hostname = models.CharField(max_length=64)
    password = models.CharField(max_length=20)
    rcon_pass = models.CharField(max_length=64)
    serv_pass = models.CharField(max_length=64, blank=True)
    port = models.PositiveIntegerField()

    # Other
    path_to_script = models.CharField(max_length=256)
    path_to_config = models.CharField(max_length=256)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    value = models.IntegerField(default=3, blank=True)

    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = 'Server'
        verbose_name_plural = 'Servery'
        ordering = ['datetime']
