
# Our Key mappings
known_maps = {
    'BTN_BASE': 'cross',
    'BTN_TRIGGER':'left',
    'BTN_TOP2':'triangle',
    'BTN_THUMB2':'up',
    'BTN_THUMB':'down',
    'BTN_PINKIE':'square',
    'BTN_TOP':'right',
    'BTN_BASE2':'circle',
    'BTN_BASE3':'select',
    'BTN_BASE4':'start'
}

# Takes an event and coverts it to the form:
# (Key, State)
def map_input(event):
    if event.ev_type != "Key": return None
    return (known_maps[event.code], [False, True][event.state])
