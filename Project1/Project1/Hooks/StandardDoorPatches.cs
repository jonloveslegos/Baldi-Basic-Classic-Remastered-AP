using BaldiAP.Enums;
using HarmonyLib;
using UnityEngine;

namespace BaldiAP.Hooks;

[HarmonyPatch(typeof(StandardDoor))]
public class StandardDoorPatches
{
    [HarmonyPatch(nameof(StandardDoor.Start))]
    [HarmonyPrefix]
    public static bool Start(StandardDoor __instance)
    {
        RenameStandardDoor(__instance.transform);
        return true;
    }

    private static void RenameStandardDoor(Transform transform)
    {
        transform.name = (transform.position.x, transform.position.y, transform.position.z) switch
        {
            (165.0f, 0.0f, 55.0f) => NineDoorNames.StartClassWest,
            (185.0f, 0.0f, 65.0f) => NineDoorNames.StartClassEast,
            (195.0f, 0.0f, 155.0f) => NineDoorNames.CenterClass,
            (145.0f, 0.0f, 265.0f) => NineDoorNames.SouthCafeClass,
            (55.0f, 0.0f, 305.0f) => NineDoorNames.WestCafeClass,
            (275.0f, 0.0f, 335.0f) => NineDoorNames.NorthEastClass,
            (275.0f, 0.0f, 195.0f) => NineDoorNames.EastClass,
            (95.0f, 0.0f, 45.0f) => FacultyDoorNames.FacSouth,
            (115.0f, 0.0f, 95.0f) => FacultyDoorNames.FacConnect,
            (145.0f, 0.0f, 155.0f) => FacultyDoorNames.FacCenter,
            (275.0f, 0.0f, 125.0f) => FacultyDoorNames.FacEast,
            (215.0f, 0.0f, 265.0f) => FacultyDoorNames.FacSouthOfCafe,
            (75.0f, 0.0f, 195.0f) => FacultyDoorNames.FacWest,
            (195.0f, 0.0f, 195.0f) => "Detention Door",
            (245.0f, 0.0f, 65.0f) => "Supply Closet Door",
            _ => transform.name
        };
    }
}