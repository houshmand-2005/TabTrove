import json
import os
import subprocess
import sys
from functools import lru_cache

import lz4.block as lz4
from rich.console import Console
from rich.prompt import Prompt

console = Console()

base_config = {
    "browsers": {
        "firefox": {"excitable_path": "", "profile_path": ""},
        "edge": {"excitable_path": ""},
    },
    "collections": {},
}


def create_valid_config() -> None:
    """still in progress"""
    with open("config.json", "w", encoding="utf-8") as config_file:
        config_file.write(json.dumps(base_config, indent=2))
    read_config_file.cache_clear()


@lru_cache()
def read_config_file() -> dict | None:
    """read config file"""
    if os.path.isfile("config.json"):
        try:
            with open("config.json", "r", encoding="utf-8") as config_file:
                return json.load(config_file)
        except json.decoder.JSONDecodeError as error:
            console.print(f"[red]{error}[/red]\nMake sure the json file Correct")
            console.rule()
            console.print(
                r"If You Are Using Windows Be sure to use \\ "
                + r"instead of \ when placing the path of the files "
                + "Like this:\n"
                + r"[red]Wrong :[/red] C:\Program Files\Mozilla Firefox\firefox.exe"
                + "\n"
                + r"[green]correct :[/green] C:\\Program Files\\Mozilla Firefox\firefox.exe"
            )
            sys.exit()
    else:
        create_valid_config()
        return None


def get_browser_profile_path() -> str:
    "return profile path"
    existing_data = read_config_file()
    if not existing_data:
        console.print("[red][bold]Your Browser Path Is Wrong![/bold][/red]")
        sys.exit()
    # TODO: Support Other Browsers
    match os.name:
        case "nt":
            recovery_path = r"\recovery.jsonlz4"
            previous_path = r"\previous.jsonlz4"
        case "posix":
            recovery_path = "/recovery.jsonlz4"
            previous_path = "/previous.jsonlz4"
    input_file = existing_data["browsers"]["firefox"]["profile_path"] + recovery_path
    if not os.path.isfile(input_file):
        input_file = (
            existing_data["browsers"]["firefox"]["profile_path"] + previous_path
        )
    return input_file


def get_browser_profile() -> str:
    """decompress browser profile file"""
    input_file = get_browser_profile_path()
    in_full_name = os.path.basename(input_file)
    try:
        in_file_handle = open(input_file, "rb")
    except FileNotFoundError:
        console.print("[red][bold]Profile Not Found![/bold][/red]")
        sys.exit()
    console.print(f"Trying To Decompress [green]{in_full_name}[/green]")
    assert in_file_handle.read(8) == b"mozLz40\0"
    decompress = lz4.decompress(in_file_handle.read())
    in_file_handle.close()
    return decompress


def extract_data(collection_name: str) -> dict:
    """extract data form browser profile"""
    json_parsed_data = json.loads(get_browser_profile())
    data = json_parsed_data["windows"][0]["tabs"]
    json_parsed_data = {
        collection_name: {
            entry["entries"][i]["ID"]: {
                "url": entry["entries"][i]["url"],
                "title": entry["entries"][i]["title"],
            }
            for entry in data
            for i, _ in enumerate(entry["entries"])
        }
    }
    return json_parsed_data


def show_browsers() -> str:
    """show browsers list and return the path of that browser"""
    console.clear()
    json_parsed_data = read_config_file()
    console.print("Select a Browsers:")
    browsers_list = []
    for index, browsers in enumerate(json_parsed_data["browsers"]):
        browsers_list.append(browsers)
        console.print(f"{index+1}) [bold]{browsers}[/bold]")
    console.rule()
    choice = Prompt.ask(
        "Enter the number",
        choices=[str(i + 1) for i in range(len(json_parsed_data["browsers"]))],
    )
    return json_parsed_data["browsers"][browsers_list[int(choice) - 1]][
        "excitable_path"
    ]


def show_titles(collection_name: str) -> None:
    """show titles of selected collections"""
    existing_data = read_config_file()
    site_titles = [
        entry["title"]
        for entry in existing_data["collections"][collection_name].values()
    ]
    console.clear()
    for index, title in enumerate(site_titles, start=1):
        console.print(f"{index}) {title}")


def show_collections() -> str:
    """show the all collections and return the selected collection"""
    console.clear()
    json_parsed_data = read_config_file()
    if not json_parsed_data or json_parsed_data["collections"] == {}:
        console.print("[red][bold]No Collections Found![/bold][/red]")
        sys.exit()
    collection_names = list(json_parsed_data["collections"].keys())
    console.print("Select a Collection:")
    for index, collection_name in enumerate(collection_names, start=1):
        console.print(f"{index}) {collection_name}")
    console.rule()
    choice = Prompt.ask(
        "Enter the number",
        choices=[str(i) for i in range(1, len(collection_names) + 1)],
    )
    return collection_names[int(choice) - 1]


def add_collection() -> None:
    """Add a Collection"""
    existing_data = read_config_file()
    console.clear()
    collection_name = input("Enter the name for this collection: ")
    json_parsed_data = extract_data(collection_name)
    existing_data["collections"].update(json_parsed_data)
    show_titles(collection_name)
    console.rule()
    choice = Prompt.ask(
        f"Are You Sure To Save [bold]{collection_name}[/bold] Collection",
        choices=["y", "n"],
    )
    match choice.lower():
        case "y":
            pass
        case _:
            sys.exit()
    with open("config.json", "w", encoding="utf-8") as config_file:
        config_file.write(json.dumps(existing_data, indent=2))
    read_config_file.cache_clear()


def open_collection() -> None:
    """Open Selected Collection"""
    json_parsed_data = read_config_file()
    selected_collection = show_collections()
    browser_path = show_browsers()
    cmdline = [browser_path]
    console.print(f"Open [green][bold]{selected_collection}[/bold][/green] Collection")
    for url_data in json_parsed_data["collections"][selected_collection].values():
        cmdline.append(url_data["url"])
    try:
        subprocess.Popen(cmdline)
    except Exception:
        console.print("[red][bold]Your Browser Path Is Wrong![/bold][/red]")


console.print("1) Open a Collection\n2) Add a Collection")
console.rule()
MENU_CHOICE = Prompt.ask(
    "Enter the number",
    choices=["1", "2"],
)
match MENU_CHOICE:
    case "1":
        open_collection()
    case "2":
        add_collection()
