# Twitch channels Übersicht Widgets

<p align="center">
    <img src="screenshot.png" alt="Screenshot" width="600"/>
</p>

## Get Twitch credentials

- Create a Twitch app in [Twitch console](https://dev.twitch.tv/console) following this [tutorial](https://dev.twitch.tv/docs/api/get-started)
- Get your Client identifier.
- Generate a new Client secret.
- Create a `.env` file in app directory.
- Set your Client ID and Secret in `.env` file like in the example below.

```bash
ID=<your-client-id>
SECRET=<your-client-secret>
```

## Install python modules requirements

```bash
pip3 install -r requirements.txt
```

## How to change the channels list

Add the different channels names to the ```channels.txt``` file.
