using Archipelago.MultiClient.Net;
using Archipelago.MultiClient.Net.BounceFeatures.DeathLink;
using Archipelago.MultiClient.Net.Enums;
using Archipelago.MultiClient.Net.Helpers;
using Archipelago.MultiClient.Net.Models;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using Rewired;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using TMPro;
using Unity.Mathematics;
using UnityEngine;
using UnityEngine.Networking.Types;
using UnityEngine.UI;
using static UnityEngine.Networking.UnityWebRequest;

namespace BaldiAP
{
    [BepInPlugin(pluginGuid, pluginName, pluginVersion)]
    public class Plugin : BaseUnityPlugin
    {
        public const string pluginGuid = "grenhunterr.baldi.archipelago.unityisstupid";
        public const string pluginName = "Baldi's Basics Classic Remastered Archipelago Mod";
        public const string pluginVersion = "1.0.0";
        internal static new ManualLogSource Logger;
        public static ArchipelagoSession ap_session;
        static string ap_ip = "";
        static string ap_port = "";
        public static DeathLinkService deathLinkService;
        public static string ap_slot = "";
        public static bool is_deathlinked = false;
        static string ap_pass = "";
        static float connect_timer = 0;
        public static int run_removed_notebooks = 0;
        public static int notebook_obtained = 0;
        public static List<Items> items_obtained = new List<Items>();
        public static List<Items> items_queue = new List<Items>();
        public static Dictionary<Items, ItemObject> item_list = new Dictionary<Items, ItemObject>();
        public static Dictionary<string, SoundObject> sound_list = new Dictionary<string, SoundObject>();
        public static List<Door> door_list = new List<Door>();
        public static Dictionary<string, Door> myLockedDoors = new Dictionary<string, Door>();
        public static Dictionary<string, Elevator> myLockedExits = new Dictionary<string, Elevator>();
        public static Dictionary<string, long> option_values = new Dictionary<string, long>();
        public static List<string> doors_obtained = new List<string>();

        public void Get_Ap_Info()
        {
            var myLoc = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            if (myLoc.Contains("BaldiAP.dll"))
            {
                myLoc = myLoc.Replace("BaldiAP.dll", "");
            }
            if (!myLoc.EndsWith("\\") && !myLoc.EndsWith("/"))
            {
                myLoc = myLoc + "\\";
            }
            // Logger.LogInfo(myLoc);
            var ap_info_settings = File.OpenText(myLoc + "AP_Connection_Info.txt");
            while (!ap_info_settings.EndOfStream)
            {
                var read_info = ap_info_settings.ReadLine();
                if (read_info.Contains("ip="))
                {
                    ap_ip = read_info.Replace("ip=", "").Trim();
                }
                else if (read_info.Contains("port="))
                {
                    ap_port = read_info.Replace("port=", "").Trim();
                }
                else if (read_info.Contains("slot="))
                {
                    ap_slot = read_info.Replace("slot=", "").Trim();
                }
                else if (read_info.Contains("pass="))
                {
                    ap_pass = read_info.Replace("pass=", "").Trim();
                }
            }
            ap_info_settings.Close();
            if (ap_pass == "") { ap_pass = null; }
            // Logger.LogInfo(ap_ip);
            // Logger.LogInfo(ap_port);
        }

