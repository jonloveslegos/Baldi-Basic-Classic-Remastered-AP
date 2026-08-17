import typing
from dataclasses import dataclass
from Options import Option, Range, Toggle, PerGameCommonOptions, DefaultOnToggle, DeathLink, Choice, OptionGroup


class RequiredRoute(Choice):
    """Which route you wanna do? Neutral, which means just beat the game, or Terrible, which means fail every problem to get to NULL."""
    display_name = "Required Route"
    option_neutral = 0
    option_terrible = 1
    option_either = 2
    default = 0

class RandomParty(Toggle):
    """Randomize Party Style?"""
    display_name = "Randomize Party"
    default = False

class RandomDemo(Toggle):
    """Randomize Demo Style?"""
    display_name = "Randomize Demo"
    default = False

class WhichStyle(Choice):
    """Which style do you want to start with?"""
    display_name = "Which Style"
    option_classic = 0
    option_party = 1
    option_demo = 2
    default = 0

class ReqGoal(Choice):
    """Which style do you want to beat to win?"""
    display_name = "Goal Style"
    option_classic = 0
    option_party = 1
    option_demo = 2
    default = 0

class Traps(Toggle):
    """These traps take the place of a few filler Quarters. Includes getting hit with Arts and Crafters, having to jump rope from Playtime, and a random teleport to Detention."""
    display_name = "Traps"
    default = False

class Trap_Weight(Range):
    """Determine the weight of your traps. This is percentage based of how many fillers you have left."""
    display_name = "Trap Weight"
    range_start = 0
    range_end = 100
    default = 10

class ExtraNotebookChecks(Toggle):
    """This makes the questions inside each notebook a check."""
    display_name = "Notebook Questions Checks"
    default = False

class ItemUsage(Toggle):
    """Turns items like the Scissors progressive, and adds locations for their usage.
    for example, using the scissors on Playtime or using the Principal's Keys on the Dentention door."""
    display_name = "Item Usage"
    default = False

class Doorsanity(Toggle):
    """Adds the 99 doors, School Faculty Doors, and the Yellow Swinging Doors to the itempool.
    Passing through doors are now checks. :)

    I should also mention that when Notesanity is off and Req Route is Terrible, this will give
    you another door to start with so that it doesn't break, crash, or throw any errors in my face.
    thank you."""
    display_name = "Door Sanity"
    default = False

@dataclass
class BBCROptions(PerGameCommonOptions):
    required_route: RequiredRoute
    party: RandomParty
    demo: RandomDemo
    which_style: WhichStyle
    req_style: ReqGoal
    notechecks: ExtraNotebookChecks
    doorsanity: Doorsanity
    item_usage: ItemUsage
    funny_traps: Traps
    trap_weight: Trap_Weight
    death_link: DeathLink


option_definitions = {
    "required_route": RequiredRoute,
}

option_groups = [
    OptionGroup("Gameplay Options", [RequiredRoute, ExtraNotebookChecks, ItemUsage]),

    OptionGroup("Trap Options", [Traps, Trap_Weight]),

    OptionGroup("Death Link", [DeathLink]),
]