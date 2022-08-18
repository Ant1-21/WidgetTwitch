""" It imports the modules:
**json** to transform requests json to python dict,
**re** to transfor strings using regular expression,
**sys** to send html output to the widget,
**numerize** to convert large numbers into readable strings,
and **requests** to get Twitch channels informations through API.
"""
import json
import re
import sys
from numerize import numerize
import requests as rq


ID = "<Your Client ID>"
TOKEN = "<Your Token>"


class Channel:
    """This class is used to store information about a Twitch channel"""

    def __init__(self, login: str):
        self.channel_id: int = 0
        self.login: str = login
        self.name: str = ""
        self.live: bool = False
        self.image: str = ""
        self.game: str = ""
        self.viewer: int = 0

    def __str__(self):
        """
        The __str__ function is a special function
        that is called when you print an object

        :return: A string with the channel name, whether
        it is live, and the number of viewers.
        """
        return (
            f"Channel :\n\tName: {self.name}\n\t"
            f"Live: {self.live}\n\tViewers: {self.viewer}"
        )

    def tohtml(self) -> str:
        """
        It returns a string that contains the HTML code of the streamer's card

        :return: A string
        """
        if self.live:
            nbviewers = re.sub(
                r"([0-9,]*)([KM])",
                r"\1&nbsp;\2",
                numerize.numerize(self.viewer, 1)
            ).lower()
            witchgame: str = f"<p>{self.game}</p>"
            islive: str = (
                "<p class='live'>&#128308;&nbsp;</p>"
                f"<p>{nbviewers}</p>"
            )
        else:
            witchgame: str = ""
            islive: str = "<p class='disconnected'>Déconnecté(e)</p>"
        return f"""
<div class="main">
    <a href="https://www.twitch.tv/{self.login}">
        <div class="frame">
            <img
                style="filter: grayscale({"0" if self.live else "100%"});"
                src="{self.image}"
            />
            <div class="text">
                <p style="font-weight: bold;">{self.name}</p>
                {witchgame}
            </div>
            <div class="spec">{islive}</div>
        </div>
    </a>
</div>
"""


def get_channels_info(channels_name, channels_list) -> int:
    """
    It takes a list of channel names and a list of channels,
    and it fills the list of channels with the information of
    the channels in the list of channel names

    :param channels_name: a list of the channels you want to get info for
    :param channels_list: list of Channel objects
    :return: An integer status code
    """
    try:
        url = "https://api.twitch.tv/helix/users?"
        for i, user in enumerate(channels_name):
            if i > 0:
                url += "&"
            url += f"login={user}"
        response = rq.get(
            url, headers={"Authorization": f"Bearer {TOKEN}", "Client-Id": ID}
        )
    except rq.exceptions.RequestException:
        return 1

    if response.status_code != 200:
        return 1

    jsn: dict = json.loads(response.text)
    if len(jsn["data"]) == 0:
        return 1

    for name in channels_name:
        for data in jsn["data"]:
            if name.lower() == data["login"].lower():
                channel = Channel(data["login"])
                channel.channel_id = data["id"]
                channel.login = data["login"]
                channel.name = data["display_name"]
                channel.image = data["profile_image_url"]
                channels_list.append(channel)
    return 0


def channels_live(channels_list) -> int:
    """
    It takes a list of channels and checks if they are live

    :param channels_list: list of Channel objects
    :return: An integer status code
    """
    for channel in channels_list:
        if channel.channel_id is None:
            return 1
    try:
        url = "https://api.twitch.tv/helix/streams?"
        for i, channel in enumerate(channels_list):
            if i > 0:
                url += "&"
            url += f"user_id={channel.channel_id}"
        response = rq.get(
            url, headers={"Authorization": f"Bearer {TOKEN}", "Client-Id": ID}
        )
    except rq.exceptions.RequestException:
        return 1

    if response.status_code != 200:
        return 1

    jsn: dict = json.loads(response.text)
    if len(jsn["data"]) > 0:
        for data in jsn["data"]:
            for channel in channels_list:
                if channel.channel_id == data["user_id"]:
                    channel.live = True
                    channel.game = data["game_name"]
                    channel.viewer = int(data["viewer_count"])
    return 0


def main():
    """
    It reads the channels.txt file, gets the channel info
    and live status for each channel, sorts them by viewer
    count, and outputs the HTML

    :return: the html code for the widget.
    """
    try:
        rq.get('https://1.1.1.1')
    except rq.exceptions.RequestException:
        sys.stdout.write("<div class='error'>"
                         "&#9888;&nbsp;Not connected.</div>")
        return

    channels_list: list = []
    channels_name: list = []

    with open("Twitch.widget/channels.txt", encoding="utf-8") as file:
        channels_name.extend(line.strip() for line in file)

    if get_channels_info(channels_name, channels_list):
        sys.stdout.write("<div class='error'>An error has occurred.</div>")

    if channels_live(channels_list):
        sys.stdout.write("<div class='error'>An error has occurred.</div>")

    channels_list.sort(key=lambda x: x.viewer, reverse=True)

    for channel in channels_list:
        sys.stdout.write(channel.tohtml())


if __name__ == "__main__":
    main()
