#! /usr/bin/env ptyhon3

import base64, pymsteams

def teams_notifications(text_to_card):
    encoded_teams_url = b'aHR0cHM6Ly9maXVkaXQud2ViaG9vay5vZmZpY2UuY29tL3dlYmhvb2tiMi9kODY2Y2M0YS1lOTFiLTRhOWItYTNkZi1jYmNlYzY3NWNlMGFAYWM3OWU1YTgtZTBlNC00MzRiLWEyOTItMmM4OWI1YzI4MzY2L0luY29taW5nV2ViaG9vay    9jOWU3MDJiZjZlMDc0OTFlOWNjMjRkMGRjM2UxYzhkYS81ZTliZDUyOS02YjYxLTQzYTItYmZkMy05MzJlMzRlNTQ2M2E='
    teams_url = (base64.b64decode(encoded_teams_url)).decode('ascii')
    card = pymsteams.connectorcard(teams_url)
    card.text(text_to_card)
    # card.printme()
    card.send()