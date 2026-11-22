using System;
using System.Collections.Generic;
using Archipelago.MultiClient.Net.Models;
using UnityEngine;
namespace BaldiAP;

public class ItemHandler : MonoBehaviour
{
    public enum BaldiItems : int
    {
        BSODA = 3
    }
    
    private Queue<(int, ItemInfo)> cachedItems;

    private void Awake()
    {
        cachedItems = new Queue<(int, ItemInfo)>();
    }

    public void HandleItem(int itemIndex, ItemInfo item)
    {
        try
        {
            if (CustomSaveDataHandler.Data == null)
                cachedItems.Enqueue((itemIndex, item));
            if (CustomSaveDataHandler.Data == null || itemIndex < CustomSaveDataHandler.Data.ItemIndex)
                return;
            if (cachedItems.Count > 0)
                FlushQueue();
            CollectItem(itemIndex, item);
        }
        catch (Exception ex)
        {
            BaldiConsole.Instance.Log($"[HandleItem ERROR] {ex.Message}]");
            throw;
        }

    }

    public void FlushQueue()
    {
        while (cachedItems.Count > 0)
        {
            var (itemIndex, item) = cachedItems.Dequeue();
            CollectItem(itemIndex, item);
        }
    }

    public void CollectItem(int index, ItemInfo item)
    {
        Main.logger.LogInfo($"CollectItem: {index} -> {item.ItemName}");
        BaldiConsole.Instance.DebugLog($"CollectItem: {index} -> {item.ItemId}");
        var customSaveDataHandler = CustomSaveDataHandler.Data;
        if  (index < customSaveDataHandler.ItemIndex)
            return;
        customSaveDataHandler.ItemIndex++;
        switch ((BaldiItems)item.ItemId)
        {
            case BaldiItems.BSODA:
                BaldiConsole.Instance.DebugLog($"SODAAAA!!");
                break;
        }
    }
}