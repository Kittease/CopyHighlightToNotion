import json
import keyboard
import pyautogui
import pyperclip
import requests
import sys
import time
from win32gui import GetWindowText, GetForegroundWindow



def notion_page(title, content):
    return {
        "parent":{
            "database_id": databaseId
        },
        "properties":{
            "Name":{
                "title":[
                    {
                        "text":{
                            "content": title
                        }
                    }
                ]
            }
        },
        "children":[
            {
                "object":"block",
                "type":"paragraph",
                "paragraph":{
                    "rich_text":[
                        {
                            "type":"text",
                            "text":{
                                "content": content
                            }
                        }
                    ]
                }
            }
        ]
    }


def copy_clipboard():
    pyperclip.copy("")
    pyautogui.hotkey("ctrl", "c")
    time.sleep(.1)
    return pyperclip.paste()


def copy_to_notion():
    title = GetWindowText(GetForegroundWindow())
    content = copy_clipboard()

    data = json.dumps(notion_page(title, content))
    res = requests.request("POST", createUrl, headers=headers, data=data)

    print("Created new page" if res.status_code == 200 else "Something went wrong")



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide your Notion API key and the Database ID")
        exit()

    createUrl = "https://api.notion.com/v1/pages"
    token = sys.argv[1]
    databaseId = sys.argv[2]
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16"
    }

    keyboard.add_hotkey("ctrl+f10", copy_to_notion) 
    keyboard.wait()