        public void Awake()
        {
            // Plugin startup logic
            Logger = base.Logger;
            Logger.LogInfo($"Plugin is loaded! Get ready for either torture, or errors, which could also be a form of torture I suppose.");
            Get_Ap_Info();
            ap_session = ArchipelagoSessionFactory.CreateSession(ap_ip, Int32.Parse(ap_port));

            ap_session.Items.ItemReceived += (receivedItemsHelper) => {
                var itemReceivedID = receivedItemsHelper.PeekItem().ItemId;

                if (itemReceivedID == 1)
                {
                    notebook_obtained += 1;
                }
                else if (itemReceivedID == 2)
                {
                    items_obtained.Add(Items.Quarter);
                    items_queue.Add(Items.Quarter);
                }
                else if (itemReceivedID == 3)
                {
                    items_obtained.Add(Items.Bsoda);
                    items_queue.Add(Items.Bsoda);
                }
                else if (itemReceivedID == 4)
                {
                    items_obtained.Add(Items.ZestyBar);
                    items_queue.Add(Items.ZestyBar);
                }
                else if (itemReceivedID == 5)
                {
                    items_obtained.Add(Items.Tape);
                    items_queue.Add(Items.Tape);
                }
                else if (itemReceivedID == 6)
                {
                    items_obtained.Add(Items.Scissors);
                    items_queue.Add(Items.Scissors);
                }
                else if (itemReceivedID == 7)
                {
                    items_obtained.Add(Items.Boots);
                    items_queue.Add(Items.Boots);
                }
                else if (itemReceivedID == 8)
                {
                    items_obtained.Add(Items.Wd40);
                    items_queue.Add(Items.Wd40);
                }
                else if (itemReceivedID == 9)
                {
                    items_obtained.Add(Items.AlarmClock);
                    items_queue.Add(Items.AlarmClock);
                }
                else if (itemReceivedID == 10)
                {
                    items_obtained.Add(Items.DetentionKey);
                    items_queue.Add(Items.DetentionKey);
                }
                else if (itemReceivedID == 11)
                {
                    items_obtained.Add(Items.DoorLock);
                    items_queue.Add(Items.DoorLock);
                }
                else if (itemReceivedID == 12)
                {
                    if (GameObject.FindObjectOfType<ClassicGameManager>() != null)
                    {
                        if (GameObject.FindObjectOfType<Playtime>() != null)
                        {
                            // Logger.LogInfo("pre-playtime");
                            AccessTools.Field(typeof(Playtime), "cooldown").SetValue(GameObject.FindObjectOfType<Playtime>(), 0f);
                            // Logger.LogInfo("post-playtime cooldown");
                            GameObject.FindObjectOfType<Playtime>().transform.position = Singleton<CoreGameManager>.Instance.GetPlayer(0).transform.position;
                            // Logger.LogInfo("post-playtime");
                        }
                    }
                }
                else if (itemReceivedID == 13)
                {
                    if (GameObject.FindObjectOfType<ClassicGameManager>() != null)
                    {
                        if (GameObject.FindObjectOfType<ArtsAndCrafters>() != null)
                        {
                            // Logger.LogInfo("pre-arts");
                            AccessTools.Field(typeof(ArtsAndCrafters), "angry").SetValue(GameObject.FindObjectOfType<ArtsAndCrafters>(), true);
                            // Logger.LogInfo("post-arts cooldown");
                            AccessTools.Method(typeof(ArtsAndCrafters), "OnTriggerEnter").Invoke(GameObject.FindObjectOfType<ArtsAndCrafters>(), new object[] { Singleton<CoreGameManager>.Instance.GetPlayer(0).plm.cc });
                            // Logger.LogInfo("post-arts");
                            AccessTools.Field(typeof(ArtsAndCrafters), "angry").SetValue(GameObject.FindObjectOfType<ArtsAndCrafters>(), false);
                        }
                    }
                }
                else if (itemReceivedID == 14)
                {
                    if (GameObject.FindObjectOfType<ClassicGameManager>() != null)
                    {
                        if (GameObject.FindObjectOfType<Principal>() != null)
                        {
                            AccessTools.Field(typeof(Principal), "angry").SetValue(GameObject.FindObjectOfType<Principal>(), true);
                            AccessTools.Field(typeof(Principal), "targetedPlayer").SetValue(GameObject.FindObjectOfType<Principal>(), Singleton<CoreGameManager>.Instance.GetPlayer(0));
                            GameObject.FindObjectOfType<Principal>().transform.position = Singleton<CoreGameManager>.Instance.GetPlayer(0).transform.position;
                        }
                    }
                }
                else if (itemReceivedID == 37)
                {
                    doors_obtained.Add("45, 0, 225");
                    doors_obtained.Add("Door_Swinging(Clone) - 55, 0, 225 - Room0_Hallway");
                }
                else if (itemReceivedID == 38)
                {
                    doors_obtained.Add("135, 0, 385");
                    doors_obtained.Add("Door_Swinging(Clone) - 135, 0, 375 - Room14_Cafeteria");
                }
                else if (itemReceivedID == 35)
                {
                    doors_obtained.Add("305, 0, 215");
                    doors_obtained.Add("Door_Swinging(Clone) - 295, 0, 215 - Room0_Hallway");
                }
                else if (itemReceivedID == 36)
                {
                    doors_obtained.Add("175, 0, 15");
                    doors_obtained.Add("Door_Swinging(Clone) - 175, 0, 25 - Room0_Hallway");
                }
                else if (itemReceivedID == 39)
                {
                    doors_obtained.Add("Door_Swinging(Clone) - 245, 0, 365 - Room0_Hallway");
                }
                else if (itemReceivedID == 19)
                {
                    doors_obtained.Add("Door_Swinging(Clone) - 195, 0, 325 - Room14_Cafeteria");
                }
                else if (itemReceivedID == 18)
                {
                    doors_obtained.Add("Door_Swinging(Clone) - 75, 0, 325 - Room14_Cafeteria");
                }
                else if (itemReceivedID == 20)
                {
                    doors_obtained.Add("Door_Swinging(Clone) - 205, 0, 225 - Room0_Hallway");
                }
                else if (itemReceivedID == 40)
                {
                    doors_obtained.Add("Door_Swinging(Clone) - 145, 0, 225 - Room0_Hallway");
                }
                else if (itemReceivedID == 15)
                {
                    doors_obtained.Add("ClassicDoor_Swinging(Clone) - 175, 0, 75 - Room0_Hallway");
                }
                else if (itemReceivedID == 17)
                {
                    doors_obtained.Add("ClassicDoor_Swinging(Clone) - 215, 0, 35 - Room0_Hallway");
                }
                else if (itemReceivedID == 16)
                {
                    doors_obtained.Add("ClassicDoor_Swinging(Clone) - 135, 0, 35 - Room0_Hallway");
                }
                else if (itemReceivedID == 28)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 245, 0, 65 - Room15_Closet");
                }
                else if (itemReceivedID == 30)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 75, 0, 195 - Room12_Faculty5");
                }
                else if (itemReceivedID == 34)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 215, 0, 265 - Room11_Faculty4");
                }
                else if (itemReceivedID == 33)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 275, 0, 125 - Room10_Faculty3");
                }
                else if (itemReceivedID == 31)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 145, 0, 155 - Room9_Faculty2");
                }
                else if (itemReceivedID == 32)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 115, 0, 95 - Room8_Faculty1");
                }
                else if (itemReceivedID == 29)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 95, 0, 45 - Room8_Faculty1");
                }
                else if (itemReceivedID == 26)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 275, 0, 195 - Room7_Classroom7");
                }
                else if (itemReceivedID == 27)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 275, 0, 335 - Room6_Classroom6");
                }
                else if (itemReceivedID == 25)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 55, 0, 305 - Room5_Classroom5");
                }
                else if (itemReceivedID == 24)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 145, 0, 265 - Room4_Classroom4");
                }
                else if (itemReceivedID == 23)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 195, 0, 155 - Room3_Classroom3");
                }
                else if (itemReceivedID == 22)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 185, 0, 65 - Room2_Classroom2");
                }
                else if (itemReceivedID == 21)
                {
                    doors_obtained.Add("ClassDoor_Standard(Clone) - 165, 0, 55 - Room1_Classroom1");
                }

                receivedItemsHelper.DequeueItem();
            };

            MyPatches.StartPatches();
        }

        public string GetDoorObjectName(Door thisDoor)
        {
            return thisDoor.name + " - " + thisDoor.transform.position.x.ToString() + ", " + thisDoor.transform.position.y.ToString() + ", " + thisDoor.transform.position.z.ToString() + " - " + thisDoor.transform.parent.parent.parent.name;
        }

        public string GetSwingDoorObjectName(Door thisDoor)
        {
            return thisDoor.name + " - " + thisDoor.transform.position.x.ToString() + ", " + thisDoor.transform.position.y.ToString() + ", " + thisDoor.transform.position.z.ToString() + " - " + thisDoor.transform.parent.parent.name;
        }

        public void Update()
        {
            var connect_status = "Connected! Launch Classic Style to play";
            if (MyPatches.lockedStandard == null)
            {
                foreach (var mat in Resources.FindObjectsOfTypeAll<Material>())
                {
                    if (mat.name == "DoorTexture_Closed")
                    {
                        MyPatches.lockedStandard = mat;
                        break;
                    }
                }
            }
            if (ap_session.ConnectionInfo.Slot == -1)
            {
                connect_status = "FAILED TO CONNECT!";
                if (connect_timer <= 0)
                {
                    Get_Ap_Info();
                    notebook_obtained = 0;
                    items_obtained = new List<Items>();
                    doors_obtained = new List<string>();
                    is_deathlinked = false;
                    option_values = new Dictionary<string, long>();
                    door_list = new List<Door>();
                    myLockedDoors = new Dictionary<string, Door>();
                    myLockedExits = new Dictionary<string, Elevator>();
                    items_queue = new List<Items>();
                    item_list = new Dictionary<Items, ItemObject>();
                    var result = ap_session.TryConnectAndLogin(game: "Baldis Basics Classic Remastered", name: ap_slot, itemsHandlingFlags: ItemsHandlingFlags.AllItems);
                    if (!result.Successful)
                    {
                        Logger.LogError($"FAILED TO CONNECT TO SLOT\nIP = " + ap_ip + ":" + ap_port + "\nSLOT = " + ap_slot);
                        LoginFailure failure = (LoginFailure)result;
                        string errorMessage = $"";
                        foreach (string error in failure.Errors)
                        {
                            errorMessage += $"\n    {error}";
                        }
                        foreach (ConnectionRefusedError error in failure.ErrorCodes)
                        {
                            errorMessage += $"\n    {error}";
                        }
                        Logger.LogError(errorMessage);
                        connect_timer = 10.0f;
                    }
                    else
                    {
                        Logger.LogMessage("Connected Successfully");
                        foreach (var item in ap_session.DataStorage.GetSlotData(slot: Plugin.ap_session.Players.ActivePlayer.Slot))
                        {
                            // Logger.LogMessage(item.Key + "  :::  "+(long)item.Value);
                            option_values.Add(item.Key, (long)item.Value);
                        }
                        if (option_values["death_link"] == 1)
                        {
                            deathLinkService = ap_session.CreateDeathLinkService();
                            deathLinkService.OnDeathLinkReceived += (deathLinkObject) =>
                            {
                                Logger.LogMessage(deathLinkObject.Cause);
                                if (ap_session.ConnectionInfo.Slot != -1)
                                {
                                    if (GameObject.FindObjectOfType<ClassicGameManager>() != null)
                                    {
                                        if (Singleton<CoreGameManager>.Instance.GetPlayer(0) != null)
                                        {
                                            var environment_controller = GameObject.FindObjectOfType<EnvironmentController>();
                                            is_deathlinked = true;
                                            environment_controller.GetBaldi().GetAngry(20);
                                        }
                                    }
                                }
                            };

                            deathLinkService.EnableDeathLink();
                        }
                    }
                }
                else
                {
                    connect_timer -= Time.deltaTime;
                }
            }
            else if (GameObject.FindObjectOfType<ClassicGameManager>() != null)
            {
                if (Singleton<CoreGameManager>.Instance.GetPlayer(0) != null)
                {
                    var player_itm_manager = Singleton<CoreGameManager>.Instance.GetPlayer(0).itm;
                    var classic_game_manager = GameObject.FindObjectOfType<ClassicGameManager>();
                    var environment_controller = GameObject.FindObjectOfType<EnvironmentController>();
                    if (is_deathlinked)
                    {
                        if (environment_controller.GetBaldi() != null)
                        {
                            var baldman = environment_controller.GetBaldi();
                            baldman.PlayerInSight(Singleton<CoreGameManager>.Instance.GetPlayer(0));
                            baldman.baseSpeed = 500;
                            baldman.GetAngry(0f);
                            baldman.ManualSlap();
                        }
                    }
                    if (item_list.Count <= 6)
                    {
                        var to_test_list = Resources.FindObjectsOfTypeAll<ItemObject>();
                        foreach (var item in to_test_list)
                        {
                            if (!item_list.ContainsKey(item.itemType))
                            {
                                item_list.Add(item.itemType, item);
                                // Logger.LogInfo("Found ItemObject of itemType " + item.itemType.ToString());
                            }
                        }
                    }
                    if (sound_list.Count <= 10)
                    {
                        var to_test_list_sound = Resources.FindObjectsOfTypeAll<SoundObject>();
                        foreach (var item in to_test_list_sound)
                        {
                            if (!sound_list.ContainsKey(item.soundKey))
                            {
                                sound_list.Add(item.soundKey, item);
                                // Logger.LogInfo("Found SoundObject of soundKey " + item.soundKey);
                            }
                        }
                    }
                    if (Singleton<BaseGameManager>.Instance.FoundNotebooks > notebook_obtained)
                    {
                        run_removed_notebooks = Math.Max(Singleton<BaseGameManager>.Instance.FoundNotebooks, run_removed_notebooks);
                        Singleton<BaseGameManager>.Instance.CollectNotebooks(notebook_obtained - Singleton<BaseGameManager>.Instance.FoundNotebooks);
                    }
                    else if (Singleton<BaseGameManager>.Instance.FoundNotebooks < notebook_obtained && run_removed_notebooks > Singleton<BaseGameManager>.Instance.FoundNotebooks)
                    {
                        Singleton<BaseGameManager>.Instance.CollectNotebooks(Math.Min(notebook_obtained - Singleton<BaseGameManager>.Instance.FoundNotebooks, run_removed_notebooks));
                    }
                    var selected_item_index = player_itm_manager.selectedItem;
                    if (Input.GetKeyDown(KeyCode.F))
                    {
                        if (player_itm_manager.items[selected_item_index].itemType != Items.None)
                        {
                            items_queue.Add(player_itm_manager.items[selected_item_index].itemType);
                            player_itm_manager.RemoveItem(selected_item_index);
                            Singleton<CoreGameManager>.Instance.audMan.PlaySingle(sound_list["Sfx_Button_Press"]);
                        }
                    }
                    if (items_queue.Count() > 0)
                    {
                        if (player_itm_manager.Has(Items.None))
                        {
                            if (item_list.ContainsKey(items_queue[0]))
                            {
                                player_itm_manager.AddItem(item_list[items_queue[0]]);
                                items_queue.RemoveAt(0);
                            }
                            else
                            {
                                if (1 < items_queue.Count())
                                {
                                    items_queue.Add(items_queue[0]);
                                    items_queue.RemoveAt(0);
                                }
                            }
                        }
                    }
                    player_itm_manager.selectedItem = selected_item_index;
                    foreach (var soda in GameObject.FindObjectsOfType<SodaMachine>())
                    {
                        AccessTools.Field(typeof(SodaMachine), "item").SetValue(soda, player_itm_manager.nothing);
                        AccessTools.Field(typeof(SodaMachine), "potentialItems").SetValue(soda, new WeightedItemObject[0]);
                    }
                    if (option_values["doorsanity"] == 1)
                    {
                        foreach (var door in GameObject.FindObjectsOfType<Door>())
                        {
                            if (!door_list.Contains(door))
                            {
                                if (door.GetType().Name == "StandardDoor")
                                {
                                    // Logger.LogMessage(GetDoorObjectName(door));
                                    door_list.Add(door);
                                }
                                else if (door.GetType().Name == "SwingDoor")
                                {
                                    // Logger.LogMessage(GetSwingDoorObjectName(door));
                                    door_list.Add(door);
                                }
                            }
                            if (!door.locked)
                            {
                                if (door.GetType().Name == "StandardDoor")
                                {
                                    if (door.transform.parent.parent.parent.name != "Room13_Office")
                                    {
                                        if (!doors_obtained.Contains(GetDoorObjectName(door)))
                                        {
                                            if (!myLockedDoors.ContainsKey(GetDoorObjectName(door)))
                                            {
                                                door.Lock(true);
                                                myLockedDoors.Add(GetDoorObjectName(door), door);
                                            }
                                        }
                                    }
                                }
                                else if (door.GetType().Name == "SwingDoor")
                                {
                                    if (!doors_obtained.Contains(GetSwingDoorObjectName(door)))
                                    {
                                        if (!myLockedDoors.ContainsKey(GetSwingDoorObjectName(door)))
                                        {
                                            door.Lock(true);
                                            myLockedDoors.Add(GetSwingDoorObjectName(door), door);
                                        }
                                    }
                                }
                            }
                            else
                            {
                                if (myLockedDoors.ContainsValue(door))
                                {
                                    if (door.GetType().Name == "StandardDoor")
                                    {
                                        if (doors_obtained.Contains(GetDoorObjectName(door)))
                                        {
                                            door.Unlock();
                                            door.Shut();
                                            myLockedDoors.Remove(GetDoorObjectName(door));
                                        }
                                    }
                                    else if (door.GetType().Name == "SwingDoor")
                                    {
                                        if (doors_obtained.Contains(GetSwingDoorObjectName(door)))
                                        {
                                            door.Unlock();
                                            myLockedDoors.Remove(GetSwingDoorObjectName(door));
                                        }
                                    }
                                }
                            }
                        }
                        foreach (Elevator elevator in environment_controller.elevators)
                        {

                            // Logger.LogMessage(elevator.name + " " + MyPatches.GetDoorObjectName(elevator.Door));
                            if (elevator.Door.open && classic_game_manager.spoopMode)
                            {
                                if (!myLockedExits.ContainsKey(elevator.name))
                                {
                                    if (!doors_obtained.Contains(MyPatches.GetDoorObjectName(elevator.Door)))
                                    {
                                        elevator.Door.Shut();
                                        elevator.ColliderGroup.Enable(false);
                                        elevator.Close();
                                        myLockedExits.Add(elevator.name, elevator);
                                    }
                                }
                            }
                            else if (!elevator.Door.open && classic_game_manager.FoundNotebooks >= classic_game_manager.NotebookTotal && classic_game_manager.doorsUnlocked)
                            {
                                if (myLockedExits.ContainsKey(elevator.name))
                                {
                                    if (doors_obtained.Contains(MyPatches.GetDoorObjectName(elevator.Door)))
                                    {
                                        elevator.ColliderGroup.Enable(true);
                                        elevator.Open();
                                        myLockedExits.Remove(elevator.name);
                                    }
                                }
                            }
                        }
                    }
                }
            }
            else if (GameObject.FindObjectOfType<ClassicGameManager>() == null)
            {
                is_deathlinked = false;
                item_list = new Dictionary<Items, ItemObject>();
                items_queue = new List<Items>(items_obtained);
                door_list = new List<Door>();
                myLockedDoors = new Dictionary<string, Door>();
                run_removed_notebooks = 0;
            }
            if (GameObject.FindObjectOfType<MainMenu>() != null)
            {
                GameObject.FindObjectOfType<MainMenu>().transform.Find("Copyright").GetComponent<TextMeshProUGUI>().text = connect_status;
                GameObject.FindObjectOfType<MainMenu>().transform.Find("Version").GetComponent<TextMeshProUGUI>().text = "Archipelago Installed";
            }
        }
    }

    public class MyPatches
    {

        public static string GetDoorObjectName(Door thisDoor)
        {
            return thisDoor.transform.position.x.ToString() + ", " + thisDoor.transform.position.y.ToString() + ", " + thisDoor.transform.position.z.ToString();
        }

        public static Material lockedStandard;
        public static void StartPatches()
        {
            Harmony harmony = new Harmony(Plugin.pluginGuid);

            harmony.Patch(AccessTools.Method(typeof(Notebook), nameof(Notebook.Clicked)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(Notebook_MyPatch))));

            harmony.Patch(AccessTools.Method(typeof(Pickup), nameof(Pickup.Clicked)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(Pickup_MyPatch))));

            harmony.Patch(AccessTools.Method(typeof(SodaMachine), nameof(SodaMachine.InsertItem)), postfix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(InsertItem_MyPatch))));
            
            harmony.Patch(AccessTools.Method(typeof(ClassicGameManager), nameof(ClassicGameManager.LoadNextLevel)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(ClassicWin_MyPatch))));
            
            harmony.Patch(AccessTools.Method(typeof(StandardDoor), nameof(StandardDoor.UpdateTextures)), postfix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(StandDoorLockSet_Patch))));
            
            harmony.Patch(AccessTools.Method(typeof(StandardDoor), nameof(StandardDoor.Lock)), postfix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(StandDoorLock_Patch))));
           
            harmony.Patch(AccessTools.Method(typeof(Door), nameof(Door.OpenTimed)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(OnTriggerEnter_patch_standarddoor))));
            
            harmony.Patch(AccessTools.Method(typeof(BaseGameManager), "ElevatorClosed"), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(BaseManager_ElevatorClosed_Patch))));
            
            harmony.Patch(AccessTools.Method(typeof(ITM_Scissors), nameof(ITM_Scissors.Use)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(Scissors_Patch_Use))));
            
            harmony.Patch(AccessTools.Method(typeof(ITM_Quarter), nameof(ITM_Quarter.Use)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(Quarter_Patch_Use))));
            
            harmony.Patch(AccessTools.Method(typeof(StandardDoor), nameof(StandardDoor.InsertItem)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(StandardDoor_InsertItem_Patch))));
            
            harmony.Patch(AccessTools.Method(typeof(ITM_NoSquee), nameof(ITM_NoSquee.Use)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(NoSquee_Patch_Use))));
        
            harmony.Patch(AccessTools.Method(typeof(ITM_BSODA), nameof(ITM_BSODA.Use)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(Bsoda_Patch_Use))));
        
            harmony.Patch(AccessTools.Method(typeof(ITM_ZestyBar), nameof(ITM_ZestyBar.Use)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(ZestyBar_Patch_Use))));
        
            harmony.Patch(AccessTools.Method(typeof(ITM_AlarmClock), nameof(ITM_AlarmClock.Use)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(Clock_Patch_Use))));
        
            harmony.Patch(AccessTools.Method(typeof(ITM_Boots), nameof(ITM_Boots.Use)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(Boots_Patch_Use))));
        
            harmony.Patch(AccessTools.Method(typeof(ITM_SwingDoorLock), nameof(ITM_SwingDoorLock.Use)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(Lock_Patch_Use))));
        
            harmony.Patch(AccessTools.Method(typeof(ITM_Tape), nameof(ITM_Tape.Use)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(Tape_Patch_Use))));
        
            harmony.Patch(AccessTools.Method(typeof(ITM_Acceptable), nameof(ITM_Acceptable.Use)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(ITM_Acceptor_Use_Patch))));
        
            harmony.Patch(AccessTools.Method(typeof(CoreGameManager), nameof(CoreGameManager.EndGame)), prefix: new HarmonyMethod(AccessTools.Method(typeof(MyPatches), nameof(Death_Patch))));
        
        }

        public static void Death_Patch(CoreGameManager __instance, Transform player, Baldi baldi, bool fieldTrip)
        {
            if (Plugin.option_values["death_link"] == 1)
            {
                if (!Plugin.is_deathlinked)
                {
                    if (!baldi.transform.name.Contains("NULL"))
                    {
                        var string_list = new List<string>();
                        string_list.Add(Plugin.ap_slot + " died to a wooden ruler.");
                        string_list.Add(Plugin.ap_slot + " failed a teacher.");
                        string_list.Add(Plugin.ap_slot + " wasn't good at math.");
                        Plugin.deathLinkService.SendDeathLink(new DeathLink(Plugin.ap_slot, string_list[UnityEngine.Random.Range(1, string_list.Count) - 1]));
                    }
                    else
                    {
                        var string_list = new List<string>();
                        string_list.Add(Plugin.ap_slot + " should not have done that.");
                        string_list.Add(Plugin.ap_slot + " did not heed their advice.");
                        string_list.Add(Plugin.ap_slot + " didn't destroy the game.");
                        string_list.Add(Plugin.ap_slot + " dug too deep.");
                        Plugin.deathLinkService.SendDeathLink(new DeathLink(Plugin.ap_slot, string_list[UnityEngine.Random.Range(1, string_list.Count) - 1]));
                    }
                }
            }
        }

        public static void StandardDoor_InsertItem_Patch(StandardDoor __instance, PlayerManager player, EnvironmentController ec)
        {

        }

        public static void ITM_Acceptor_Use_Patch(ITM_Acceptable __instance, PlayerManager pm)
        {
            RaycastHit hits;
            if (Physics.Raycast(pm.transform.position, Singleton<CoreGameManager>.Instance.GetCamera(pm.playerNumber).transform.forward, out hits, pm.pc.reach, pm.pc.ClickLayers))
            {
                foreach (IItemAcceptor itemAcceptor in hits.transform.GetComponents<IItemAcceptor>())
                {
                    if (itemAcceptor != null && Traverse.Create(__instance).Field("item").GetValue<Items>() == Items.DetentionKey && itemAcceptor.ItemFits(Traverse.Create(__instance).Field("item").GetValue<Items>()))
                    {
                        Plugin.ap_session.Locations.CompleteLocationChecksAsync(72);
                    }
                    else if (itemAcceptor != null && Traverse.Create(__instance).Field("item").GetValue<Items>() == Items.Quarter && itemAcceptor.ItemFits(Traverse.Create(__instance).Field("item").GetValue<Items>()))
                    {
                        Plugin.ap_session.Locations.CompleteLocationChecksAsync(80);
                    }
                    else if (itemAcceptor != null && Traverse.Create(__instance).Field("item").GetValue<Items>() == Items.DoorLock && itemAcceptor.ItemFits(Traverse.Create(__instance).Field("item").GetValue<Items>()))
                    {
                        Plugin.ap_session.Locations.CompleteLocationChecksAsync(76);
                    }
                }
            }
        }

        public static void Tape_Patch_Use(ITM_Tape __instance, PlayerManager pm)
        {
            RaycastHit hits;
            if (Physics.Raycast(pm.transform.position, Singleton<CoreGameManager>.Instance.GetCamera(pm.playerNumber).transform.forward, out hits, pm.pc.reach, pm.pc.ClickLayers))
            {
                IItemAcceptor component = hits.transform.GetComponent<IItemAcceptor>();
                if (component != null && component.ItemFits(Items.Tape))
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(75);
                }
            }
        }

        public static void Lock_Patch_Use(ITM_SwingDoorLock __instance, PlayerManager pm)
        {
            RaycastHit hits;
            if (Physics.Raycast(pm.transform.position, Singleton<CoreGameManager>.Instance.GetCamera(pm.playerNumber).transform.forward, out hits, pm.pc.reach, pm.pc.ClickLayers))
            {
                IItemAcceptor component = hits.transform.GetComponent<IItemAcceptor>();
                if (component != null && component.ItemFits(Items.DoorLock))
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(76);
                }
            }
        }

        public static void Boots_Patch_Use(ITM_Boots __instance, PlayerManager pm)
        {
            Plugin.ap_session.Locations.CompleteLocationChecksAsync(79);
        }

        public static void Clock_Patch_Use(ITM_AlarmClock __instance, PlayerManager pm)
        {
            Plugin.ap_session.Locations.CompleteLocationChecksAsync(77);
        }

        public static void ZestyBar_Patch_Use(ITM_ZestyBar __instance, PlayerManager pm)
        {
            Plugin.ap_session.Locations.CompleteLocationChecksAsync(73);
        }

        public static void NoSquee_Patch_Use(ITM_NoSquee __instance, PlayerManager pm)
        {
            RaycastHit hits;
            if (Physics.Raycast(pm.transform.position, Singleton<CoreGameManager>.Instance.GetCamera(pm.playerNumber).transform.forward, out hits, pm.pc.reach, pm.pc.ClickLayers))
            {
                if (hits.transform.tag == "StandardDoor")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(78);
                }
                IItemAcceptor component2 = hits.transform.GetComponent<IItemAcceptor>();
                if (component2 != null && component2.ItemFits(Items.Wd40))
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(78);
                }
            }
        }

        public static void Quarter_Patch_Use(ITM_Quarter __instance, PlayerManager pm)
        {
            RaycastHit hits;
            if (Physics.Raycast(pm.transform.position, Singleton<CoreGameManager>.Instance.GetCamera(pm.playerNumber).transform.forward, out hits, pm.pc.reach, pm.pc.ClickLayers))
            {
                IItemAcceptor component = hits.transform.GetComponent<IItemAcceptor>();
                if (component != null && component.ItemFits(Items.Quarter))
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(80);
                }
            }
        }

        public static void Bsoda_Patch_Use(ITM_BSODA __instance, PlayerManager pm)
        {
            Plugin.ap_session.Locations.CompleteLocationChecksAsync(74);
        }

        public static void Scissors_Patch_Use(ITM_Scissors __instance, PlayerManager pm)
        {
            if (pm.jumpropes.Count > 0)
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(71);
            }
        }

        public static void OnTriggerEnter_patch_standarddoor(Door __instance, float time, bool makeNoise)
        {
            if (makeNoise && !__instance.locked)
            {
                if (MyPatches.GetDoorObjectName(__instance) == "245, 0, 365")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(82);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "195, 0, 325")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(51);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "75, 0, 325")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(52);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "205, 0, 225")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(53);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "145, 0, 225")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(81);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "175, 0, 75")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(50);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "215, 0, 35")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(49);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "135, 0, 35")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(48);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "245, 0, 65")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(83);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "75, 0, 195")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(70);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "215, 0, 265")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(69);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "275, 0, 125")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(68);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "145, 0, 155")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(67);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "115, 0, 95")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(66);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "95, 0, 45")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(65);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "275, 0, 195")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(64);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "275, 0, 335")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(63);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "55, 0, 305")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(62);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "145, 0, 265")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(61);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "195, 0, 155")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(60);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "185, 0, 65")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(59);
                }
                else if (MyPatches.GetDoorObjectName(__instance) == "165, 0, 55")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(58);
                }
            }
        }

        public static void BaseManager_ElevatorClosed_Patch(BaseGameManager __instance, Elevator elevator)
        {
            Plugin.Logger.LogMessage(elevator.name + " "+ MyPatches.GetDoorObjectName(elevator.Door));
            if (MyPatches.GetDoorObjectName(elevator.Door) == "45, 0, 225")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(55);
            }
            else if (MyPatches.GetDoorObjectName(elevator.Door) == "135, 0, 385")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(56);
            }
            else if (MyPatches.GetDoorObjectName(elevator.Door) == "305, 0, 215")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(54);
            }
            else if (MyPatches.GetDoorObjectName(elevator.Door) == "175, 0, 15")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(57);
            }
        }

        public static void StandDoorLockSet_Patch(StandardDoor __instance)
        {
            if (__instance.locked)
            {
                for (int i = 0; i < __instance.doors.Length; i++)
                {
                    MaterialModifier.ChangeHole(__instance.doors[i], __instance.mask[i], MyPatches.lockedStandard);
                }
            }
        }
        
        public static void StandDoorLock_Patch(StandardDoor __instance, bool cancelTimer)
        {
            __instance.Shut();
            for (int i = 0; i < __instance.doors.Length; i++)
            {
                MaterialModifier.ChangeOverlay(__instance.doors[i], MyPatches.lockedStandard);
            }
        }

        public static void ClassicWin_MyPatch(ClassicGameManager __instance)
        {
            Plugin.ap_session.Locations.CompleteLocationChecksAsync(54, 55, 56, 57);
            if (__instance.secretAvailable && Plugin.option_values["required_route"] == 1)
            {
                Plugin.ap_session.SetGoalAchieved();
            }
            else if (!__instance.secretAvailable && Plugin.option_values["required_route"] == 0)
            {
                Plugin.ap_session.SetGoalAchieved();
            }
            else if (Plugin.option_values["required_route"] == 2)
            {
                Plugin.ap_session.SetGoalAchieved();
            }
        }

        public static void Notebook_MyPatch(Notebook __instance)
        {
            if (__instance.transform.parent.name == "Room1_Classroom1")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(1, 27, 28, 29);
            }
            if (__instance.transform.parent.name == "Room2_Classroom2")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(2, 30, 31, 32);
            }
            if (__instance.transform.parent.name == "Room3_Classroom3")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(3, 33, 34, 35);
            }
            if (__instance.transform.parent.name == "Room4_Classroom4")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(4, 36, 37, 38);
            }
            if (__instance.transform.parent.name == "Room5_Classroom5")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(5, 39, 40, 41);
            }
            if (__instance.transform.parent.name == "Room6_Classroom6")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(6, 42, 43, 44);
            }
            if (__instance.transform.parent.name == "Room7_Classroom7")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(7, 45, 46, 47);
            }
        }
        public static void InsertItem_MyPatch(SodaMachine __instance, PlayerManager pm, EnvironmentController ec)
        {
            if (__instance.transform.parent.parent.name == "Room11_Faculty4")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(14);
            }
            if (__instance.transform.parent.parent.name == "Room14_Cafeteria")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(25);
            }
            if (__instance.transform.parent.parent.name == "Room0_Hallway")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(17);
            }
        }

        public static bool Pickup_MyPatch(Pickup __instance)
        {
            bool sent_loc = false;
            if (__instance.transform.parent.name == "ClassicHappyBaldi(Clone)")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(8);
                sent_loc = true;
            }
            if (__instance.transform.parent.name == "Room3_Classroom3")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(19);
                sent_loc = true;
            }
            if (__instance.transform.parent.name == "Room4_Classroom4")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(20);
                sent_loc = true;
            }
            if (__instance.transform.parent.name == "Room5_Classroom5")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(21);
                sent_loc = true;
            }
            if (__instance.transform.parent.name == "Room7_Classroom7")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(22);
                sent_loc = true;
            }
            if (__instance.transform.parent.name == "Room8_Faculty1")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(9);
                sent_loc = true;
            }
            if (__instance.transform.parent.name == "Room9_Faculty2")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(10);
                sent_loc = true;
            }
            if (__instance.transform.parent.name == "Room10_Faculty3")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(11);
                sent_loc = true;
            }
            if (__instance.transform.parent.name == "Room15_Closet")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(23);
                sent_loc = true;
            }
            if (__instance.transform.parent.parent.name == "Room0_Hallway")
            {
                Plugin.ap_session.Locations.CompleteLocationChecksAsync(18);
                sent_loc = true;
            }
            if (__instance.transform.parent.name == "Room11_Faculty4")
            {
                if (__instance.gameObject.name == "Item_DetentionKey")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(12);
                    sent_loc = true;
                }
                else
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(13);
                    sent_loc = true;
                }
            }
            if (__instance.transform.parent.name == "Room12_Faculty5")
            {
                if (__instance.gameObject.name == "Item_AlarmClock")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(15);
                    sent_loc = true;
                }
                else
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(16);
                    sent_loc = true;
                }
            }
            if (__instance.transform.parent.name == "Room14_Cafeteria")
            {
                if (__instance.gameObject.name == "Item_Bsoda")
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(26);
                    sent_loc = true;
                }
                else
                {
                    Plugin.ap_session.Locations.CompleteLocationChecksAsync(24);
                    sent_loc = true;
                }
            }

            if (sent_loc)
            {
                __instance.gameObject.SetActive(false);
                if (__instance.icon != null)
                {
                    __instance.icon.sprite.enabled = false;
                }
                return false;
            }
            return true;
        }
    }

}
