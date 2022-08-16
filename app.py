""" It imports the modules:
json to transform requests json to python dict,
re to transfor strings using regular expression,
sys to send html output to the widget,
numerize to convert large numbers into readable strings,
and requests to get Twitch channels informations through API.
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
        self.__init_name = login
        self.channel_id: int = 0
        self.login: str = ""
        self.name: str = ""
        self.live: bool = False
        self.image: str = ""
        self.offline_image: str = ""
        self.game: str = ""
        self.viewer: str = ""

    def __str__(self):
        """
        This function returns a string that contains the login,
        name, id, live status, image, and game of the channel
        """
        return (
            f"Channel :\n\tLogin: {self.login}\n\tName: {self.name}\n\t"
            f"Id: {self.channel_id}\n\tLive: {self.live}\n\t"
            f"Image: {self.image}\n\tGame: {self.game}\n"
        )

    def get_channel_info(self) -> None:
        """
        It gets the channel's information from the Twitch API and
        stores it in the class
        """
        jsn: dict = json.loads(
            rq.get(
                f"https://api.twitch.tv/helix/users?login={self.__init_name}",
                headers={"Authorization": f"Bearer {TOKEN}", "Client-Id": ID},
            ).text
        )
        data: dict = jsn["data"][0]
        self.channel_id = data["id"]
        self.login = data["login"]
        self.name = data["display_name"]
        self.image = data["profile_image_url"]
        self.offline_image = data["profile_image_url"]
        # self.offlineImage = data["offline_image_url"]

    def islive(self) -> None:
        """
        It checks if the user is live, and if they are, it sets the
        `live` attribute to `True`, and sets the `game` and `viewer`
        attributes to the game they're playing and the number of viewers
        they have, respectively
        """
        if self.channel_id is not None:
            jsn: dict = json.loads(
                rq.get(
                    "https://api.twitch.tv/helix/streams?"
                    f"user_id={self.channel_id}",
                    headers={
                        "Authorization": f"Bearer {TOKEN}",
                        "Client-Id": ID
                    },
                ).text
            )
            if len(jsn["data"]) > 0:
                self.live = True
                self.game = jsn["data"][0]["game_name"]
                self.viewer = re.sub(
                    r"([0-9,]*)([KM])",
                    r"\1&nbsp;\2",
                    numerize.numerize(jsn["data"][0]["viewer_count"]),
                )

    def tohtml(self) -> str:
        """
        It returns a string that contains the HTML code of the streamer's card
        :return: A string
        """
        witchgame: str = f"<p>{self.game}</p>" if self.live else ""
        islive: str = (
            f"<p class='live'>&#x2022;&nbsp;</p><p>{self.viewer}</p>"
            if self.live
            else "<p class='disconnected'>Déconnecté(e)</p>"
        )
        return f"""
<div class="main">
    <a href="https://www.twitch.tv/{self.login}">
        <div class="frame">
            <img src="{self.image if self.live else self.offline_image}"/>
            <div class="text">
                <p style="font-weight: bold;">{self.name}</p>
                {witchgame}
            </div>
            <div class="spec">{islive}</div>
        </div>
    </a>
</div>
"""


def main():
    """
    It reads the channels.txt file, creates a Channel object for each line,
    gets the channel info, checks if the channel is live, and then writes
    the HTML for each channel to stdout
    """
    channels = []
    with open("Twitch.widget/channels.txt", encoding="utf-8") as file:
        channels.extend(Channel(line.strip()) for line in file)
    for channel in channels:
        channel.get_channel_info()
        channel.islive()
        sys.stdout.write(channel.tohtml())


if __name__ == "__main__":
    main()
