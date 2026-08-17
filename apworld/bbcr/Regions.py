from BaseClasses import Location, LocationProgressType
from typing import Optional
from BaseClasses import Region, Entrance
from .Locations import BBCRLocation, location_table
from ..generic.Rules import add_rule


def create_regions(world):
    player = world.player
    multiworld = world.multiworld
    regmen = Region("Menu", player, multiworld, "Menu")
    multiworld.regions.append(regmen)

    regui = Region("UI", player, multiworld, "UI")
    locui_names = []
    regui.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regui) for loc_name in locui_names]
    multiworld.regions.append(regui)


    #regions for the halls
    regstart = Region("Starting Halls", player, multiworld, "Starting Halls")
    locstart_names = []
    if world.options.required_route != 1:
        locstart_names.append("Classic Mode - Baldi's Quarter Reward")
    if world.options.party:
        if world.options.required_route != 1:
            locstart_names.append("Party Mode - Baldi's Present Reward")
    if world.options.demo:
        if world.options.required_route != 1:
            locstart_names.append("Demo Mode - Baldi's Quarter Reward")
    if world.options.item_usage == 1:
        locstart_names.append("Used Zesty Bar")
        locstart_names.append("Used BSODA")
        locstart_names.append("Used the Yellow Swinging Door Lock")
        locstart_names.append("Used the Alarm Clock")
        locstart_names.append("Used the WD-NoSquee")
        locstart_names.append("Used the Big 'Ol Boots")
    regstart.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regstart) for loc_name in locstart_names]
    multiworld.regions.append(regstart)

    reghalls = Region("Halls", player, multiworld, "Halls")
    lochalls_names = ["Classic Mode - BSODA Machine (Halls)", "Classic Mode - Quarter Pickup (Halls)"]
    if world.options.party:
        lochalls_names.append("Party Mode - Halls Fun Item Machine")
    if world.options.demo:
        lochalls_names.append("Demo Mode - BSODA Machine (Halls)")
        lochalls_names.append("Demo Mode - Quarter Pickup (Halls)")
    if world.options.item_usage == 1:
        lochalls_names.append("Used Scissors")
        lochalls_names.append("Escaped Detention With Keys")
        lochalls_names.append("Used Baldi's Least Favorite Tape")
        lochalls_names.append("Used a Quarter")
    reghalls.locations += [BBCRLocation(player, loc_name, location_table[loc_name], reghalls) for loc_name in lochalls_names]
    multiworld.regions.append(reghalls)


    #regions for the notebook rooms
    regnote1 = Region("Notebook 1 Room", player, multiworld, "Notebook 1 Room")
    locnote1_names = ["Notebook 1"]
    regnote1.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regnote1) for loc_name in locnote1_names]
    multiworld.regions.append(regnote1)

    regnote2 = Region("Notebook 2 Room", player, multiworld, "Notebook 2 Room")
    locnote2_names = ["Notebook 2"]
    regnote2.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regnote2) for loc_name in locnote2_names]
    multiworld.regions.append(regnote2)

    regnote3 = Region("Notebook 3 Room", player, multiworld, "Notebook 3 Room")
    locnote3_names = ["Notebook 3", "Classic Mode - Scissors Pickup (Notebook 3 Room)"]
    if world.options.party:
        locnote3_names.append("Party Mode - Notebook 3 Room Present #1")
        locnote3_names.append("Party Mode - Notebook 3 Room Present #2")
    if world.options.demo:
        locnote3_names.append("Demo Mode - Item Pickup (Notebook 3 Room)")
    regnote3.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regnote3) for loc_name in locnote3_names]
    multiworld.regions.append(regnote3)

    regnote4 = Region("Notebook 4 Room", player, multiworld, "Notebook 4 Room")
    locnote4_names = ["Notebook 4", "Classic Mode - Scissors Pickup (Notebook 4 Room)"]
    if world.options.party:
        locnote4_names.append("Party Mode - Notebook 4 Room Present")
    if world.options.demo:
        locnote4_names.append("Demo Mode - Item Pickup (Notebook 4 Room)")
    regnote4.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regnote4) for loc_name in locnote4_names]
    multiworld.regions.append(regnote4)

    regnote5 = Region("Notebook 5 Room", player, multiworld, "Notebook 5 Room")
    locnote5_names = ["Notebook 5", "Classic Mode - Big 'Ol Boots Pickup (Notebook 5 Room)"]
    if world.options.party:
        locnote5_names.append("Party Mode - Notebook 5 Room Present #1")
        locnote5_names.append("Party Mode - Notebook 5 Room Present #2")
    if world.options.demo:
        locnote5_names.append("Demo Mode - Item Pickup (Notebook 5 Room)")
    regnote5.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regnote5) for loc_name in locnote5_names]
    multiworld.regions.append(regnote5)

    regnote6 = Region("Notebook 6 Room", player, multiworld, "Notebook 6 Room")
    locnote6_names = ["Notebook 6"]
    if world.options.party:
        locnote6_names.append("Party Mode - Notebook 6 Room Present")
    regnote6.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regnote6) for loc_name in locnote6_names]
    multiworld.regions.append(regnote6)

    regnote7 = Region("Notebook 7 Room", player, multiworld, "Notebook 7 Room")
    locnote7_names = ["Notebook 7", "Classic Mode - Scissors Pickup (Notebook 7 Room)"]
    if world.options.party:
        locnote7_names.append("Party Mode - Notebook 7 Room Present")
    if world.options.demo:
        locnote7_names.append("Demo Mode - Item Pickup #1 (Notebook 7 Room)")
        locnote7_names.append("Demo Mode - Item Pickup #2 (Notebook 7 Room)")
    regnote7.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regnote7) for loc_name in locnote7_names]
    multiworld.regions.append(regnote7)




    #regions for the school faculty rooms
    regfac1 = Region("Faculty Room 1 (Near South Exit)", player, multiworld, "Faculty Room 1 (Near South Exit)")
    locfac1_names = ["Classic Mode - Zesty Bar Pickup (School Faculty Room)"]
    if world.options.party:
        locfac1_names.append("Party Mode - South School Faculty Present")
    if world.options.demo:
        locfac1_names.append("Demo Mode - Item Pickup (South School Faculty Room)")
    regfac1.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regfac1) for loc_name in locfac1_names]
    multiworld.regions.append(regfac1)

    regfac2 = Region("Faculty Room 2 (Near Middle Of School)", player, multiworld, "Faculty Room 2 (Near Middle Of School)")
    locfac2_names = ["Classic Mode - Baldi's Least Favorite Tape Pickup (School Faculty Room)"]
    if world.options.party:
        locfac2_names.append("Party Mode - Center School Faculty Present")
    if world.options.demo:
        locfac2_names.append("Demo Mode - Item Pickup #1 (Center School Faculty Room)")
        locfac2_names.append("Demo Mode - Item Pickup #2 (Center School Faculty Room)")
    regfac2.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regfac2) for loc_name in locfac2_names]
    multiworld.regions.append(regfac2)

    regfac3 = Region("Faculty Room 3 (Near East Exit)", player, multiworld, "Faculty Room 3 (Near East Exit)")
    locfac3_names = ["Classic Mode - Swinging Door Lock Pickup (School Faculty Room)"]
    if world.options.party:
        locfac3_names.append("Party Mode - East School Faculty Present")
    if world.options.demo:
        locfac3_names.append("Demo Mode - Item Pickup #1 (East School Faculty Room)")
        locfac3_names.append("Demo Mode - Item Pickup #2 (East School Faculty Room)")
    regfac3.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regfac3) for loc_name in locfac3_names]
    multiworld.regions.append(regfac3)

    regfac4 = Region("Faculty Room 4 (Near Cafe)", player, multiworld, "Faculty Room 4 (Near Cafe)")
    locfac4_names = ["Classic Mode - Principal's Keys Pickup (School Faculty Room)", "Classic Mode - WD-NoSquee Pickup (School Faculty Room)", "Classic Mode - Zesty Bar Machine (School Faculty Room)"]
    if world.options.party:
        locfac4_names.append("Party Mode - Cafe School Faculty Present #1")
        locfac4_names.append("Party Mode - Cafe School Faculty Present #2")
        locfac4_names.append("Party Mode - School Faculty Fun Item Machine")
    if world.options.demo:
        locfac4_names.append("Demo Mode - Item Pickup #1 (Cafe School Faculty Room)")
        locfac4_names.append("Demo Mode - Item Pickup #2 (Cafe School Faculty Room)")
        locfac4_names.append("Demo Mode - Zesty Bar Machine (School Faculty Room)")
    regfac4.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regfac4) for loc_name in locfac4_names]
    multiworld.regions.append(regfac4)

    regfac5 = Region("Faculty Room 5 (Near West Exit)", player, multiworld, "Faculty Room 5 (Near West Exit)")
    locfac5_names = ["Classic Mode - Alarm Clock (School Faculty Room)", "Classic Mode - Quarter Pickup (School Faculty Room)"]
    if world.options.party:
        locfac5_names.append("Party Mode - West School Faculty Present #1")
        locfac5_names.append("Party Mode - West School Faculty Present #2")
    regfac5.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regfac5) for loc_name in locfac5_names]
    multiworld.regions.append(regfac5)

    # supply closet
    regsup = Region("Supply Closet", player, multiworld, "Supply Closet")
    locsup_names = ["Classic Mode - WD-NoSquee Pickup (Supply Closet)"]
    if world.options.party:
        locsup_names.append("Party Mode - Supply Closet Present")
    regsup.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regsup) for loc_name in locsup_names]
    multiworld.regions.append(regsup)

    # cafe thing
    regcafe = Region("Cafeteria", player, multiworld, "Cafeteria")
    loccafe_names = ["Classic Mode - Zesty Bar Pickup (Cafeteria)", "Classic Mode - BSODA Machine (Cafeteria)", "Classic Mode - BSODA Pickup (Cafeteria)"]
    if world.options.party:
        loccafe_names.append("Party Mode - Cafe Fun Item Machine")
        loccafe_names.append("Party Mode - Cafe Present #1")
        loccafe_names.append("Party Mode - Cafe Present #2")
    if world.options.demo:
        loccafe_names.append("Demo Mode - BSODA Machine (Cafeteria)")
        loccafe_names.append("Demo Mode - Item Pickup #1 (Cafeteria)")
        loccafe_names.append("Demo Mode - Item Pickup #2 (Cafeteria)")
    regcafe.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regcafe) for loc_name in loccafe_names]
    multiworld.regions.append(regcafe)

    if world.options.doorsanity:

        # Exits
        regwexit = Region("West Exit Region", player, multiworld, "West Exit Region")
        locwexit_names = ["Activated West Exit"]
        regwexit.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regwexit) for loc_name in
                              locwexit_names]
        multiworld.regions.append(regwexit)

        regsexit = Region("South Exit Region", player, multiworld, "South Exit Region")
        locsexit_names = ["Activated South Exit"]
        regsexit.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regsexit) for loc_name in
                               locsexit_names]
        multiworld.regions.append(regsexit)

        regeexit = Region("East Exit Region", player, multiworld, "East Exit Region")
        loceexit_names = ["Activated East Exit"]
        regeexit.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regeexit) for loc_name in
                               loceexit_names]
        multiworld.regions.append(regeexit)

        regnexit = Region("North Exit Region", player, multiworld, "North Exit Region")
        locnexit_names = ["Activated North Exit"]
        regnexit.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regnexit) for loc_name in
                               locnexit_names]
        multiworld.regions.append(regnexit)




        # Starting Yellow doors

        regwestydoor = Region("West Start Yellow Door", player, multiworld, "West Start Yellow Door")
        locwestydoor_names = ["Passed Through Yellow Swinging Door - West of Start"]
        regwestydoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regwestydoor) for loc_name in locwestydoor_names]
        multiworld.regions.append(regwestydoor)

        regeastydoor = Region("East Start Yellow Door", player, multiworld, "East Start Yellow Door")
        loceastydoor_names = ["Passed Through Yellow Swinging Door - East of Start"]
        regeastydoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regeastydoor) for loc_name
                                   in loceastydoor_names]
        multiworld.regions.append(regeastydoor)

        regnorthydoor = Region("North Start Yellow Door", player, multiworld, "North Start Yellow Door")
        locnorthydoor_names = ["Passed Through Yellow Swinging Door - North of Start"]
        regnorthydoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regnorthydoor) for loc_name
                                   in locnorthydoor_names]
        multiworld.regions.append(regnorthydoor)


        # Cafe Yellow Doors
        regcafewydoor = Region("West Cafe Yellow Door", player, multiworld, "West Cafe Yellow Door")
        loccafewydoor_names = ["Passed Through Yellow Swinging Door - West of Cafe"]
        regcafewydoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regcafewydoor) for loc_name
                                   in loccafewydoor_names]
        multiworld.regions.append(regcafewydoor)

        regcafeeydoor = Region("East Cafe Yellow Door", player, multiworld, "East Cafe Yellow Door")
        loccafeeydoor_names = ["Passed Through Yellow Swinging Door - East of Cafe"]
        regcafeeydoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regcafeeydoor) for loc_name
                                   in loccafeeydoor_names]
        multiworld.regions.append(regcafeeydoor)

        # rando middle yellow door
        regrdetdoor = Region("Right Detention Door", player, multiworld, "Right Detention Door")
        locrdetdoor_names = ["Passed Through Yellow Swinging Door - Right of Detention"]
        regrdetdoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regrdetdoor) for loc_name
                                    in locrdetdoor_names]
        multiworld.regions.append(regrdetdoor)

        regldetdoor = Region("Left Detention Door", player, multiworld, "Left Detention Door")
        locldetdoor_names = ["Passed Through Yellow Swinging Door - Left of Detention"]
        regldetdoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regldetdoor) for loc_name
                                  in locldetdoor_names]
        multiworld.regions.append(regldetdoor)

        regneydoor = Region("North-East Y Door", player, multiworld, "North-East Y Door")
        locneydoor_names = ["Passed Through Yellow Swinging Door - North-East Halls"]
        regneydoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regneydoor) for loc_name
                                  in locneydoor_names]
        multiworld.regions.append(regneydoor)


        # 99 Doors
        reg99wsdoor = Region("West Start 99 Door", player, multiworld, "West Start 99 Door")
        loc99wsdoor_names = ["Passed Through 99 Door - West Starting Class"]
        reg99wsdoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], reg99wsdoor) for loc_name
                                    in loc99wsdoor_names]
        multiworld.regions.append(reg99wsdoor)

        reg99esdoor = Region("East Start 99 Door", player, multiworld, "East Start 99 Door")
        loc99esdoor_names = ["Passed Through 99 Door - East Starting Class"]
        reg99esdoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], reg99esdoor) for loc_name
                                    in loc99esdoor_names]
        multiworld.regions.append(reg99esdoor)

        reg99cmdoor = Region("Center Middle 99 Door", player, multiworld, "Center Middle 99 Door")
        loc99cmdoor_names = ["Passed Through 99 Door - Center Middle Class"]
        reg99cmdoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], reg99cmdoor) for loc_name
                                  in loc99cmdoor_names]
        multiworld.regions.append(reg99cmdoor)

        reg99fcdoor = Region("99 Door Facing Cafe ^", player, multiworld, "99 Door Facing Cafe ^")
        loc99fcdoor_names = ["Passed Through 99 Door - Class North Facing Cafe"]
        reg99fcdoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], reg99fcdoor) for loc_name
                                  in loc99fcdoor_names]
        multiworld.regions.append(reg99fcdoor)

        reg99fc2door = Region("99 Door Facing Cafe >", player, multiworld, "99 Door Facing Cafe >")
        loc99fc2door_names = ["Passed Through 99 Door - Class Facing East Cafe"]
        reg99fc2door.locations += [BBCRLocation(player, loc_name, location_table[loc_name], reg99fc2door) for loc_name
                                  in loc99fc2door_names]
        multiworld.regions.append(reg99fc2door)

        reg99fedoor = Region("99 Door Facing East", player, multiworld, "99 Door Facing East")
        loc99fedoor_names = ["Passed Through 99 Door - East Hall Class"]
        reg99fedoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], reg99fedoor) for loc_name
                                   in loc99fedoor_names]
        multiworld.regions.append(reg99fedoor)

        reg99eXdoor = Region("99 Door by East Exit", player, multiworld, "99 Door by East Exit")
        loc99eXdoor_names = ["Passed Through 99 Door - Class by East Exit"]
        reg99eXdoor.locations += [BBCRLocation(player, loc_name, location_table[loc_name], reg99eXdoor) for loc_name
                                   in loc99eXdoor_names]
        multiworld.regions.append(reg99eXdoor)

        # School Faculty Doors

        regsfdoor1 = Region("South School Faculty Door", player, multiworld, "South School Faculty Door")
        locsfdoor1_names = ["Passed Through School Faculty Door - South"]
        regsfdoor1.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regsfdoor1) for loc_name
                                  in locsfdoor1_names]
        multiworld.regions.append(regsfdoor1)

        regsfdoor2 = Region("Joining School Faculty Door", player, multiworld, "Joining School Faculty Door")
        locsfdoor2_names = ["Passed Through School Faculty Door - Joining Two SF Rooms"]
        regsfdoor2.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regsfdoor2) for loc_name
                                 in locsfdoor2_names]
        multiworld.regions.append(regsfdoor2)

        regsfdoor3 = Region("School Faculty Door Near Center", player, multiworld, "School Faculty Door Near Center")
        locsfdoor3_names = ["Passed Through School Faculty Door - Near Center"]
        regsfdoor3.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regsfdoor3) for loc_name
                                 in locsfdoor3_names]
        multiworld.regions.append(regsfdoor3)

        regsfdoor4 = Region("School Faculty Door by East Exit", player, multiworld, "School Faculty Door by East Exit")
        locsfdoor4_names = ["Passed Through School Faculty Door - Near East Exit"]
        regsfdoor4.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regsfdoor4) for loc_name
                                 in locsfdoor4_names]
        multiworld.regions.append(regsfdoor4)

        regsfdoor5 = Region("School Faculty Door by Cafe", player, multiworld, "School Faculty Door by Cafe")
        locsfdoor5_names = ["Passed Through School Faculty Door - by Cafe"]
        regsfdoor5.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regsfdoor5) for loc_name
                                 in locsfdoor5_names]
        multiworld.regions.append(regsfdoor5)

        regsfdoor6 = Region("School Faculty Door by West Exit", player, multiworld, "School Faculty Door by West Exit")
        locsfdoor6_names = ["Passed Through School Faculty Door - Near West Exit"]
        regsfdoor6.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regsfdoor6) for loc_name in locsfdoor6_names]
        multiworld.regions.append(regsfdoor6)

        regsupply = Region("Supply Closet Door Region", player, multiworld, "Supply Closet Door")
        locsupply_names = ["Passed Through Supply Closet Door"]
        regsupply.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regsupply) for loc_name in
                                 locsupply_names]
        multiworld.regions.append(regsupply)

    if world.options.notechecks:

        regbook1 = Region("Notebook 1 Questions", player, multiworld, "Notebook 1 Questions")
        locbook1_names = ["Notebook 1 Question 1", "Notebook 1 Question 2", "Notebook 1 Question 3"]
        regbook1.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regbook1) for loc_name in locbook1_names]
        multiworld.regions.append(regbook1)

        regbook2 = Region("Notebook 2 Questions", player, multiworld, "Notebook 2 Questions")
        locbook2_names = ["Notebook 2 Question 1", "Notebook 2 Question 2", "Notebook 2 Question 3"]
        regbook2.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regbook2) for loc_name in locbook2_names]
        multiworld.regions.append(regbook2)

        regbook3 = Region("Notebook 3 Questions", player, multiworld, "Notebook 3 Questions")
        locbook3_names = ["Notebook 3 Question 1", "Notebook 3 Question 2", "Notebook 3 Question 3"]
        regbook3.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regbook3) for loc_name in locbook3_names]
        multiworld.regions.append(regbook3)

        regbook4 = Region("Notebook 4 Questions", player, multiworld, "Notebook 4 Questions")
        locbook4_names = ["Notebook 4 Question 1", "Notebook 4 Question 2", "Notebook 4 Question 3"]
        regbook4.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regbook4) for loc_name in locbook4_names]
        multiworld.regions.append(regbook4)

        regbook5 = Region("Notebook 5 Questions", player, multiworld, "Notebook 5 Questions")
        locbook5_names = ["Notebook 5 Question 1", "Notebook 5 Question 2", "Notebook 5 Question 3"]
        regbook5.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regbook5) for loc_name in locbook5_names]
        multiworld.regions.append(regbook5)

        regbook6 = Region("Notebook 6 Questions", player, multiworld, "Notebook 6 Questions")
        locbook6_names = ["Notebook 6 Question 1", "Notebook 6 Question 2", "Notebook 6 Question 3"]
        regbook6.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regbook6) for loc_name in locbook6_names]
        multiworld.regions.append(regbook6)

        regbook7 = Region("Notebook 7 Questions", player, multiworld, "Notebook 7 Questions")
        locbook7_names = ["Notebook 7 Question 1", "Notebook 7 Question 2", "Notebook 7 Question 3"]
        regbook7.locations += [BBCRLocation(player, loc_name, location_table[loc_name], regbook7) for loc_name in locbook7_names]
        multiworld.regions.append(regbook7)


    regnorthexit = Region("North Exit", player, multiworld, "North Exit")
    multiworld.regions.append(regnorthexit)

    regwestexit = Region("West Exit", player, multiworld, "West Exit")
    multiworld.regions.append(regwestexit)

    regeastexit = Region("East Exit", player, multiworld, "East Exit")
    multiworld.regions.append(regeastexit)

    regsouthexit = Region("South Exit", player, multiworld, "South Exit")
    multiworld.regions.append(regsouthexit)

    regexit = Region("Exit", player, multiworld, "Exit")
    multiworld.regions.append(regexit)




