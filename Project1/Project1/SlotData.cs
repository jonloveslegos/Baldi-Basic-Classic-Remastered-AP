using System.Collections.Generic;
using Newtonsoft.Json.Linq;
using UnityEngine;

namespace BaldiAP;

public class SlotData
{
    public readonly bool DeathLink;
    public readonly int RequiredRoute;
    public readonly bool RandomParty;
    public readonly bool RandomDemo;
    public readonly int StartingStyle;
    public readonly int ReqGoal;
    public readonly bool ExtraNotebookChecks;
    public readonly bool Doorsanity;
    public readonly bool ItemUsage;
    public readonly bool GlitchedNotebook;
    public SlotData(Dictionary<string, object> slotDict)
    {
        foreach (var x in slotDict) BaldiConsole.Instance.DebugLog($"{x.Key} {x.Value}");
        if (slotDict.TryGetValue("death_link", out var rawDeathLink) &&
            rawDeathLink is JObject deathLink)
            DeathLink = deathLink.Value<bool>();
        if (slotDict.TryGetValue("required_route", out var rawRequiredRoute) && 
            rawRequiredRoute is JObject requiredRoute)
            RequiredRoute = requiredRoute.Value<int>();
        if (slotDict.TryGetValue("party", out var rawParty) && 
            rawParty is JObject party)
            RandomParty = party.Value<bool>();
        if (slotDict.TryGetValue("demo", out var rawDemo) && 
            rawDemo is JObject demo)
            RandomDemo = demo.Value<bool>();
        if (slotDict.TryGetValue("which_style", out var rawWhichStyle) && 
            rawWhichStyle is JObject whichStyle)
            StartingStyle = whichStyle.Value<int>();
        if (slotDict.TryGetValue("req_style", out var rawReqStyle) && 
            rawReqStyle is JObject reqStyle)
            ReqGoal = reqStyle.Value<int>();
        if (slotDict.TryGetValue("notechecks", out var rawNoteChecks) && 
            rawNoteChecks is JObject noteChecks)
            ExtraNotebookChecks = noteChecks.Value<bool>();
        if (slotDict.TryGetValue("doorsanity", out var rawDoorsanity) && 
            rawDoorsanity is JObject doorsanity)
            Doorsanity = doorsanity.Value<bool>();
        if (slotDict.TryGetValue("item_usage", out var rawItemUsage) && 
            rawItemUsage is JObject itemUsage)
            ItemUsage = itemUsage.Value<bool>();
        if (slotDict.TryGetValue("gnotebooks", out var rawGNotebooks) && 
            rawGNotebooks is JObject gNotebooks)
            GlitchedNotebook = gNotebooks.Value<bool>();
    }
}