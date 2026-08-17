import typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .__init__ import BBCRWorld
from ..generic.Rules import add_rule, set_rule
from BaseClasses import CollectionState

def set_location_rules(world: "BBCRWorld") -> None:

    yellow_door_west_start = world.get_location("Passed Through Yellow Swinging Door - West of Start")
    add_rule(yellow_door_west_start, lambda state: state.has("Yellow Swinging Door - West of Start", world.player, 1))

    yellow_door_east_start = world.get_location("Passed Through Yellow Swinging Door - East of Start")
    add_rule(yellow_door_east_start, lambda state: state.has("Yellow Swinging Door - East of Start", world.player, 1))

    yellow_door_north_start = world.get_location("Passed Through Yellow Swinging Door - North of Start")
    add_rule(yellow_door_north_start, lambda state: state.has("Yellow Swinging Door - North of Start", world.player, 1))

    yellow_door_east_cafe = world.get_location("Passed Through Yellow Swinging Door - East of Cafe")
    add_rule(yellow_door_east_cafe, lambda state: state.has("Yellow Swinging Door - Cafeteria East", world.player, 1))

    yellow_door_west_cafe = world.get_location("Passed Through Yellow Swinging Door - West of Cafe")
    add_rule(yellow_door_west_cafe, lambda state: state.has("Yellow Swinging Door - Cafeteria West", world.player, 1))

    yellow_door_det_r = world.get_location("Passed Through Yellow Swinging Door - Right of Detention")
    add_rule(yellow_door_det_r, lambda state: state.has("Yellow Swinging Door - Right of Detention", world.player, 1))

    yellow_door_det_l = world.get_location("Passed Through Yellow Swinging Door - Left of Detention")
    add_rule(yellow_door_det_l, lambda state: state.has("Yellow Swinging Door - Left of Detention", world.player, 1))

    yellow_door_ne = world.get_location("Passed Through Yellow Swinging Door - North-East Halls")
    add_rule(yellow_door_ne, lambda state: state.has("Yellow Swinging Door - North-East Halls", world.player, 1))

    # 99 doors
    nine_door_west_start = world.get_location("Passed Through 99 Door - West Starting Class")
    add_rule(nine_door_west_start, lambda state: state.has("99 Door - Starting Classroom West", world.player, 1))

    nine_door_east_start = world.get_location("Passed Through 99 Door - East Starting Class")
    add_rule(nine_door_east_start, lambda state: state.has("99 Door - Starting Classroom East", world.player, 1))

    nine_door_center = world.get_location("Passed Through 99 Door - Center Middle Class")
    add_rule(nine_door_center, lambda state: state.has("99 Door - Classroom Near Center", world.player, 1))

    nine_door_north_cafe = world.get_location("Passed Through 99 Door - Class Facing East Cafe")
    add_rule(nine_door_north_cafe, lambda state: state.has("99 Door - Classroom West of Cafeteria", world.player, 1))

    nine_door_south_of_cafe = world.get_location("Passed Through 99 Door - Class North Facing Cafe")
    add_rule(nine_door_south_of_cafe, lambda state: state.has("99 Door - Classroom South of Cafeteria", world.player, 1))

    nine_door_east_hall = world.get_location("Passed Through 99 Door - East Hall Class")
    add_rule(nine_door_east_hall, lambda state: state.has("99 Door - Classroom in North East Halls", world.player, 1))

    nine_door_east_exit = world.get_location("Passed Through 99 Door - Class by East Exit")
    add_rule(nine_door_east_exit, lambda state: state.has("99 Door - Classroom by East Exit", world.player, 1))

    # Faculty Doors
    fac_door_south = world.get_location("Passed Through School Faculty Door - South")
    add_rule(fac_door_south, lambda state: state.has("School Faculty Door - South", world.player, 1))

    fac_door_connec = world.get_location("Passed Through School Faculty Door - Joining Two SF Rooms")
    add_rule(fac_door_connec, lambda state: state.has("School Faculty Door - Connecting Rooms", world.player, 1))

    fac_door_center = world.get_location("Passed Through School Faculty Door - Near Center")
    add_rule(fac_door_center, lambda state: state.has("School Faculty Door - Center", world.player, 1))

    fac_door_east = world.get_location("Passed Through School Faculty Door - Near East Exit")
    add_rule(fac_door_east, lambda state: state.has("School Faculty Door - East Halls", world.player, 1))

    fac_door_cafe = world.get_location("Passed Through School Faculty Door - by Cafe")
    add_rule(fac_door_cafe, lambda state: state.has("School Faculty Door - South East of Cafeteria", world.player, 1))

    fac_door_west = world.get_location("Passed Through School Faculty Door - Near West Exit")
    add_rule(fac_door_west, lambda state: state.has("School Faculty Door - West by Exit", world.player, 1))

    closet = world.get_location("Passed Through Supply Closet Door")
    add_rule(closet, lambda state: state.has("Supply Closet Door", world.player, 1))

    # Exits
    south_exit = world.get_location("Activated South Exit")
    add_rule(south_exit,
             lambda state: state.has("South Exit", world.player, 1) and state.has("Notebook", world.player, 7))

    east_exit = world.get_location("Activated East Exit")
    add_rule(east_exit, lambda state: state.has("East Exit", world.player, 1) and state.has("Notebook", world.player, 7))

    west_exit = world.get_location("Activated West Exit")
    add_rule(west_exit, lambda state: state.has("West Exit", world.player, 1) and state.has("Notebook", world.player, 7))

    north_exit = world.get_location("Activated North Exit")
    add_rule(north_exit,
             lambda state: state.has("North Exit", world.player, 1) and state.has("Notebook", world.player, 7))

    # Vending Machines
    bsoda1 = world.get_location("Classic Mode - BSODA Machine (Cafeteria)")
    add_rule(bsoda1, lambda state: state.has("Quarter", world.player, 2))

    bsoda2 = world.get_location("Classic Mode - BSODA Machine (Halls)")
    add_rule(bsoda2, lambda state: state.has("Quarter", world.player, 2))

    zesty1 = world.get_location("Classic Mode - Zesty Bar Machine (School Faculty Room)")
    add_rule(zesty1, lambda state: state.has("Quarter", world.player, 2))

    #quarter reward
    quarter = world.get_location("Classic Mode - Baldi's Quarter Reward")
    add_rule(quarter, lambda state: state.has("Notebook", world.player, 1))

    #item usage
    if world.options.item_usage:
        quarter_use = world.get_location("Used a Quarter")
        add_rule(quarter_use, lambda state: state.has("Quarter", world.player, 1))

        scissor_use = world.get_location("Used Scissors")
        add_rule(scissor_use, lambda state: state.has("Safety Scissors", world.player, 1))

        keys_use = world.get_location("Escaped Detention With Keys")
        add_rule(keys_use, lambda state: state.has("Principal's Keys", world.player, 1))

        tape_use = world.get_location("Used Baldi's Least Favorite Tape")
        add_rule(tape_use, lambda state: state.has("Baldi's Least Favorite Tape", world.player, 1))

        bar_use = world.get_location("Used Zesty Bar")
        add_rule(bar_use, lambda state: state.has("Zesty Bar", world.player, 1))

        soda_use = world.get_location("Used BSODA")
        add_rule(soda_use, lambda state: state.has("BSODA", world.player, 1))

        boot_use = world.get_location("Used the Big 'Ol Boots")
        add_rule(boot_use, lambda state: state.has("Big 'Ol Boots", world.player, 1))

        wd_use = world.get_location("Used the WD-NoSquee")
        add_rule(wd_use, lambda state: state.has("WD-NoSquee", world.player, 1))

        lock_use = world.get_location("Used the Yellow Swinging Door Lock")
        add_rule(lock_use, lambda state: state.has("Swinging Door Lock", world.player, 1))

        clock_use = world.get_location("Used the Alarm Clock")
        add_rule(clock_use, lambda state: state.has("Alarm Clock", world.player, 1))

    empty_variable = 0
    while empty_variable != 18:
        print(str(world.location_id_to_name[8 + empty_variable]))
        add_rule(world.get_location(str(world.location_id_to_name[8 + empty_variable])), lambda state: state.has("Classic Style", world.player, 1))
        print(str(world.location_id_to_name[8 + empty_variable]) + " is now locked behind classic")
        empty_variable += 1

    empty_variable = 1
    while empty_variable != 17:
        print(str(world.location_id_to_name[83 + empty_variable]))
        add_rule(world.get_location(str(world.location_id_to_name[83 + empty_variable])), lambda state: state.has("Party Style", world.player, 1))
        print(str(world.location_id_to_name[83 + empty_variable]) + " is now locked behind party")
        empty_variable += 1

    empty_variable = 1
    while empty_variable != 20:
        print(str(world.location_id_to_name[104 + empty_variable]))
        add_rule(world.get_location(str(world.location_id_to_name[104 + empty_variable])),
                 lambda state: state.has("Demo Style", world.player, 1))
        print(str(world.location_id_to_name[104 + empty_variable]) + " is now locked behind demo")
        empty_variable += 1