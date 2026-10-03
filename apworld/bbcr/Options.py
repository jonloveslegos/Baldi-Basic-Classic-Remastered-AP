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

class StartingStyle(Choice):
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

class NorthLogic(Toggle):
    """When enabled, this option makes it possible (not guaranteed!) that the game will expect you to
go north towards Baldi to get into the school halls. Would only recommend if you are good at the
game.

    ONLY WORKS WITH DOORSANITY!"""
    display_name = "North Yellow Door Logic"
    default = False

class ItemBehindItem(Toggle):
    """When enabled, this option will make sure that items will not be placed behind their
locations. For example, a Zesty Bar cannot be placed behind "Used a Zesty Bar".

    ONLY WORKS WITH ITEM USAGE CHECKS!"""
    display_name = "Item Behind Items"
    default = False

class YellowDoorNorth(Toggle):
    """When enabled, this option will make sure that the Yellow Swinging Door North of Start is NOT
the first yellow swinging door that the logic expects you to get to the halls through. It's really
only possible if either you're really skilled, or have a BSODA or two.

    ONLY WORKS WITH DOORSANITY!"""
    display_name = "North Yellow Door Logic"
    default = True

class GlitchedNotebook(Toggle):
    """When enabled, this will make the glitched notebooks at the end of Party Mode
locations. This will not add anymore Notebook items to the itempool.

ONLY WORKS IF PARTY MODE IS ON!!!"""
    display_name = "Glitched Notebook Checks"
    default = True

@dataclass
class BBCROptions(PerGameCommonOptions):
    required_route: RequiredRoute
    party: RandomParty
    demo: RandomDemo
    which_style: StartingStyle
    req_style: ReqGoal
    notechecks: ExtraNotebookChecks
    doorsanity: Doorsanity
    item_usage: ItemUsage
    funny_traps: Traps
    trap_weight: Trap_Weight
    north_logic: NorthLogic
    gnotebooks: GlitchedNotebook
    death_link: DeathLink
    itemitem: ItemBehindItem
    yndoorlogic: YellowDoorNorth


option_definitions = {
    "required_route": RequiredRoute,
}

option_groups_list = [
    OptionGroup("Base Options", [RandomParty, RandomDemo, RequiredRoute, StartingStyle, ReqGoal]),

    OptionGroup("Extra Options", [GlitchedNotebook, ExtraNotebookChecks, Doorsanity, ItemUsage]),

    OptionGroup("Trap Options", [Traps, Trap_Weight]),

    OptionGroup("Logic Options", [NorthLogic, ItemBehindItem, YellowDoorNorth]),

    OptionGroup("Death Link", [DeathLink]),
]