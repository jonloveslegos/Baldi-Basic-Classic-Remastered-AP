import os

import settings
import typing
import random

from Options import OptionError
from Utils import visualize_regions
from .Options import BBCROptions  # the options we defined earlier
from .Items import BBCRItem, item_table  # data used below to add items to the World
from .Locations import BBCRLocation, location_table  # same as above
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, MultiWorld, CollectionState
from .Regions import create_regions, connect_entrances
from . import Rules
from ..generic.Rules import set_rule, add_rule


class BBCRWeb(WebWorld):
    theme = "stone"
    options_presets = {
        "Baldis Basics Classic Remastered": {
            "sample_option": True,
        }
    }


class BBCRWorld(World):
    """Welcome to Baldi's Basics in education, and learning! That's me!"""
    game = "Baldis Basics Classic Remastered"  # name of the game/world
    options_dataclass = BBCROptions  # options the player can set
    options: BBCROptions  # typing hints for option results
    # settings: typing.ClassVar[MyGameSettings]  # will be automatically assigned from type hint
    topology_present = False  # show path to required location checks in spoiler





    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 1
    # instead of dynamic numbering, IDs could be part of data

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for
                       name, id in item_table.items()}
    location_name_to_id = {name: id for
                           name, id in location_table.items()}

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    item_name_groups = {
        "Notebooks": {"Notebook"},
    }


    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)



    def create_regions(self):
        create_regions(self)
        if not self.options.doorsanity:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Exit", "Region", self.player) and state.has("Notebook", self.player, 7)
        elif self.options.doorsanity:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Exit", "Region", self.player) and state.has("Notebook",
                        self.player, 7) and state.has("East Exit", self.player) and state.has("West Exit", self.player) and state.has("South Exit", self.player) and state.has("North Exit",
                        self.player) and state.can_reach("Cafeteria", "Region", self.player)


    def create_item(self, name: str) -> "Item":
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self):
        starting_pool = len(self.multiworld.itempool)
        print(str(self.options.required_route))
        starting_locations = len(self.multiworld.get_unfilled_locations(self.player))

        totalItems = len(self.multiworld.get_unfilled_locations(self.player))
        print(len(self.multiworld.get_unfilled_locations(self.player)))
        NotebookNumber = 7
        BSODANumber = 3
        ScissorsNumber = 3
        ZestyNumber = 3
        SwingDoorLockNum = 1
        PKeysNumber = 1
        WDNoSqNumber = 2
        ACNumber = 1
        BigBootNumber = 1
        QuarterNumber = 3
        trap_amount = self.options.trap_weight

        print(totalItems)

        if not self.options.item_usage:
            for _ in range(NotebookNumber):
                self.multiworld.itempool.append(Item("Notebook", ItemClassification.progression, self.item_name_to_id["Notebook"], self.player))
                totalItems -= 1
                NotebookNumber -= 1
                print(totalItems)
                print("Notebooks" + str(NotebookNumber))

            for _ in range(BSODANumber):
                self.multiworld.itempool.append(Item("BSODA", ItemClassification.useful, self.item_name_to_id["BSODA"], self.player))
                BSODANumber -= 1
                totalItems -= 1
                print(totalItems)
                print("BSODAS" + str(BSODANumber))

            self.multiworld.itempool.append(Item("Baldi's Least Favorite Tape", ItemClassification.useful, self.item_name_to_id["Baldi's Least Favorite Tape"], self.player))
            totalItems -= 1
            print(totalItems)
            print("Unfortunately, Baldi's Least Favorite Tape was added to the itempool")

            for _ in range(ScissorsNumber):
                self.multiworld.itempool.append(Item("Safety Scissors", ItemClassification.useful, self.item_name_to_id["Safety Scissors"], self.player))
                totalItems -= 1
                ScissorsNumber -= 1
                print(totalItems)
                print("Scissors for safety" + str(ScissorsNumber))

            for _ in range(ZestyNumber):
                self.multiworld.itempool.append(Item("Zesty Bar", ItemClassification.useful, self.item_name_to_id["Zesty Bar"], self.player))
                totalItems -= 1
                ZestyNumber -= 1
                print(totalItems)
                print("Zesty Bars" + str(ZestyNumber))

            for _ in range(SwingDoorLockNum):
                self.multiworld.itempool.append(Item("Swinging Door Lock", ItemClassification.useful, self.item_name_to_id["Swinging Door Lock"], self.player))
                totalItems -= 1
                SwingDoorLockNum -= 1
                print(totalItems)
                print("Swinging Door Lock" + str(SwingDoorLockNum))

            for _ in range(PKeysNumber):
                self.multiworld.itempool.append(Item("Principal's Keys", ItemClassification.useful, self.item_name_to_id["Principal's Keys"], self.player))
                totalItems -= 1
                PKeysNumber -= 1
                print(totalItems)
                print("Principal's Keys" + str(PKeysNumber))

            for _ in range(WDNoSqNumber):
                self.multiworld.itempool.append(Item("WD-NoSquee", ItemClassification.useful, self.item_name_to_id["WD-NoSquee"], self.player))
                totalItems -= 1
                WDNoSqNumber -= 1
                print(totalItems)
                print("WD-NoSquee" + str(WDNoSqNumber))

            for _ in range(ACNumber):
                self.multiworld.itempool.append(Item("Alarm Clock", ItemClassification.useful, self.item_name_to_id["Alarm Clock"], self.player))
                totalItems -= 1
                ACNumber -= 1
                print(totalItems)
                print("Alarm Clock" + str(ACNumber))

            for _ in range(BigBootNumber):
                self.multiworld.itempool.append(Item("Big 'Ol Boots", ItemClassification.useful, self.item_name_to_id["Big 'Ol Boots"], self.player))
                totalItems -= 1
                BigBootNumber -= 1
                print(totalItems)
                print("Big 'Ol Boots" + str(BigBootNumber))

            for _ in range(QuarterNumber):
                self.multiworld.itempool.append(Item("Quarter", ItemClassification.progression, self.item_name_to_id["Quarter"], self.player))
                totalItems -= 1
                print("Quarter")
                print(totalItems)
        else:
            for _ in range(NotebookNumber):
                self.multiworld.itempool.append(
                    Item("Notebook", ItemClassification.progression, self.item_name_to_id["Notebook"], self.player))
                totalItems -= 1
                NotebookNumber -= 1
                print(totalItems)
                print("Notebooks" + str(NotebookNumber))

            for _ in range(BSODANumber):
                self.multiworld.itempool.append(
                    Item("BSODA", ItemClassification.progression, self.item_name_to_id["BSODA"], self.player))
                BSODANumber -= 1
                totalItems -= 1
                print(totalItems)
                print("BSODAS" + str(BSODANumber))

            self.multiworld.itempool.append(Item("Baldi's Least Favorite Tape", ItemClassification.progression,
                                                 self.item_name_to_id["Baldi's Least Favorite Tape"], self.player))
            totalItems -= 1
            print(totalItems)
            print("Unfortunately, Baldi's Least Favorite Tape was added to the itempool")

            for _ in range(ScissorsNumber):
                self.multiworld.itempool.append(Item("Safety Scissors", ItemClassification.progression, self.item_name_to_id["Safety Scissors"], self.player))
                totalItems -= 1
                ScissorsNumber -= 1
                print(totalItems)
                print("Scissors for safety" + str(ScissorsNumber))

            for _ in range(ZestyNumber):
                self.multiworld.itempool.append(
                    Item("Zesty Bar", ItemClassification.progression, self.item_name_to_id["Zesty Bar"], self.player))
                totalItems -= 1
                ZestyNumber -= 1
                print(totalItems)
                print("Zesty Bars" + str(ZestyNumber))

            for _ in range(SwingDoorLockNum):
                self.multiworld.itempool.append(
                    Item("Swinging Door Lock", ItemClassification.progression, self.item_name_to_id["Swinging Door Lock"],
                         self.player))
                totalItems -= 1
                SwingDoorLockNum -= 1
                print(totalItems)
                print("Swinging Door Lock" + str(SwingDoorLockNum))

            for _ in range(PKeysNumber):
                self.multiworld.itempool.append(
                    Item("Principal's Keys", ItemClassification.progression, self.item_name_to_id["Principal's Keys"],
                         self.player))
                totalItems -= 1
                PKeysNumber -= 1
                print(totalItems)
                print("Principal's Keys" + str(PKeysNumber))

            for _ in range(WDNoSqNumber):
                self.multiworld.itempool.append(
                    Item("WD-NoSquee", ItemClassification.progression, self.item_name_to_id["WD-NoSquee"], self.player))
                totalItems -= 1
                WDNoSqNumber -= 1
                print(totalItems)
                print("WD-NoSquee" + str(WDNoSqNumber))

            for _ in range(ACNumber):
                self.multiworld.itempool.append(
                    Item("Alarm Clock", ItemClassification.progression, self.item_name_to_id["Alarm Clock"], self.player))
                totalItems -= 1
                ACNumber -= 1
                print(totalItems)
                print("Alarm Clock" + str(ACNumber))

            for _ in range(BigBootNumber):
                self.multiworld.itempool.append(
                    Item("Big 'Ol Boots", ItemClassification.progression, self.item_name_to_id["Big 'Ol Boots"],
                         self.player))
                totalItems -= 1
                BigBootNumber -= 1
                print(totalItems)
                print("Big 'Ol Boots" + str(BigBootNumber))

            for _ in range(QuarterNumber):
                self.multiworld.itempool.append(
                    Item("Quarter", ItemClassification.progression, self.item_name_to_id["Quarter"], self.player))
                totalItems -= 1
                print("Quarter")
                print(totalItems)

        if self.options.doorsanity:
            # Yellow Doors
            if self.options.required_route == 1 and self.options.notechecks == 0:
                self.multiworld.push_precollected(self.create_item("Yellow Swinging Door - North of Start"))
            else:
                self.multiworld.itempool.append(Item("Yellow Swinging Door - North of Start", ItemClassification.progression, self.item_name_to_id["Yellow Swinging Door - North of Start"], self.player))
                totalItems -=1

            self.multiworld.itempool.append(
                Item("Yellow Swinging Door - West of Start", ItemClassification.progression, self.item_name_to_id["Yellow Swinging Door - West of Start"], self.player))
            self.multiworld.itempool.append(
                Item("Yellow Swinging Door - East of Start", ItemClassification.progression, self.item_name_to_id["Yellow Swinging Door - East of Start"], self.player))
            self.multiworld.itempool.append(
                Item("Yellow Swinging Door - Cafeteria West", ItemClassification.progression, self.item_name_to_id["Yellow Swinging Door - Cafeteria West"], self.player))
            self.multiworld.itempool.append(
                Item("Yellow Swinging Door - Cafeteria East", ItemClassification.progression, self.item_name_to_id["Yellow Swinging Door - Cafeteria East"], self.player))
            self.multiworld.itempool.append(
                Item("Yellow Swinging Door - Right of Detention", ItemClassification.progression, self.item_name_to_id["Yellow Swinging Door - Right of Detention"], self.player))
            self.multiworld.itempool.append(Item("Yellow Swinging Door - Left of Detention", ItemClassification.progression, self.item_name_to_id["Yellow Swinging Door - Left of Detention"], self.player))
            self.multiworld.itempool.append(
                Item("Yellow Swinging Door - North-East Halls", ItemClassification.progression, self.item_name_to_id["Yellow Swinging Door - North-East Halls"], self.player))
            totalItems -= 7
            print("Yellow Doors" + str(totalItems))

            # 99 Doors
            if self.options.required_route == 1 and (not self.options.notechecks) and self.options.doorsanity:
                self.multiworld.push_precollected(self.create_item("99 Door - Starting Classroom West"))
                self.multiworld.push_precollected(self.create_item("99 Door - Starting Classroom East"))
            else:
                randomdoor = random.randint(1, 10)
                if randomdoor >= 6:
                    self.multiworld.push_precollected(self.create_item("99 Door - Starting Classroom West"))
                    self.multiworld.itempool.append(
                        Item("99 Door - Starting Classroom East", ItemClassification.progression,
                             self.item_name_to_id["99 Door - Starting Classroom East"], self.player))
                elif randomdoor <= 5:
                    self.multiworld.push_precollected(self.create_item("99 Door - Starting Classroom East"))
                    self.multiworld.itempool.append(
                        Item("99 Door - Starting Classroom West", ItemClassification.progression,
                             self.item_name_to_id["99 Door - Starting Classroom West"], self.player))
                totalItems -= 1

            # self.multiworld.itempool.append(
            #     Item("99 Door - Starting Classroom West", ItemClassification.progression, self.item_name_to_id["99 Door - Starting Classroom West"], self.player))
            # self.multiworld.itempool.append(
            #     Item("99 Door - Starting Classroom East", ItemClassification.progression, self.item_name_to_id["99 Door - Starting Classroom East"], self.player))
            self.multiworld.itempool.append(
                Item("99 Door - Classroom Near Center", ItemClassification.progression, self.item_name_to_id["99 Door - Classroom Near Center"], self.player))
            self.multiworld.itempool.append(
                Item("99 Door - Classroom South of Cafeteria", ItemClassification.progression, self.item_name_to_id["99 Door - Classroom South of Cafeteria"], self.player))
            self.multiworld.itempool.append(
                Item("99 Door - Classroom West of Cafeteria", ItemClassification.progression, self.item_name_to_id["99 Door - Classroom West of Cafeteria"], self.player))
            self.multiworld.itempool.append(
                Item("99 Door - Classroom by East Exit", ItemClassification.progression, self.item_name_to_id["99 Door - Classroom by East Exit"], self.player))
            self.multiworld.itempool.append(
                Item("99 Door - Classroom in North East Halls", ItemClassification.progression, self.item_name_to_id["99 Door - Classroom in North East Halls"], self.player))
            totalItems -= 5
            print("99 Door" + str(totalItems))

            self.multiworld.itempool.append(
                Item("Supply Closet Door", ItemClassification.progression,
                     self.item_name_to_id["Supply Closet Door"], self.player))
            totalItems -= 1

            # School Fac Doors
            self.multiworld.itempool.append(
                Item("School Faculty Door - South", ItemClassification.progression, self.item_name_to_id["School Faculty Door - South"], self.player))
            self.multiworld.itempool.append(
                Item("School Faculty Door - West by Exit", ItemClassification.progression, self.item_name_to_id["School Faculty Door - West by Exit"], self.player))
            self.multiworld.itempool.append(
                Item("School Faculty Door - Center", ItemClassification.progression, self.item_name_to_id["School Faculty Door - Center"], self.player))
            self.multiworld.itempool.append(
                Item("School Faculty Door - Connecting Rooms", ItemClassification.progression, self.item_name_to_id["School Faculty Door - Connecting Rooms"], self.player))
            self.multiworld.itempool.append(
                Item("School Faculty Door - East Halls", ItemClassification.progression, self.item_name_to_id["School Faculty Door - East Halls"], self.player))
            self.multiworld.itempool.append(
                Item("School Faculty Door - South East of Cafeteria", ItemClassification.progression, self.item_name_to_id["School Faculty Door - South East of Cafeteria"], self.player))
            totalItems -= 6
            print("School Faculty Door" + str(totalItems))

            # Exits
            self.multiworld.itempool.append(
                Item("East Exit", ItemClassification.progression, self.item_name_to_id["East Exit"], self.player))
            self.multiworld.itempool.append(
                Item("West Exit", ItemClassification.progression, self.item_name_to_id["West Exit"], self.player))
            self.multiworld.itempool.append(
                Item("North Exit", ItemClassification.progression, self.item_name_to_id["North Exit"], self.player))
            self.multiworld.itempool.append(
                Item("South Exit", ItemClassification.progression, self.item_name_to_id["South Exit"], self.player))
            totalItems -= 4
            print("Exit" + str(totalItems))

            if self.options.party:
                self.multiworld.itempool.append(Item("Purple Baldi (Party Style)", ItemClassification.progression, self.item_name_to_id["Purple Baldi (Party Style)"], self.player))
                self.multiworld.itempool.append(Item("Orange Baldi (Party Style)", ItemClassification.progression, self.item_name_to_id["Orange Baldi (Party Style)"], self.player))
                self.multiworld.itempool.append(Item("Green Baldi (Party Style)", ItemClassification.progression, self.item_name_to_id["Green Baldi (Party Style)"], self.player))
                self.multiworld.itempool.append(Item("Blue Baldi (Party Style)", ItemClassification.progression, self.item_name_to_id["Blue Baldi (Party Style)"], self.player))
                if self.options.which_style != 1:
                    self.multiworld.itempool.append(Item("Party Style", ItemClassification.progression, self.item_name_to_id["Party Style"], self.player))
                else:
                    self.multiworld.push_precollected(self.create_item("Party Style"))
            else:
                if self.options.which_style == 1:
                    print("Party Style isn't randomized. Giving " + str(self.player) + " Classic Style Instead.")
                    self.multiworld.push_precollected(self.create_item("Classic Style"))

            if self.options.demo:
                self.multiworld.itempool.append(Item("Number Balloons", ItemClassification.progression,
                                                     self.item_name_to_id["Number Balloons"], self.player))
                self.multiworld.itempool.append(Item("Number Balloon Receptacle", ItemClassification.progression,
                                                     self.item_name_to_id["Number Balloon Receptacle"], self.player))
                if self.options.which_style != 2:
                    self.multiworld.itempool.append(Item("Demo Style", ItemClassification.progression, self.item_name_to_id["Demo Style"], self.player))
                else:
                    self.multiworld.push_precollected(self.create_item("Demo Style"))
            else:
                if self.options.which_style == 1:
                    print("Demo Style isn't randomized. Giving " + str(self.player) + " Classic Style Instead.")
                    self.multiworld.push_precollected(self.create_item("Classic Style"))

            if self.options.which_style == 0:
                self.multiworld.push_precollected(self.create_item("Classic Style"))
            else:
                self.multiworld.itempool.append(
                    Item("Classic Style", ItemClassification.progression, self.item_name_to_id["Classic Style"], self.player))


        if totalItems >= 1:
            print("i have " + str(totalItems) + " items, so I'm gonna fill some stuff.")
            self.multiworld.itempool.append(Item("Quarter", ItemClassification.progression, self.item_name_to_id["Quarter"], self.player))
            totalItems -= 1
            print("Quarter")
            print(totalItems)
            print(totalItems * (trap_amount / 100))
            trap_amount = round(totalItems * (trap_amount / 100))
            if totalItems >= 1:
                if self.options.funny_traps:
                    for _ in range(trap_amount):
                        trap_choose = self.random.randint(1, 3)
                        if trap_choose == 1:
                            self.multiworld.itempool.append(Item("Jump Rope Time (Trap)", ItemClassification.trap, self.item_name_to_id["Jump Rope Time (Trap)"], self.player))
                        elif trap_choose == 2:
                            self.multiworld.itempool.append(Item("The Arts and Crafters Effect (Trap)", ItemClassification.trap, self.item_name_to_id["The Arts and Crafters Effect (Trap)"], self.player))
                        elif trap_choose == 3:
                            self.multiworld.itempool.append(Item("Detention For You. (When Will You Learn?) (Trap)", ItemClassification.trap, self.item_name_to_id["Detention For You. (When Will You Learn?) (Trap)"], self.player))
                        totalItems -= 1
                        print("Trap")
                        print(totalItems)
        if totalItems >= 1:
            for _ in range(totalItems):
                item_to_gen = self.random.randint(1, 12)
                print("item number" + str(item_to_gen))
                if item_to_gen == 1 or item_to_gen >= 10:
                    self.multiworld.itempool.append(
                        Item("BSODA", ItemClassification.useful, self.item_name_to_id["BSODA"], self.player))
                elif item_to_gen == 2:
                    self.multiworld.itempool.append(Item("Baldi's Least Favorite Tape", ItemClassification.useful, self.item_name_to_id["Baldi's Least Favorite Tape"], self.player))
                elif item_to_gen == 3:
                    if self.options.item_usage:
                        self.multiworld.itempool.append(Item("Safety Scissors", ItemClassification.progression, self.item_name_to_id["Safety Scissors"], self.player))
                    elif not self.options.item_usage:
                        self.multiworld.itempool.append(Item("Safety Scissors", ItemClassification.useful, self.item_name_to_id["Safety Scissors"], self.player))
                elif item_to_gen == 4:
                    self.multiworld.itempool.append(
                        Item("Zesty Bar", ItemClassification.useful, self.item_name_to_id["Zesty Bar"],
                             self.player))
                elif item_to_gen == 5:
                    self.multiworld.itempool.append(Item("Swinging Door Lock", ItemClassification.useful,
                                                         self.item_name_to_id["Swinging Door Lock"], self.player))
                elif item_to_gen == 6:
                    self.multiworld.itempool.append(Item("Principal's Keys", ItemClassification.useful,
                                                         self.item_name_to_id["Principal's Keys"], self.player))
                elif item_to_gen == 7:
                    self.multiworld.itempool.append(
                        Item("WD-NoSquee", ItemClassification.useful, self.item_name_to_id["WD-NoSquee"],
                             self.player))
                elif item_to_gen == 8:
                    self.multiworld.itempool.append(
                        Item("Alarm Clock", ItemClassification.useful, self.item_name_to_id["Alarm Clock"],
                             self.player))
                elif item_to_gen == 9:
                    self.multiworld.itempool.append(
                        Item("Big 'Ol Boots", ItemClassification.useful, self.item_name_to_id["Big 'Ol Boots"],
                             self.player))
                totalItems -= 1
                print(totalItems)

        if totalItems >= 1:
            print("greater than or equal to one")

        actual_added = len(self.multiworld.itempool) - starting_pool

        print("Locations:", starting_locations)
        print("Added:", actual_added)
        print("Difference:", actual_added - starting_locations)

        print(len(self.multiworld.itempool))
        print(totalItems)



    def connect_entrances(self) -> None:
        connect_entrances(self)



        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_BBCR_world.puml", show_entrance_names=True, regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[self.player])

    def generate_basic(self) -> None:
        state: CollectionState = self.multiworld.get_all_state()
        state.update_reachable_regions(self.player)
        reachable_regions: set[Region] = set(state.reachable_regions[self.player])
        unreachable_regions: set[Region] = set()  # type: ignore
        for region in self.multiworld.regions:
            if region not in reachable_regions:
                unreachable_regions.add(region)
        visualize_regions(root_region=self.get_region(region_name="Menu"), file_name=f"{self.player_name}_world.puml",
                          show_entrance_names=True, regions_to_highlight=unreachable_regions)

        return super().generate_basic()

    def fill_slot_data(self) -> dict[str, any]:
        # In order for our game client to handle the generated seed correctly we need to know what the user selected
        # for their difficulty and final boss HP.
        # A dictionary returned from this method gets set as the slot_data and will be sent to the client after connecting.
        # The options dataclass has a method to return a `Dict[str, Any]` of each option name provided and the relevant
        # option's value.
        names = ["required_route", "notechecks", ]
        return self.options.as_dict(*names)


    def generate_output(self, output_directory: str) -> None:
        ConnectInf ="""ip=[replace these brackets with the server name, like archipelago.gg]
    port=[port number]
    slot=[slot name]
    pass=[password. remove brackets if none]
    [please move back port, slot, and pass so that they are all along side ip. I don't know how to fix it.]"""
        print(ConnectInf)

        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.aptxt"
        with open(os.path.join(output_directory, filename), 'w') as f:
            f.write(ConnectInf)