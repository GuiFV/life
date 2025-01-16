from django.db import models
from django.utils.translation import gettext_lazy as _


class Series(models.Model):
    """A series of exercises for a given user"""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name=_("Usuário"))
    name = models.CharField(max_length=100, verbose_name=_("Nome da série"))
    active = models.BooleanField(default=True, verbose_name=_("Ativa"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))

    class Meta:
        verbose_name = _("Série do usuário")
        verbose_name_plural = _("Séries do usuário")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.name}"


class Exercise(models.Model):
    """The exercise itself."""
    name = models.CharField(max_length=100, verbose_name=_("Nome do Exercício"))
    video_url = models.URLField(blank=True, verbose_name=_("URL do Vídeo"))

    @property
    def embed_url(self):
        """
           Converts video_url to YouTube embed format.
           Example: https://www.youtube.com/watch?v=abc123 -> https://www.youtube.com/embed/abc123
           """
        if self.video_url and 'watch?v=' in self.video_url:
            return self.video_url.replace('watch?v=', 'embed/')
        return self.video_url

    class Meta:
        verbose_name = _("Exercício")
        verbose_name_plural = _("Exercícios")

    def __str__(self):
        return self.name


class SeriesExercise(models.Model):
    """The exercise in a series."""
    class ColorChoices(models.TextChoices):
        RED = "#FFCCCC", _("Vermelho")
        GREEN = "#CCFFCC", _("Verde")
        BLUE = "#CCCCFF", _("Azul")
        YELLOW = "#FFFFCC", _("Amarelo")
        PURPLE = "#E5CCFF", _("Roxo")
        PINK = "#FFCCE5", _("Rosa")

    class GroupChoices(models.TextChoices):
        STRETCHING = "stretching", _("Alongamento")
        MOBILITY = "mobility", _("Mobilidade")
        ACTIVATION = "activation", _("Ativação")
        MOTOR_CONTROL = "motor_control", _("Controle Motor")
        WARM_UP = "warm_up", _("Aquecimento")
        STRENGTH = "strength", _("Força")

    class UnitChoices(models.TextChoices):
        REPETITIONS = "repetitions", _("Repetições")
        SECONDS = "seconds", _("Segundos")

    series = models.ForeignKey('Series', on_delete=models.CASCADE, verbose_name=_("Série"))
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE, verbose_name=_("Exercício"))
    group = models.CharField(max_length=100, choices=GroupChoices.choices, verbose_name=_("Grupo"), default=GroupChoices.STRENGTH)
    order = models.PositiveIntegerField(verbose_name=_("Ordem"))
    color = models.CharField(max_length=10, choices=ColorChoices.choices, verbose_name=_("Cor"), blank=True, null=True)
    sets = models.PositiveIntegerField(verbose_name=_("Sets"))
    repetitions_or_time = models.PositiveIntegerField(verbose_name=_("Qtd. (Repetições ou Tempo)"))
    unit = models.CharField(max_length=15, choices=UnitChoices.choices, verbose_name=_("Unidade"), default=UnitChoices.REPETITIONS)
    load = models.PositiveIntegerField(verbose_name=_("Carga (Kg)"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))


    class Meta:
        verbose_name = _("Exercício da Série")
        verbose_name_plural = _("Exercícios da Série")

    def __str__(self):
        return f"{self.exercise.name}-{self.series.name}"
