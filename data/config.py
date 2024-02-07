# - *- coding: utf- 8 - *-
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
BOT_TOKEN = config["settings"]["token"]
admins = config["settings"]["admin_id"]
ctypro_bot_token = config["settings"]["ctypro_bot_token"]

if "," in admins:
    admins = admins.split(",")
elif len(admins) >= 1:
    admins = [admins]
else:
    admins = []
    print("***** Вы не указали админ ID *****")

if not ctypro_bot_token:
    print("***** Вы не указали CryptoBot Token *****")


bot_version = "2.3"
bot_description = f"<b>♻ Bot created by @static_assert</b>\n" \
                  f"<b>⚜ Bot Version:</b> <code>{bot_version}</code>\n" \
                  f"<b>🍩 Donate to the author:</b> <a href='https://t.me/send?start=IVTFNZEEFaFx'><b>Click me</b></a>"
