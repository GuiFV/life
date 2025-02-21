from itertools import groupby
from operator import attrgetter
from life.gym.models import ProgramExercise


def group_exercises_by_group(training_programs):
    """
    Utility function to group exercises by their 'group' attribute in the order
    defined in ProgramExercise.GroupChoices.
    """
    # Define a list to enforce the 'group' order based on GroupChoices
    group_order = [
        ProgramExercise.GroupChoices.RELEASE,
        ProgramExercise.GroupChoices.STRETCHING,
        ProgramExercise.GroupChoices.MOBILITY,
        ProgramExercise.GroupChoices.MOTOR_CONTROL,
        ProgramExercise.GroupChoices.STABILITY,
        ProgramExercise.GroupChoices.POWER,
        ProgramExercise.GroupChoices.STRENGTH,
    ]

    # Iterate through each training program
    for program in training_programs:
        # Sort the exercises by 'group' (based on group_order) and 'order'
        sorted_exercises = sorted(
            program.programexercise_set.all(),
            key=lambda ex: (group_order.index(ex.group), ex.order),
        )

        # Group exercises by 'group', maintaining the desired order
        program.grouped_exercises = {
            ProgramExercise.GroupChoices(group).label: list(exercises)
            for group, exercises in groupby(sorted_exercises, key=attrgetter('group'))
        }
