from django.db import models
from django.utils.translation import gettext_lazy as _


class TrainingProgram(models.Model):
    """A program of exercises for a given user"""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name=_("User"))
    name = models.CharField(max_length=100, verbose_name=_("Programme name"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("User programme")
        verbose_name_plural = _("User programmes")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.name}"


class Exercise(models.Model):
    """The exercise itself."""
    name = models.CharField(max_length=100, verbose_name=_("Exercise name"))
    video_url = models.URLField(blank=True, verbose_name=_("Video URL"))

    @property
    def embed_url(self):
        """
        Converts video_url to YouTube embed format.
        Supports:
        - https://youtube.com/watch?v=<video_id>
        - https://youtube.com/shorts/<video_id>
        - https://youtu.be/<video_id>
        Converts to:
        - https://www.youtube.com/embed/<video_id>
        """
        if self.video_url:
            # Handle the standard YouTube watch URL
            if "watch?v=" in self.video_url:
                video_id = self.video_url.split("watch?v=")[1].split("&")[0]
                return f"https://www.youtube-nocookie.com/embed/{video_id}"

            # Handle YouTube Shorts URLs
            elif "youtube.com/shorts/" in self.video_url:
                video_id = self.video_url.split("youtube.com/shorts/")[1].split("?")[0]
                return f"https://www.youtube-nocookie.com/embed/{video_id}"

            # Handle shortened YouTube URLs
            elif "youtu.be/" in self.video_url:
                video_id = self.video_url.split("youtu.be/")[1].split("?")[0]
                return f"https://www.youtube-nocookie.com/embed/{video_id}"

        # Default: return as-is, if no recognized pattern is found
        return self.video_url

    class Meta:
        verbose_name = _("Exercise")
        verbose_name_plural = _("Exercises")

    def __str__(self):
        return self.name


class ProgramExercise(models.Model):
    """The exercise in a program."""
    class ColorChoices(models.TextChoices):
        RED = "#FFCCCC", _("Red")
        GREEN = "#CCFFCC", _("Green")
        BLUE = "#CCCCFF", _("Blue")
        YELLOW = "#FFFFCC", _("Yellow")
        PURPLE = "#E5CCFF", _("Purple")
        PINK = "#FFCCE5", _("Pink")

    class GroupChoices(models.TextChoices):
        RELEASE = "release", _("Release")
        STRETCHING = "stretching", _("Stretching")
        MOBILITY = "mobility", _("Mobility")
        MOTOR_CONTROL = "motor_control", _("Motor Control")
        STABILITY = "stability", _("Stability")
        POWER = "power", _("Power")
        STRENGTH = "strength", _("Strength")

    class UnitChoices(models.TextChoices):
        REPETITIONS = "repetitions", _("Repetitions")
        SECONDS = "seconds", _("Seconds")

    program = models.ForeignKey('TrainingProgram', on_delete=models.CASCADE, verbose_name=_("Programme"))
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE, verbose_name=_("Exercise"))
    group = models.CharField(max_length=100, choices=GroupChoices.choices, verbose_name=_("Group"), default=GroupChoices.STRENGTH)
    order = models.PositiveIntegerField(verbose_name=_("Order"))
    color = models.CharField(max_length=10, choices=ColorChoices.choices, verbose_name=_("Colour"), blank=True, null=True)
    sets = models.PositiveIntegerField(verbose_name=_("Sets"))
    repetitions_or_time = models.PositiveIntegerField(verbose_name=_("Qty. (Reps or Time)"))
    unit = models.CharField(max_length=15, choices=UnitChoices.choices, verbose_name=_("Unit"), default=UnitChoices.REPETITIONS)
    load = models.DecimalField(max_digits=5, decimal_places=1, verbose_name=_("Load (Kg)"), blank=True, null=True)
    observation = models.CharField(max_length=200, verbose_name=_("Observation"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))


    class Meta:
        verbose_name = _("Programme exercise")
        verbose_name_plural = _("Programme exercises")

    def __str__(self):
        return f"{self.exercise.name}-{self.program.name}"
