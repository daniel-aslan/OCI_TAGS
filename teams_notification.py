#! /usr/bin/env ptyhon3

import base64, pymsteams

def teams_notifications(text_to_card):
    encoded_teams_url = b'XXXXXXXXXXXXXXXXX'
    teams_url = (base64.b64decode(encoded_teams_url)).decode('ascii')
    card = pymsteams.connectorcard(teams_url)
    card.text(text_to_card)
    # card.printme()
    card.send()
