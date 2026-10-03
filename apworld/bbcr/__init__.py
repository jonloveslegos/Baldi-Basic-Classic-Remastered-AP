import os

import settings
import typing
import random

from Options import OptionError
from Utils import visualize_regions
from .Options import BBCROptions, option_groups_list  # the options we defined earlier
from .Items import BBCRItem, item_table  # data used below to add items to the World
from .Locations import BBCRLocation, location_table  # same as above
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, MultiWorld, CollectionState
from .Regions import create_regions, connect_entrances
from . import Rules
from ..generic.Rules import set_rule, add_rule, forbid_item


class BBCRWeb(WebWorld):
    theme = "stone"
    option_groups = option_groups_list
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
    web = BBCRWeb()





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
        "Items": {"Quarter", "BSODA", "Zesty Bar", "Baldi's Least Favorite Tape", "Saftey Scissors", "Big 'Ol Boots", "WD-NoSquee", "Alarm Clock", "Principal's Keys", "Swinging Door Lock"},
        "Doors": {"School Faculty Door - South", "School Faculty Door - West by Exit", "School Faculty Door - Center", "School Faculty Door - East Halls",
                                 "School Faculty Door - Connecting Rooms", "School Faculty Door - South East of Cafeteria", "99 Door - Starting Classroom West", "99 Door - Starting Classroom East", "99 Door - Classroom Near Center", "99 Door - Classroom South of Cafeteria", "99 Door - West of Cafeteria",
                     "99 Door - Classroom by East Exit", "99 Door - Classroom in North East Halls", "Yellow Swinging Door - North of Start", "Yellow Swinging Door - West of Start", "Yellow Swinging Door - East of Start", "Yellow Swinging Door - Cafeteria West", "Yellow Swinging Door - Cafeteria East",
                                  "Yellow Swinging Door - Right of Detention", "Yellow Swinging Door - Left of Detention", "Yellow Swinging Door - North-East Halls"},
        "Exits": {"North Exit", "South Exit", "West Exit", "East Exit"},
        "School Faculty Doors": {"School Faculty Door - South", "School Faculty Door - West by Exit", "School Faculty Door - Center", "School Faculty Door - East Halls",
                                 "School Faculty Door - Connecting Rooms", "School Faculty Door - South East of Cafeteria"},
        "99 Doors": {"99 Door - Starting Classroom West", "99 Door - Starting Classroom East", "99 Door - Classroom Near Center", "99 Door - Classroom South of Cafeteria", "99 Door - West of Cafeteria",
                     "99 Door - Classroom by East Exit", "99 Door - Classroom in North East Halls"},
        "Yellow Swinging Doors": {"Yellow Swinging Door - North of Start", "Yellow Swinging Door - West of Start", "Yellow Swinging Door - East of Start", "Yellow Swinging Door - Cafeteria West", "Yellow Swinging Door - Cafeteria East",
                                  "Yellow Swinging Door - Right of Detention", "Yellow Swinging Door - Left of Detention", "Yellow Swinging Door - North-East Halls"},
    }

    location_name_groups = {
        "Notebooks": {"Notebook 1", "Notebook 2", "Notebook 3", "Notebook 4", "Notebook 5", "Notebook 6", "Notebook 7", "Party Mode - Notebook 8", "Party Mode - Notebook 9"},

        "Notebook Questions": {"Notebook 1 Question 1", "Notebook 1 Question 2", "Notebook 1 Question 3", "Notebook 2 Question 1", "Notebook 2 Question 2", "Notebook 2 Question 3",
        "Notebook 3 Question 1", "Notebook 3 Question 2", "Notebook 3 Question 3", "Notebook 4 Question 1", "Notebook 4 Question 2", "Notebook 4 Question 3", "Notebook 5 Question 1",
        "Notebook 5 Question 2", "Notebook 5 Question 3", "Notebook 6 Question 1", "Notebook 6 Question 2", "Notebook 6 Question 3", "Notebook 7 Question 1", "Notebook 7 Question 2",
        "Notebook 7 Question 3", "Notebook 8 Question 1", "Notebook 8 Question 2", "Notebook 8 Question 3", "Notebook 9 Question 1", "Notebook 9 Question 2", "Notebook 9 Question 3"},

        "Items": {"Used Scissors", "Escaped Detention With Keys", "Used Zesty Bar", "Used BSODA", "Used Baldi's Least Favorite Tape", "Used the Yellow Swinging Door Lock",
        "Used the Alarm Clock", "Used the WD-NoSquee", "Used the Big 'Ol Boots", "Used a Quarter"},

        "Classic Mode": {"Classic Mode - Baldi's Quarter Reward", "Classic Mode - Zesty Bar Pickup (School Faculty Room)",
        "Classic Mode - Baldi's Least Favorite Tape Pickup (School Faculty Room)", "Classic Mode - Swinging Door Lock Pickup (School Faculty Room)",
        "Classic Mode - Principal's Keys Pickup (School Faculty Room)", "Classic Mode - WD-NoSquee Pickup (School Faculty Room)", "Classic Mode - Zesty Bar Machine (School Faculty Room)",
        "Classic Mode - Alarm Clock (School Faculty Room)", "Classic Mode - Quarter Pickup (School Faculty Room)", "Classic Mode - BSODA Machine (Halls)",
        "Classic Mode - Quarter Pickup (Halls)", "Classic Mode - Scissors Pickup (Notebook 3 Room)", "Classic Mode - Scissors Pickup (Notebook 4 Room)",
        "Classic Mode - Big 'Ol Boots Pickup (Notebook 5 Room)", "Classic Mode - Scissors Pickup (Notebook 7 Room)", "Classic Mode - WD-NoSquee Pickup (Supply Closet)",
        "Classic Mode - Zesty Bar Pickup (Cafeteria)", "Classic Mode - BSODA Machine (Cafeteria)", "Classic Mode - BSODA Pickup (Cafeteria)"},

        "Party Mode": {"Party Mode - Cafe Present #1", "Party Mode - Cafe Present #2", "Party Mode - South School Faculty Present", "Party Mode - Center School Faculty Present",
        "Party Mode - West School Faculty Present #1", "Party Mode - West School Faculty Present #2", "Party Mode - Notebook 3 Room Present #1", "Party Mode - Notebook 3 Room Present #2",
        "Party Mode - Notebook 4 Room Present", "Party Mode - Notebook 5 Room Present #1", "Party Mode - Notebook 5 Room Present #2", "Party Mode - Notebook 6 Room Present",
        "Party Mode - Notebook 7 Room Present", "Party Mode - Supply Closet Present", "Party Mode - Baldi's Present Reward", "Party Mode - East School Faculty Present",
        "Party Mode - Halls Fun Item Machine", "Party Mode - Cafe Fun Item Machine", "Party Mode - School Faculty Fun Item Machine", "Party Mode - Cafe School Faculty Present #1",
        "Party Mode - Cafe School Faculty Present #2", "Party Mode - Notebook 8", "Party Mode - Notebook 9"},

        "Demo Mode": {"Demo Mode - Baldi's Quarter Reward", "Demo Mode - Item Pickup #1 (East School Faculty Room)", "Demo Mode - Item Pickup #2 (East School Faculty Room)",
        "Demo Mode - Item Pickup #1 (Center School Faculty Room)", "Demo Mode - Item Pickup #2 (Center School Faculty Room)", "Demo Mode - Item Pickup (South School Faculty Room)",
        "Demo Mode - Zesty Bar Machine (School Faculty Room)", "Demo Mode - Item Pickup #1 (Cafe School Faculty Room)", "Demo Mode - Item Pickup #2 (Cafe School Faculty Room)",
        "Demo Mode - BSODA Machine (Halls)", "Demo Mode - Quarter Pickup (Halls)", "Demo Mode - Item Pickup (Notebook 3 Room)", "Demo Mode - Item Pickup (Notebook 4 Room)",
        "Demo Mode - Item Pickup (Notebook 5 Room)", "Demo Mode - Item Pickup #1 (Notebook 7 Room)", "Demo Mode - Item Pickup #2 (Notebook 7 Room)",
        "Demo Mode - Item Pickup #1 (Cafeteria)", "Demo Mode - Item Pickup #2 (Cafeteria)", "Demo Mode - BSODA Machine (Cafeteria)"},

        "99 Doors": {"Passed Through 99 Door - West Starting Class", "Passed Through 99 Door - East Starting Class", "Passed Through 99 Door - Center Middle Class",
        "Passed Through 99 Door - Class North Facing Cafe", "Passed Through 99 Door - Class Facing East Cafe", "Passed Through 99 Door - East Hall Class",
        "Passed Through 99 Door - Class by East Exit"},

        "Yellow Swinging Doors": {"Passed Through Yellow Swinging Door - Left of Detention", "Passed Through Yellow Swinging Door - North-East Halls",
        "Passed Through Yellow Swinging Door - Right of Detention", "Passed Through Yellow Swinging Door - West of Cafe", "Passed Through Yellow Swinging Door - East of Cafe",
        "Passed Through Yellow Swinging Door - North of Start", "Passed Through Yellow Swinging Door - East of Start", "Passed Through Yellow Swinging Door - West of Start"},

        "School Faculty Doors": {"Passed Through School Faculty Door - South", "Passed Through School Faculty Door - Joining Two SF Rooms", "Passed Through School Faculty Door - Near Center",
        "Passed Through School Faculty Door - Near East Exit", "Passed Through School Faculty Door - by Cafe", "Passed Through School Faculty Door - Near West Exit"},

        "Doors": {"Passed Through 99 Door - West Starting Class", "Passed Through 99 Door - East Starting Class", "Passed Through 99 Door - Center Middle Class",
        "Passed Through 99 Door - Class North Facing Cafe", "Passed Through 99 Door - Class Facing East Cafe", "Passed Through 99 Door - East Hall Class",
        "Passed Through 99 Door - Class by East Exit", "Passed Through Yellow Swinging Door - Left of Detention", "Passed Through Yellow Swinging Door - North-East Halls",
        "Passed Through Yellow Swinging Door - Right of Detention", "Passed Through Yellow Swinging Door - West of Cafe", "Passed Through Yellow Swinging Door - East of Cafe",
        "Passed Through Yellow Swinging Door - North of Start", "Passed Through Yellow Swinging Door - East of Start", "Passed Through Yellow Swinging Door - West of Start",
        "Passed Through School Faculty Door - South", "Passed Through School Faculty Door - Joining Two SF Rooms", "Passed Through School Faculty Door - Near Center",
        "Passed Through School Faculty Door - Near East Exit", "Passed Through School Faculty Door - by Cafe", "Passed Through School Faculty Door - Near West Exit",
        "Passed Through Supply Closet Door"},

        "Exits": {"Activated East Exit", "Activated West Exit", "Activated South Exit", "Activated North Exit"},
    }


    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.unplaced_items: int = 0



    def create_regions(self):
        create_regions(self)

        if self.options.req_style == 1:
            if self.options.party == 0:
                raise OptionError("I really doubt that you would want to try to beat Party Style when you don't even have it randomized.")

        if self.options.which_style == 1:
            if self.options.party == 0:
                raise OptionError("I can't give you the style of the game you haven't randomized. In this case, it's Party. please change it")

        if self.options.req_style == 2:
            if self.options.demo == 0:
                raise OptionError("I really doubt that you would want to try to beat Demo Style when you don't even have it randomized.")

        if self.options.which_style == 2:
            if self.options.demo == 0:
                raise OptionError("I can't give you the style of the game you haven't randomized. In this case, it's Demo. please change it")



        if self.options.req_style == 0:
            if not self.options.doorsanity:
                self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Exit", "Region", self.player) and state.has("Notebook", self.player, 7) and state.has("Classic Style", self.player)
            elif self.options.doorsanity:
                self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Exit", "Region", self.player) and state.has("Notebook",
                            self.player, 7) and state.has("East Exit", self.player) and state.has("West Exit", self.player) and state.has("South Exit", self.player) and state.has("North Exit",
                            self.player) and state.has("Classic Style", self.player) and state.can_reach("Cafeteria", "Region", self.player)
        elif self.options.req_style == 1:
            if not self.options.doorsanity:
                self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Exit", "Region", self.player) and state.has("Notebook", self.player, 7) and state.has("Party Style", self.player) and state.has("Purple Baldi (Party Style)", self.player) and state.has("Blue Baldi (Party Style)",
                            self.player) and state.has("Orange Baldi (Party Style)", self.player) and state.has("Green Baldi (Party Style)", self.player)
            elif self.options.doorsanity:
                self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Exit", "Region", self.player) and state.has("Notebook",
                            self.player, 7) and state.has("East Exit", self.player) and state.has("West Exit", self.player) and state.has("South Exit", self.player) and state.has("North Exit",
                            self.player) and state.has("Party Style", self.player) and state.can_reach("Cafeteria", "Region", self.player) and state.has("Purple Baldi (Party Style)", self.player) and state.has("Blue Baldi (Party Style)",
                            self.player) and state.has("Orange Baldi (Party Style)", self.player) and state.has("Green Baldi (Party Style)", self.player)
        elif self.options.req_style == 2:
            if not self.options.doorsanity:
                self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Exit", "Region", self.player) and state.has("Notebook", self.player, 7) and state.has("Demo Style", self.player)
            elif self.options.doorsanity:
                self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Exit", "Region", self.player) and state.has("Notebook",
                            self.player, 7) and state.has("East Exit", self.player) and state.has("West Exit", self.player) and state.has("South Exit", self.player) and state.has("North Exit",
                            self.player) and state.has("Demo Style", self.player) and state.can_reach("Cafeteria", "Region", self.player)



    def create_item(self, name: str) -> "Item":
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self):
        starting_pool = len(self.multiworld.itempool)
        # print(str(self.options.required_route))
        starting_locations = len(self.multiworld.get_unfilled_locations(self.player))

        totalItems = len(self.multiworld.get_unfilled_locations(self.player))
        self.unplaced_items = totalItems
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

        # print(totalItems)

        if not self.options.item_usage:
            for _ in range(NotebookNumber):
                self.multiworld.itempool.append(Item("Notebook", ItemClassification.progression, self.item_name_to_id["Notebook"], self.player))
                totalItems -= 1
                NotebookNumber -= 1
                # print(totalItems)
                # print("Notebooks" + str(NotebookNumber))

            for _ in range(BSODANumber):
                self.multiworld.itempool.append(Item("BSODA", ItemClassification.useful, self.item_name_to_id["BSODA"], self.player))
                BSODANumber -= 1
                totalItems -= 1
                # print(totalItems)
                # print("BSODAS" + str(BSODANumber))

            self.multiworld.itempool.append(Item("Baldi's Least Favorite Tape", ItemClassification.useful, self.item_name_to_id["Baldi's Least Favorite Tape"], self.player))
            totalItems -= 1
            # print(totalItems)
            # print("Unfortunately, Baldi's Least Favorite Tape was added to the itempool")

            for _ in range(ScissorsNumber):
                self.multiworld.itempool.append(Item("Safety Scissors", ItemClassification.useful, self.item_name_to_id["Safety Scissors"], self.player))
                totalItems -= 1
                ScissorsNumber -= 1
                # print(totalItems)
                # print("Scissors for safety" + str(ScissorsNumber))

            for _ in range(ZestyNumber):
                self.multiworld.itempool.append(Item("Zesty Bar", ItemClassification.useful, self.item_name_to_id["Zesty Bar"], self.player))
                totalItems -= 1
                ZestyNumber -= 1
                # print(totalItems)
                # print("Zesty Bars" + str(ZestyNumber))

            for _ in range(SwingDoorLockNum):
                self.multiworld.itempool.append(Item("Swinging Door Lock", ItemClassification.useful, self.item_name_to_id["Swinging Door Lock"], self.player))
                totalItems -= 1
                SwingDoorLockNum -= 1
                # print(totalItems)
                # print("Swinging Door Lock" + str(SwingDoorLockNum))

            for _ in range(PKeysNumber):
                self.multiworld.itempool.append(Item("Principal's Keys", ItemClassification.useful, self.item_name_to_id["Principal's Keys"], self.player))
                totalItems -= 1
                PKeysNumber -= 1
                # print(totalItems)
                # print("Principal's Keys" + str(PKeysNumber))

            for _ in range(WDNoSqNumber):
                self.multiworld.itempool.append(Item("WD-NoSquee", ItemClassification.useful, self.item_name_to_id["WD-NoSquee"], self.player))
                totalItems -= 1
                WDNoSqNumber -= 1
                # print(totalItems)
                # print("WD-NoSquee" + str(WDNoSqNumber))

            for _ in range(ACNumber):
                self.multiworld.itempool.append(Item("Alarm Clock", ItemClassification.useful, self.item_name_to_id["Alarm Clock"], self.player))
                totalItems -= 1
                ACNumber -= 1
                # print(totalItems)
                # print("Alarm Clock" + str(ACNumber))

            for _ in range(BigBootNumber):
                self.multiworld.itempool.append(Item("Big 'Ol Boots", ItemClassification.useful, self.item_name_to_id["Big 'Ol Boots"], self.player))
                totalItems -= 1
                BigBootNumber -= 1
                # print(totalItems)
                # print("Big 'Ol Boots" + str(BigBootNumber))

            for _ in range(QuarterNumber):
                self.multiworld.itempool.append(Item("Quarter", ItemClassification.progression, self.item_name_to_id["Quarter"], self.player))
                totalItems -= 1
                # print("Quarter")
                # print(totalItems)
        else:
            for _ in range(NotebookNumber):
                self.multiworld.itempool.append(
                    Item("Notebook", ItemClassification.progression, self.item_name_to_id["Notebook"], self.player))
                totalItems -= 1
                NotebookNumber -= 1
                # print(totalItems)
                # print("Notebooks" + str(NotebookNumber))

            for _ in range(BSODANumber):
                self.multiworld.itempool.append(
                    Item("BSODA", ItemClassification.progression, self.item_name_to_id["BSODA"], self.player))
                BSODANumber -= 1
                totalItems -= 1
                # print(totalItems)
                # print("BSODAS" + str(BSODANumber))

            self.multiworld.itempool.append(Item("Baldi's Least Favorite Tape", ItemClassification.progression,
                                                 self.item_name_to_id["Baldi's Least Favorite Tape"], self.player))
            totalItems -= 1
            # print(totalItems)
            # print("Unfortunately, Baldi's Least Favorite Tape was added to the itempool")

            for _ in range(ScissorsNumber):
                self.multiworld.itempool.append(Item("Safety Scissors", ItemClassification.progression, self.item_name_to_id["Safety Scissors"], self.player))
                totalItems -= 1
                ScissorsNumber -= 1
                # print(totalItems)
                # print("Scissors for safety" + str(ScissorsNumber))

            for _ in range(ZestyNumber):
                self.multiworld.itempool.append(
                    Item("Zesty Bar", ItemClassification.progression, self.item_name_to_id["Zesty Bar"], self.player))
                totalItems -= 1
                ZestyNumber -= 1
                # print(totalItems)
                # print("Zesty Bars" + str(ZestyNumber))

            for _ in range(SwingDoorLockNum):
                self.multiworld.itempool.append(
                    Item("Swinging Door Lock", ItemClassification.progression, self.item_name_to_id["Swinging Door Lock"],
                         self.player))
                totalItems -= 1
                SwingDoorLockNum -= 1
                # print(totalItems)
                # print("Swinging Door Lock" + str(SwingDoorLockNum))

            for _ in range(PKeysNumber):
                self.multiworld.itempool.append(
                    Item("Principal's Keys", ItemClassification.progression, self.item_name_to_id["Principal's Keys"],
                         self.player))
                totalItems -= 1
                PKeysNumber -= 1
                # print(totalItems)
                # print("Principal's Keys" + str(PKeysNumber))

            for _ in range(WDNoSqNumber):
                self.multiworld.itempool.append(
                    Item("WD-NoSquee", ItemClassification.progression, self.item_name_to_id["WD-NoSquee"], self.player))
                totalItems -= 1
                WDNoSqNumber -= 1
                # print(totalItems)
                # print("WD-NoSquee" + str(WDNoSqNumber))

            for _ in range(ACNumber):
                self.multiworld.itempool.append(
                    Item("Alarm Clock", ItemClassification.progression, self.item_name_to_id["Alarm Clock"], self.player))
                totalItems -= 1
                ACNumber -= 1
                # print(totalItems)
                # print("Alarm Clock" + str(ACNumber))

            for _ in range(BigBootNumber):
                self.multiworld.itempool.append(
                    Item("Big 'Ol Boots", ItemClassification.progression, self.item_name_to_id["Big 'Ol Boots"],
                         self.player))
                totalItems -= 1
                BigBootNumber -= 1
                # print(totalItems)
                # print("Big 'Ol Boots" + str(BigBootNumber))

            for _ in range(QuarterNumber):
                self.multiworld.itempool.append(
                    Item("Quarter", ItemClassification.progression, self.item_name_to_id["Quarter"], self.player))
                totalItems -= 1
                # print("Quarter")
                # print(totalItems)

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
            # print("Yellow Doors" + str(totalItems))

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
            # print("99 Door" + str(totalItems))

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
            # print("School Faculty Door" + str(totalItems))

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
            # print("Exit" + str(totalItems))

        if self.options.party:
            self.multiworld.itempool.append(Item("Purple Baldi (Party Style)", ItemClassification.progression, self.item_name_to_id["Purple Baldi (Party Style)"], self.player))
            self.multiworld.itempool.append(Item("Orange Baldi (Party Style)", ItemClassification.progression, self.item_name_to_id["Orange Baldi (Party Style)"], self.player))
            self.multiworld.itempool.append(Item("Green Baldi (Party Style)", ItemClassification.progression, self.item_name_to_id["Green Baldi (Party Style)"], self.player))
            self.multiworld.itempool.append(Item("Blue Baldi (Party Style)", ItemClassification.progression, self.item_name_to_id["Blue Baldi (Party Style)"], self.player))
            totalItems -= 4
            if self.options.which_style != 1:
                self.multiworld.itempool.append(Item("Party Style", ItemClassification.progression, self.item_name_to_id["Party Style"], self.player))
                # print("Party Style to multi")
                totalItems -= 1
            else:
                self.multiworld.push_precollected(self.create_item("Party Style"))
                # print("party style to precollected")
        else:
            if self.options.which_style == 1:
                print("Party Style isn't randomized. Giving " + str(self.player_name) + " Classic Style Instead.")
                self.multiworld.push_precollected(self.create_item("Classic Style"))

        if self.options.demo:
            if self.options.which_style != 2:
                self.multiworld.itempool.append(Item("Demo Style", ItemClassification.progression, self.item_name_to_id["Demo Style"], self.player))
                # print("Demo Style to multi")
                totalItems -= 1
            else:
                self.multiworld.push_precollected(self.create_item("Demo Style"))
                # print("demo style to precollected")
        else:
            if self.options.which_style == 1:
                print("Demo Style isn't randomized. Giving " + str(self.player_name) + " Classic Style Instead.")
                self.multiworld.push_precollected(self.create_item("Classic Style"))

        if self.options.demo == 1 or self.options.party == 1:
            if self.options.party == 0 and self.options.which_style == 1:
                # print("nothing to do here")
                self.random.randint(1,2)
            elif self.options.demo == 0 and self.options.which_style == 2:
                # print("nothing to do here")
                self.random.randint(1, 2)
            else:
                if self.options.which_style == 0:
                    self.multiworld.push_precollected(self.create_item("Classic Style"))
                else:
                    self.multiworld.itempool.append(Item("Classic Style", ItemClassification.progression, self.item_name_to_id["Classic Style"], self.player))
                    totalItems -= 1
        if self.options.demo == 0 and self.options.party == 0:
            self.multiworld.push_precollected(self.create_item("Classic Style"))


        if totalItems >= 1:
            # print("i have " + str(totalItems) + " items, so I'm gonna fill some stuff.")
            self.multiworld.itempool.append(Item("Quarter", ItemClassification.progression, self.item_name_to_id["Quarter"], self.player))
            totalItems -= 1
            # print("Quarter")
            # print(totalItems)
            # print(totalItems * (trap_amount / 100))
            trap_amount = round(totalItems * (trap_amount / 100))
            trap_amount -= 2
            # print(trap_amount)

            if totalItems >= 1:
                if self.options.funny_traps:
                    for _ in range(trap_amount):
                        if totalItems >= 1:
                            trap_choose = self.random.randint(1, 3)
                            if trap_choose == 1:
                                self.multiworld.itempool.append(Item("Jump Rope Time (Trap)", ItemClassification.trap, self.item_name_to_id["Jump Rope Time (Trap)"], self.player))
                            elif trap_choose == 2:
                                self.multiworld.itempool.append(Item("The Arts and Crafters Effect (Trap)", ItemClassification.trap, self.item_name_to_id["The Arts and Crafters Effect (Trap)"], self.player))
                            elif trap_choose == 3:
                                self.multiworld.itempool.append(Item("Detention For You. (When Will You Learn?) (Trap)", ItemClassification.trap, self.item_name_to_id["Detention For You. (When Will You Learn?) (Trap)"], self.player))
                            totalItems -= 1
                            # print("Trap")
                            # print(totalItems)

        if totalItems >= 1:
            filler_num = totalItems
            filler_num -= 0
            for _ in range(filler_num):
                item_to_gen = self.random.randint(1, 12)
                # print("item number" + str(item_to_gen))
                if item_to_gen == 1 or item_to_gen >= 10:
                    if self.options.item_usage:
                        self.multiworld.itempool.append(
                            Item("BSODA", ItemClassification.progression, self.item_name_to_id["BSODA"], self.player))
                    else:
                        self.multiworld.itempool.append(
                            Item("BSODA", ItemClassification.useful, self.item_name_to_id["BSODA"], self.player))
                elif item_to_gen == 2:
                    if self.options.item_usage:
                        self.multiworld.itempool.append(Item("Baldi's Least Favorite Tape", ItemClassification.progression, self.item_name_to_id["Baldi's Least Favorite Tape"], self.player))
                    else:
                        self.multiworld.itempool.append(Item("Baldi's Least Favorite Tape", ItemClassification.useful,
                                                             self.item_name_to_id["Baldi's Least Favorite Tape"],
                                                             self.player))
                elif item_to_gen == 3:
                    if self.options.item_usage:
                        self.multiworld.itempool.append(Item("Safety Scissors", ItemClassification.progression, self.item_name_to_id["Safety Scissors"], self.player))
                    elif not self.options.item_usage:
                        self.multiworld.itempool.append(Item("Safety Scissors", ItemClassification.useful, self.item_name_to_id["Safety Scissors"], self.player))
                elif item_to_gen == 4:
                    if self.options.item_usage:
                        self.multiworld.itempool.append(
                            Item("Zesty Bar", ItemClassification.progression, self.item_name_to_id["Zesty Bar"],
                                 self.player))
                    else:
                        self.multiworld.itempool.append(
                            Item("Zesty Bar", ItemClassification.useful, self.item_name_to_id["Zesty Bar"],
                                 self.player))
                elif item_to_gen == 5:
                    if self.options.item_usage:
                        self.multiworld.itempool.append(Item("Swinging Door Lock", ItemClassification.progression,
                                                             self.item_name_to_id["Swinging Door Lock"], self.player))
                    else:
                        self.multiworld.itempool.append(Item("Swinging Door Lock", ItemClassification.useful,
                                                             self.item_name_to_id["Swinging Door Lock"], self.player))
                elif item_to_gen == 6:
                    if self.options.item_usage:
                        self.multiworld.itempool.append(Item("Principal's Keys", ItemClassification.progression,
                                                             self.item_name_to_id["Principal's Keys"], self.player))
                    else:
                        self.multiworld.itempool.append(Item("Principal's Keys", ItemClassification.useful,
                                                             self.item_name_to_id["Principal's Keys"], self.player))
                elif item_to_gen == 7:
                    if self.options.item_usage:
                        self.multiworld.itempool.append(
                            Item("WD-NoSquee", ItemClassification.progression, self.item_name_to_id["WD-NoSquee"],
                                 self.player))
                    else:
                        self.multiworld.itempool.append(
                            Item("WD-NoSquee", ItemClassification.useful, self.item_name_to_id["WD-NoSquee"],
                                 self.player))
                elif item_to_gen == 8:
                    if self.options.item_usage:
                        self.multiworld.itempool.append(
                            Item("Alarm Clock", ItemClassification.progression, self.item_name_to_id["Alarm Clock"],
                                 self.player))
                    else:
                        self.multiworld.itempool.append(
                            Item("Alarm Clock", ItemClassification.useful, self.item_name_to_id["Alarm Clock"],
                                 self.player))
                elif item_to_gen == 9:
                    if self.options.item_usage:
                        self.multiworld.itempool.append(
                            Item("Big 'Ol Boots", ItemClassification.progression, self.item_name_to_id["Big 'Ol Boots"],
                                 self.player))
                    else:
                        self.multiworld.itempool.append(
                            Item("Big 'Ol Boots", ItemClassification.useful, self.item_name_to_id["Big 'Ol Boots"],
                                 self.player))
                totalItems -= 1
                # print(totalItems)


        actual_added = len(self.multiworld.itempool) - starting_pool

        # print("Locations:", starting_locations)
        # print("Added:", actual_added)
        # print("Difference:", actual_added - starting_locations)
        #
        # print(len(self.multiworld.itempool))
        # print(totalItems)

        empty_variable = 1
        while empty_variable != 18:
            # print(str(self.location_id_to_name[8 + empty_variable]))
            add_rule(self.get_location(str(self.location_id_to_name[8 + empty_variable])),
                     lambda state: state.has("Classic Style", self.player, 1))
            # print(str(self.location_id_to_name[8 + empty_variable]) + " is now locked behind classic")
            empty_variable += 1

        if self.options.party:
            empty_variable = 1
            while empty_variable != 22:
                # print(str(self.location_id_to_name[83 + empty_variable]))
                if empty_variable + 83 != 98:
                    add_rule(self.get_location(str(self.location_id_to_name[83 + empty_variable])),
                             lambda state: state.has("Party Style", self.player, 1))
                # print(str(self.location_id_to_name[83 + empty_variable]) + " is now locked behind party")
                empty_variable += 1

        if self.options.demo:
            empty_variable = 2
            while empty_variable != 20:
                # print(str(self.location_id_to_name[104 + empty_variable]))
                add_rule(self.get_location(str(self.location_id_to_name[104 + empty_variable])),
                         lambda state: state.has("Demo Style", self.player, 1))
                # print(str(self.location_id_to_name[104 + empty_variable]) + " is now locked behind demo")
                empty_variable += 1

        bsoda1 = self.get_location("Classic Mode - BSODA Machine (Cafeteria)")
        add_rule(bsoda1, lambda state: state.has("Quarter", self.player, 2))

        bsoda2 = self.get_location("Classic Mode - BSODA Machine (Halls)")
        add_rule(bsoda2, lambda state: state.has("Quarter", self.player, 2))

        zesty1 = self.get_location("Classic Mode - Zesty Bar Machine (School Faculty Room)")
        add_rule(zesty1, lambda state: state.has("Quarter", self.player, 2))

        # quarter reward
        if self.options.required_route != 1:
            quarter = self.get_location("Classic Mode - Baldi's Quarter Reward")
            add_rule(quarter, lambda state: state.has("Notebook", self.player, 1) and state.has("Classic Style", self.player, 1))
            if self.options.demo:
                add_rule(self.get_location("Demo Mode - Baldi's Quarter Reward"), lambda state: state.has("Notebook", self.player, 1) and state.has("Demo Style", self.player, 1))
            if self.options.party:
                add_rule(self.get_location("Party Mode - Baldi's Present Reward"), lambda state: state.has("Notebook", self.player, 1) and state.has("Party Style", self.player, 1))

        # item usage
        if self.options.item_usage:
            quarter_use = self.get_location("Used a Quarter")
            add_rule(quarter_use, lambda state: state.has("Quarter", self.player, 1))

            scissor_use = self.get_location("Used Scissors")
            add_rule(scissor_use, lambda state: state.has("Safety Scissors", self.player, 1))

            keys_use = self.get_location("Escaped Detention With Keys")
            add_rule(keys_use, lambda state: state.has("Principal's Keys", self.player, 1))

            tape_use = self.get_location("Used Baldi's Least Favorite Tape")
            add_rule(tape_use, lambda state: state.has("Baldi's Least Favorite Tape", self.player, 1))

            bar_use = self.get_location("Used Zesty Bar")
            add_rule(bar_use, lambda state: state.has("Zesty Bar", self.player, 1))

            soda_use = self.get_location("Used BSODA")
            add_rule(soda_use, lambda state: state.has("BSODA", self.player, 1))

            boot_use = self.get_location("Used the Big 'Ol Boots")
            add_rule(boot_use, lambda state: state.has("Big 'Ol Boots", self.player, 1))

            wd_use = self.get_location("Used the WD-NoSquee")
            add_rule(wd_use, lambda state: state.has("WD-NoSquee", self.player, 1))

            lock_use = self.get_location("Used the Yellow Swinging Door Lock")
            add_rule(lock_use, lambda state: state.has("Swinging Door Lock", self.player, 1))

            clock_use = self.get_location("Used the Alarm Clock")
            add_rule(clock_use, lambda state: state.has("Alarm Clock", self.player, 1))

            if self.options.itemitem:
                bupp = 71
                while bupp != 81:
                    location = self.get_location(str(self.location_id_to_name[bupp]))
                    if bupp == 71:
                        item = "Safety Scissors"
                    elif bupp == 72:
                        item = "Principal's Keys"
                    elif bupp == 73:
                        item = "Zesty Bar"
                    elif bupp == 74:
                        item = "BSODA"
                    elif bupp == 75:
                        item = "Baldi's Least Favorite Tape"
                    elif bupp == 76:
                        item = "Swinging Door Lock"
                    elif bupp == 77:
                        item = "Alarm Clock"
                    elif bupp == 78:
                        item = "WD-NoSquee"
                    elif bupp == 79:
                        item = "Big 'Ol Boots"
                    elif bupp == 80:
                        item = "Quarter"
                    forbid_item(location, item, player=self.player),
                    bupp += 1
                    print("Blocked " + str(item) + " from being at " + str(location))



    def connect_entrances(self) -> None:
        connect_entrances(self)



        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_BBCR_world.puml", show_entrance_names=True, regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[self.player])

    def generate_basic(self) -> None:
        # state: CollectionState = self.multiworld.get_all_state()
        # state.update_reachable_regions(self.player)
        # reachable_regions: set[Region] = set(state.reachable_regions[self.player])
        # unreachable_regions: set[Region] = set()  # type: ignore
        # for region in self.multiworld.regions:
        #     if region not in reachable_regions:
        #         unreachable_regions.add(region)
        # visualize_regions(root_region=self.get_region(region_name="Menu"), file_name=f"{self.player_name}_world.puml",
        #                   show_entrance_names=True, regions_to_highlight=unreachable_regions)

        return super().generate_basic()

    def fill_slot_data(self) -> dict[str, any]:
        # In order for our game client to handle the generated seed correctly we need to know what the user selected
        # for their difficulty and final boss HP.
        # A dictionary returned from this method gets set as the slot_data and will be sent to the client after connecting.
        # The options dataclass has a method to return a `Dict[str, Any]` of each option name provided and the relevant
        # option's value.
        names = ["required_route", "notechecks", "doorsanity", "death_link", "req_style", "party", "demo"]
        return self.options.as_dict(*names)


    def generate_output(self, output_directory: str) -> None:
        ConnectInf ="""ip=archipelago.gg
port=[port number]
slot=""" + self.player_name + """
pass=[password. remove brackets if none]"""
        # print(ConnectInf)

        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.aptxt"
        with open(os.path.join(output_directory, filename), 'w') as f:
            f.write(ConnectInf)