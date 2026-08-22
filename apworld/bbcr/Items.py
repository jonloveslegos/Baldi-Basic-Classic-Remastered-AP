from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification\

if TYPE_CHECKING:
    from . import BBCRWorld


class BBCRItem(Item):
    game: str = "Baldis Basics Classic Remastered"
    type: str
    
item_table = {
    "Notebook": 1,
    "Quarter": 2,
    "BSODA": 3,
    "Zesty Bar": 4,
    "Baldi's Least Favorite Tape": 5,
    "Safety Scissors": 6,
    "Big 'Ol Boots": 7,
    "WD-NoSquee": 8,
    "Alarm Clock": 9,
    "Principal's Keys": 10,
    "Swinging Door Lock": 11,

    "Jump Rope Time (Trap)": 12,
    "The Arts and Crafters Effect (Trap)": 13,
    "Detention For You. (When Will You Learn?) (Trap)": 14,

    "Yellow Swinging Door - North of Start": 15,
    "Yellow Swinging Door - West of Start": 16,
    "Yellow Swinging Door - East of Start": 17,
    "Yellow Swinging Door - Cafeteria West": 18,
    "Yellow Swinging Door - Cafeteria East": 19,
    "Yellow Swinging Door - Right of Detention": 20,

    "99 Door - Starting Classroom West": 21,
    "99 Door - Starting Classroom East": 22,
    "99 Door - Classroom Near Center": 23,
    "99 Door - Classroom South of Cafeteria": 24,
    "99 Door - Classroom West of Cafeteria": 25,
    "99 Door - Classroom by East Exit": 26,
    "99 Door - Classroom in North East Halls": 27,

    "Supply Closet Door": 28,

    "School Faculty Door - South": 29,
    "School Faculty Door - West by Exit": 30,
    "School Faculty Door - Center": 31,
    "School Faculty Door - Connecting Rooms": 32,
    "School Faculty Door - East Halls": 33,
    "School Faculty Door - South East of Cafeteria": 34,

    "East Exit": 35,
    "South Exit": 36,
    "West Exit": 37,
    "North Exit": 38,

    "Yellow Swinging Door - North-East Halls": 39,
    "Yellow Swinging Door - Left of Detention": 40,

    "Purple Baldi (Party Style)": 41,
    "Blue Baldi (Party Style)": 42,
    "Green Baldi (Party Style)": 43,
    "Orange Baldi (Party Style)": 44,

    "Party Style": 45,
    "Demo Style": 46,
    "Classic Style": 47,

    "Classic Style Notebook": 48,
    "Party Style Notebook": 49,
    "Demo Style Notebook": 50,

    "Random Event (Trap)": 51,
}

def create_items_and_append(world: "BBCRWorld", name: str, classification: ItemClassification, amount: int = 1) -> None:
    for _ in range(amount):
        world.multiworld.itempool.append(Item(name=name, code=world.item_name_to_id[name], classification=classification, player=world.player))
        world.unplaced_items -= 1