def connect(world, name: str, source: str, target: str, rule=None, reach: Optional[bool] = False,
            rule_to_str: Optional[str] = None, ) -> Optional[Entrance]:
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    connection = Entrance(world.player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)

    # print(f"\nConnecting Region {source} to Region {target} with rule: {rule_to_str}\n")

    return connection if reach else None


def connect_entrances(world) -> None:
    #connect Menu to the UI if I feel like AP'ing more than just classic mode
    connect(world, "Menu UI", "Menu", "UI")

    #classic mode entrance
    connect(world, "Game Start", "UI", "Starting Halls", lambda state: state.has("Classic Style", world.player) or state.has("Party Style", world.player) or state.has("Demo Style", world.player))

    connect(world, "North Exit", "North Exit", "Exit", lambda state: state.has("Notebook", world.player, 7))
    connect(world, "West Exit", "West Exit", "Exit", lambda state: state.has("Notebook", world.player, 7))
    connect(world, "East Exit", "East Exit", "Exit", lambda state: state.has("Notebook", world.player, 7))
    connect(world, "South Exit", "South Exit", "Exit", lambda state: state.has("Notebook", world.player, 7))

    if not world.options.doorsanity:

        #double doors lock
        connect(world, "Golden Double Doors", "Starting Halls", "Halls", lambda state: state.has("Notebook", world.player, 2))

        #connecting the other funny rooms
        connect(world, "Cafe Entrance", "Halls", "Cafeteria")
        connect(world, "Supply Closet Entrance", "Halls", "Supply Closet")

        #notebook room connecting (starting halls)
        connect(world, "Notebook 1 Room Entrance", "Starting Halls", "Notebook 1 Room")
        connect(world, "Notebook 2 Room Entrance", "Starting Halls", "Notebook 2 Room")
        connect(world, "Notebook 3 Room Entrance", "Halls", "Notebook 3 Room")
        connect(world, "Notebook 4 Room Entrance", "Halls", "Notebook 4 Room")
        connect(world, "Notebook 5 Room Entrance", "Halls", "Notebook 5 Room")
        connect(world, "Notebook 6 Room Entrance", "Halls", "Notebook 6 Room")
        connect(world, "Notebook 7 Room Entrance", "Halls", "Notebook 7 Room")

        #school faculty connecting (to halls)
        connect(world, "School Faculty Room Near South Exit", "Halls", "Faculty Room 1 (Near South Exit)")
        connect(world, "School Faculty Room Near Middle Of School", "Halls", "Faculty Room 2 (Near Middle Of School)")
        connect(world, "School Faculty Room Near East Exit", "Halls", "Faculty Room 3 (Near East Exit)")
        connect(world, "School Faculty Room Near Cafe", "Halls", "Faculty Room 4 (Near Cafe)")
        connect(world, "School Faculty Room Near West Exit", "Halls", "Faculty Room 5 (Near West Exit)")

        #school faculty rooms that need to be connected
        connect(world, "School Faculty Room 1 & 2 Connections", "Faculty Room 1 (Near South Exit)", "Faculty Room 2 (Near Middle Of School)")

        #connect the exits to the halls
        connect(world, "Cafe to North Exit", "Cafeteria", "North Exit", lambda state: state.has("Notebook", world.player, 7))
        connect(world, "Halls to West Exit", "Halls", "West Exit", lambda state: state.has("Notebook", world.player, 7))
        connect(world, "Halls to East Exit", "Halls", "East Exit", lambda state: state.has("Notebook", world.player, 7))
        connect(world, "Starting Halls to South Exit", "Starting Halls", "South Exit", lambda state: state.has("Notebook", world.player, 7))



    elif world.options.doorsanity:
        connect(world, "Start -> East Start Yellow Doors", "Starting Halls", "East Start Yellow Door", lambda state: state.has("Yellow Swinging Door - East of Start", world.player) and state.has("Notebook", world.player, 2) and state.has("99 Door - Starting Classroom West", world.player, 1) and state.has("99 Door - Starting Classroom East", world.player, 1))
        connect(world, "East Start Yellow Doors -> Halls", "East Start Yellow Door", "Halls", lambda state: state.has("Notebook", world.player, 2) and state.has("99 Door - Starting Classroom West", world.player, 1) and state.has("99 Door - Starting Classroom East", world.player, 1))

        connect(world, "Start -> West Start Yellow Doors", "Starting Halls", "West Start Yellow Door",
                lambda state: state.has("Yellow Swinging Door - West of Start", world.player) and state.has("Notebook", world.player, 2) and state.has("99 Door - Starting Classroom West", world.player, 1) and state.has("99 Door - Starting Classroom East", world.player, 1))
        connect(world, "West Start Yellow Doors -> Halls", "West Start Yellow Door", "Halls",
                lambda state: state.has("Notebook", world.player, 2) and state.has("99 Door - Starting Classroom West", world.player, 1) and state.has("99 Door - Starting Classroom East", world.player, 1))

        connect(world, "Start -> North Start Yellow Doors", "Starting Halls", "North Start Yellow Door",
                lambda state: state.has("Yellow Swinging Door - North of Start", world.player) and state.has("Notebook", world.player, 2) and state.has("99 Door - Starting Classroom West", world.player, 1) and state.has("99 Door - Starting Classroom East", world.player, 1))
        connect(world, "North Start Yellow Doors -> Halls", "North Start Yellow Door", "Halls",
                lambda state: state.has("Notebook", world.player, 2) and state.has("99 Door - Starting Classroom West", world.player, 1) and state.has("99 Door - Starting Classroom East", world.player, 1))

        connect(world, "Start -> West 99 Door", "Starting Halls", "West Start 99 Door",
                lambda state: state.has("99 Door - Starting Classroom West", world.player))
        connect(world, "Notebook 1 Room Entrance", "West Start 99 Door", "Notebook 1 Room")

        connect(world, "Start -> East 99 Door", "Starting Halls", "East Start 99 Door",
                lambda state: state.has("99 Door - Starting Classroom East", world.player))
        connect(world, "Notebook 2 Room Entrance", "East Start 99 Door", "Notebook 2 Room")

        connect(world, "Halls -> R Det Door", "Halls", "Right Detention Door",
                lambda state: state.has("Yellow Swinging Door - Right of Detention", world.player))

        connect(world, "Halls -> L Det Door", "Halls", "Left Detention Door",
                lambda state: state.has("Yellow Swinging Door - Left of Detention", world.player))

        connect(world, "Halls -> NE Y Door", "Halls", "North-East Y Door",
                lambda state: state.has("Yellow Swinging Door - North-East Halls", world.player))

        connect(world, "North Exit Door", "North Exit Region", "North Exit", lambda state: state.has("Notebook", world.player, 7) and state.has("North Exit", world.player))
        connect(world, "West Exit Door", "West Exit Region", "West Exit", lambda state: state.has("Notebook", world.player, 7) and state.has("West Exit", world.player))
        connect(world, "East Exit Door", "East Exit Region", "East Exit", lambda state: state.has("Notebook", world.player, 7) and state.has("East Exit", world.player))
        connect(world, "South Exit Door", "South Exit Region", "South Exit", lambda state: state.has("Notebook", world.player, 7) and state.has("South Exit", world.player))

        connect(world, "Starting Halls -> South Exit Door", "Starting Halls", "South Exit Region", lambda state: state.has("South Exit", world.player) and state.has("Notebook", world.player, 7))

        connect(world, "Halls -> East Cafe Door", "Halls", "East Cafe Yellow Door",
                lambda state: state.has("Yellow Swinging Door - Cafeteria East", world.player))
        connect(world, "Halls -> West Cafe Door", "Halls", "West Cafe Yellow Door",
                lambda state: state.has("Yellow Swinging Door - Cafeteria West", world.player))
        connect(world, "East Cafe Door -> Cafe", "East Cafe Yellow Door", "Cafeteria",
                lambda state: state.has("Yellow Swinging Door - Cafeteria East", world.player))
        connect(world, "West Cafe Door -> Cafe", "West Cafe Yellow Door", "Cafeteria",
                lambda state: state.has("Yellow Swinging Door - Cafeteria West", world.player))

        connect(world, "North Exit Door in Cafe", "Cafeteria", "North Exit Region",
                lambda state: state.has("Notebook", world.player, 7) and state.has("North Exit", world.player))

        connect(world, "Halls -> East Exit", "Halls", "East Exit Region",
                lambda state: state.has("East Exit", world.player) and state.has("Notebook", world.player, 7))
        connect(world, "Halls -> West Exit", "Halls", "West Exit Region",
                lambda state: state.has("West Exit", world.player) and state.has("Notebook", world.player, 7))

        connect(world, "Halls -> Center Middle 99 Door", "Halls", "Center Middle 99 Door",
                lambda state: state.has("99 Door - Classroom Near Center", world.player))
        connect(world, "Notebook 3 Room Entrance", "Center Middle 99 Door", "Notebook 3 Room")

        connect(world, "Halls -> 99 Door Facing Cafe ^", "Halls", "99 Door Facing Cafe ^",
                lambda state: state.has("99 Door - Classroom South of Cafeteria", world.player))
        connect(world, "Notebook 4 Room Entrance", "99 Door Facing Cafe ^", "Notebook 4 Room")

        connect(world, "Halls -> 99 Door Facing Cafe >", "Halls", "99 Door Facing Cafe >",
                lambda state: state.has("99 Door - Classroom West of Cafeteria", world.player))
        connect(world, "Notebook 5 Room Entrance", "99 Door Facing Cafe >", "Notebook 5 Room")

        connect(world, "Halls -> 99 Door Facing East", "Halls", "99 Door Facing East",
                lambda state: state.has("99 Door - Classroom in North East Halls", world.player))
        connect(world, "Notebook 6 Room Entrance", "99 Door Facing East", "Notebook 6 Room")

        connect(world, "Halls -> 99 Door by East Exit", "Halls", "99 Door by East Exit",
                lambda state: state.has("99 Door - Classroom by East Exit", world.player))
        connect(world, "Notebook 7 Room Entrance", "99 Door by East Exit", "Notebook 7 Room")

        # Connect School Fac

        connect(world, "Halls -> SF1", "Halls", "South School Faculty Door",
                lambda state: state.has("School Faculty Door - South", world.player))
        connect(world, "SF1 Entrance", "South School Faculty Door", "Faculty Room 1 (Near South Exit)")

        connect(world, "Halls -> SF2", "Halls", "School Faculty Door Near Center",
                lambda state: state.has("School Faculty Door - Center", world.player))
        connect(world, "SF2 Entrance", "School Faculty Door Near Center", "Faculty Room 2 (Near Middle Of School)")

        connect(world, "Halls -> SF3", "Halls", "School Faculty Door by East Exit",
                lambda state: state.has("School Faculty Door - East Halls", world.player))
        connect(world, "SF3 Entrance", "School Faculty Door by East Exit", "Faculty Room 3 (Near East Exit)")

        connect(world, "Halls -> SF4", "Halls", "School Faculty Door by Cafe",
                lambda state: state.has("School Faculty Door - South East of Cafeteria", world.player))
        connect(world, "SF4 Entrance", "School Faculty Door by Cafe", "Faculty Room 4 (Near Cafe)")

        connect(world, "Halls -> SF5", "Halls", "School Faculty Door by West Exit",
                lambda state: state.has("School Faculty Door - West by Exit", world.player))
        connect(world, "SF5 Entrance", "School Faculty Door by West Exit", "Faculty Room 5 (Near West Exit)")

        connect(world, "Halls -> Supply Closet Door", "Halls", "Supply Closet Door Region", lambda state: state.has("Supply Closet Door", world.player))
        connect(world, "Supply Closet Door -> Supply Closet", "Supply Closet Door Region", "Supply Closet")

        connect(world, "SF1 -> Joining Door", "Faculty Room 1 (Near South Exit)", "Joining School Faculty Door", lambda state: state.has("School Faculty Door - Connecting Rooms", world.player))
        connect(world, "SF2 -> Joining Door", "Faculty Room 2 (Near Middle Of School)", "Joining School Faculty Door", lambda state: state.has("School Faculty Door - Connecting Rooms", world.player))









    if world.options.notechecks:
        connect(world, "Notebook 1 Questions Entrance", "Notebook 1 Room", "Notebook 1 Questions")
        connect(world, "Notebook 2 Questions Entrance", "Notebook 2 Room", "Notebook 2 Questions")
        connect(world, "Notebook 3 Questions Entrance", "Notebook 3 Room", "Notebook 3 Questions")
        connect(world, "Notebook 4 Questions Entrance", "Notebook 4 Room", "Notebook 4 Questions")
        connect(world, "Notebook 5 Questions Entrance", "Notebook 5 Room", "Notebook 5 Questions")
        connect(world, "Notebook 6 Questions Entrance", "Notebook 6 Room", "Notebook 6 Questions")
        connect(world, "Notebook 7 Questions Entrance", "Notebook 7 Room", "Notebook 7 Questions")

