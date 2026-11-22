using System.IO;
using JetBrains.Annotations;
using Newtonsoft.Json;
using UnityEngine;

namespace BaldiAP;

public class CustomSaveData
{
    public int ItemIndex;
}

public class CustomSaveDataHandler : MonoBehaviour
{
    [CanBeNull] public static CustomSaveData Data;
    
    public static void Save()
    {
        if (!Main.ArchipelagoHandler?.IsConnected ?? true)
            return;
        Data ??= new CustomSaveData();
        var saveFolder = Application.persistentDataPath + "/ArchipelagoSaves";
        if (!Directory.Exists(saveFolder))
            Directory.CreateDirectory(saveFolder);
        var path = Path.Combine(saveFolder,
            $"Custom{Main.ArchipelagoHandler.seed}{Main.ArchipelagoHandler.SlotName}.json");
        var text = JsonConvert.SerializeObject(Data, Formatting.Indented);
        File.WriteAllText(path, text);
    }

    public static void Load()
    {
        if (!Main.ArchipelagoHandler?.IsConnected ?? true)
            return;
        var saveFolder = Application.persistentDataPath + "/ArchipelagoSaves";
        var path = Path.Combine(saveFolder, $"Custom{Main.ArchipelagoHandler.seed}{Main.ArchipelagoHandler.SlotName}.json");
        if (!File.Exists(path))
            Save();
        var json = File.ReadAllText(path);
        var tempData = JsonConvert.DeserializeObject<CustomSaveData>(json);
        if (tempData == null)
            return;
        Data = tempData;
        Main.ItemHandler.FlushQueue();
    }
}