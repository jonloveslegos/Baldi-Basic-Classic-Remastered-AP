from BaseClasses import Location


class BBCRLocation(Location):
    game: str = "Baldis Basics Classic Remastered"

location_table = {
    "Notebook 1": 1,
    "Notebook 2": 2,
    "Notebook 3": 3,
    "Notebook 4": 4,
    "Notebook 5": 5,
    "Notebook 6": 6,
    "Notebook 7": 7,

    "Classic Mode - Baldi's Quarter Reward": 8,

    "Classic Mode - Zesty Bar Pickup (School Faculty Room)": 9,
    "Classic Mode - Baldi's Least Favorite Tape Pickup (School Faculty Room)": 10,
    "Classic Mode - Swinging Door Lock Pickup (School Faculty Room)": 11,
    "Classic Mode - Principal's Keys Pickup (School Faculty Room)": 12,
    "Classic Mode - WD-NoSquee Pickup (School Faculty Room)": 13,
    "Classic Mode - Zesty Bar Machine (School Faculty Room)": 14,
    "Classic Mode - Alarm Clock (School Faculty Room)": 15,
    "Classic Mode - Quarter Pickup (School Faculty Room)": 16,


    "Classic Mode - BSODA Machine (Halls)": 17,
    "Classic Mode - Quarter Pickup (Halls)": 18,

    "Classic Mode - Scissors Pickup (Notebook 3 Room)": 19,
    "Classic Mode - Scissors Pickup (Notebook 4 Room)": 20,
    "Classic Mode - Big 'Ol Boots Pickup (Notebook 5 Room)": 21,
    "Classic Mode - Scissors Pickup (Notebook 7 Room)": 22,

    "Classic Mode - WD-NoSquee Pickup (Supply Closet)": 23,

    "Classic Mode - Zesty Bar Pickup (Cafeteria)": 24,
    "Classic Mode - BSODA Machine (Cafeteria)": 25,
    "Classic Mode - BSODA Pickup (Cafeteria)": 26,

    "Notebook 1 Question 1": 27,
    "Notebook 1 Question 2": 28,
    "Notebook 1 Question 3": 29,

    "Notebook 2 Question 1": 30,
    "Notebook 2 Question 2": 31,
    "Notebook 2 Question 3": 32,

    "Notebook 3 Question 1": 33,
    "Notebook 3 Question 2": 34,
    "Notebook 3 Question 3": 35,

    "Notebook 4 Question 1": 36,
    "Notebook 4 Question 2": 37,
    "Notebook 4 Question 3": 38,

    "Notebook 5 Question 1": 39,
    "Notebook 5 Question 2": 40,
    "Notebook 5 Question 3": 41,

    "Notebook 6 Question 1": 42,
    "Notebook 6 Question 2": 43,
    "Notebook 6 Question 3": 44,

    "Notebook 7 Question 1": 45,
    "Notebook 7 Question 2": 46,
    "Notebook 7 Question 3": 47,

    "Passed Through Yellow Swinging Door - West of Start": 48,
    "Passed Through Yellow Swinging Door - East of Start": 49,
    "Passed Through Yellow Swinging Door - North of Start": 50,

    "Passed Through Yellow Swinging Door - East of Cafe": 51,
    "Passed Through Yellow Swinging Door - West of Cafe": 52,

    "Passed Through Yellow Swinging Door - Right of Detention": 53,

    "Activated East Exit": 54,
    "Activated West Exit": 55,
    "Activated North Exit": 56,
    "Activated South Exit": 57,

    "Passed Through 99 Door - West Starting Class": 58,
    "Passed Through 99 Door - East Starting Class": 59,
    "Passed Through 99 Door - Center Middle Class": 60,
    "Passed Through 99 Door - Class North Facing Cafe": 61,
    "Passed Through 99 Door - Class Facing East Cafe": 62,
    "Passed Through 99 Door - East Hall Class": 63,
    "Passed Through 99 Door - Class by East Exit": 64,

    "Passed Through School Faculty Door - South": 65,
    "Passed Through School Faculty Door - Joining Two SF Rooms": 66,
    "Passed Through School Faculty Door - Near Center": 67,
    "Passed Through School Faculty Door - Near East Exit": 68,
    "Passed Through School Faculty Door - by Cafe": 69,
    "Passed Through School Faculty Door - Near West Exit": 70,

    "Used Scissors": 71,
    "Escaped Detention With Keys": 72,
    "Used Zesty Bar": 73,
    "Used BSODA": 74,
    "Used Baldi's Least Favorite Tape": 75,
    "Used the Yellow Swinging Door Lock": 76,
    "Used the Alarm Clock": 77,
    "Used the WD-NoSquee": 78,
    "Used the Big 'Ol Boots": 79,
    "Used a Quarter": 80,

    "Passed Through Yellow Swinging Door - Left of Detention": 81,
    "Passed Through Yellow Swinging Door - North-East Halls": 82,
    "Passed Through Supply Closet Door": 83,

    "Party Mode - Cafe Present #1": 84,
    "Party Mode - Cafe Present #2": 85,

    "Party Mode - South School Faculty Present": 86,

    "Party Mode - Center School Faculty Present": 87,

    "Party Mode - West School Faculty Present #1": 88,
    "Party Mode - West School Faculty Present #2": 89,

    "Party Mode - Notebook 3 Room Present #1": 90,
    "Party Mode - Notebook 3 Room Present #2": 91,
    "Party Mode - Notebook 4 Room Present": 92,
    "Party Mode - Notebook 5 Room Present #1": 93,
    "Party Mode - Notebook 5 Room Present #2": 94,
    "Party Mode - Notebook 6 Room Present": 95,
    "Party Mode - Notebook 7 Room Present": 96,

    "Party Mode - Supply Closet Present": 97,

    "Party Mode - Baldi's Present Reward": 98,

    "Party Mode - East School Faculty Present": 99,

    "Party Mode - Halls Fun Item Machine": 100,
    "Party Mode - Cafe Fun Item Machine": 101,
    "Party Mode - School Faculty Fun Item Machine": 102,

    "Party Mode - Cafe School Faculty Present #1": 103,
    "Party Mode - Cafe School Faculty Present #2": 104,


    "Demo Mode - Baldi's Quarter Reward": 105,

    "Demo Mode - Item Pickup #1 (East School Faculty Room)": 106,
    "Demo Mode - Item Pickup #2 (East School Faculty Room)": 107,
    "Demo Mode - Item Pickup #1 (Center School Faculty Room)": 108,
    "Demo Mode - Item Pickup #2 (Center School Faculty Room)": 109,
    "Demo Mode - Item Pickup (South School Faculty Room)": 110,
    "Demo Mode - Zesty Bar Machine (School Faculty Room)": 111,
    "Demo Mode - Item Pickup #1 (Cafe School Faculty Room)": 112,
    "Demo Mode - Item Pickup #2 (Cafe School Faculty Room)": 113,


    "Demo Mode - BSODA Machine (Halls)": 114,
    "Demo Mode - Quarter Pickup (Halls)": 115,

    "Demo Mode - Item Pickup (Notebook 3 Room)": 116,
    "Demo Mode - Item Pickup (Notebook 4 Room)": 117,
    "Demo Mode - Item Pickup (Notebook 5 Room)": 118,
    "Demo Mode - Item Pickup #1 (Notebook 7 Room)": 119,
    "Demo Mode - Item Pickup #2 (Notebook 7 Room)": 120,

    "Demo Mode - Item Pickup #1 (Cafeteria)": 121,
    "Demo Mode - Item Pickup #2 (Cafeteria)": 122,
    "Demo Mode - BSODA Machine (Cafeteria)": 123,




}