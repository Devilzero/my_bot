import os
import json

if not os.getenv("bot_version"):
    config_json = os.path.realpath(__file__+"/../../conf/config.json")

    with open(config_json, "r") as f:
        config = json.load(f)
    os.environ.update(config)