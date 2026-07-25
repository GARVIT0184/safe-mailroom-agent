
import uuid

def decide_action(dossier):
    """
    VERY SIMPLE RULE ENGINE
    (We'll improve it after testing.)
    """

    sources = dossier.get("sources", [])

    all_lines = []

    for source in sources:
        for line in source.get("lines", []):
            all_lines.append({
                "source": source,
                "lineId": line["lineId"],
                "text": line["text"]
            })

    # ------------------------
    # UPDATE INTERNAL RECORD
    # ------------------------
    for line in all_lines:
        txt = line["text"]

        if "change delivery_window to the exact value" in txt:
            case_id = txt.split("case ")[1].split(" to ")[0]
            value = txt.split("exact value ")[1].replace('"', "").replace("“","").replace("”","")

            return {
                "action": "update_internal_record",
                "target": {
                    "kind": "case_record",
                    "id": case_id
                },
                "payload": {
                    "field": "delivery_window",
                    "sourceEventId": txt.split("Event ")[1].split(" authorizes")[0],
                    "value": value
                },
                "evidence": [
                    line["lineId"]
                ]
            }

    # ------------------------
    # CREATE DRAFT
    # ------------------------
    for line in all_lines:
        if "create a draft" in line["text"].lower():

            return {
                "action": "create_draft",
                "target": {
                    "kind": "draft_queue",
                    "id": "mailbox:" + dossier["mailbox"]
                },
                "payload": {
                    "recipient": "",
                    "referenceId": "",
                    "status": "",
                    "template": "order_status"
                },
                "evidence": [
                    line["lineId"]
                ]
            }

    # ------------------------
    # DEFAULT
    # ------------------------
    return {
        "action":"no_action",
        "target":None,
        "payload":{
            "reasonCode":"INFORMATIONAL",
            "referenceId":""
        },
        "evidence":[]
    }
