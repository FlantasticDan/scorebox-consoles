# ScoreBox Consoles
[![PyPI version](https://badge.fury.io/py/scorebox-consoles.svg)](https://badge.fury.io/py/scorebox-consoles)

Python interface for scoreboard consoles manufactured by Daktronics and Colorado Time Systems

## Supported Consoles
- Daktronics All Sport 5000
    - :basketball: Basketball
    - :football: Football
    - :volleyball: Volleyball
    - :water_polo: Water Polo
    - :wrestling: Wrestling
- Colorado Time Systems System 6
    - :water_polo: Water Polo

## Installation
`pip install scorebox-consoles`

## Usage
```python
from consoles.sports import Basketball

if __name__ == '__main__':
    basketball = Basketball('COM1')
    game_state = basketball.export()
```
*Calls to sport class must be protected by an `if __name__ == '__main__'` because the serial connection is read in a seperate process*

### Connecting a Console
Consoles are connected with via a Serial to USB cable.

**Daktronics All Sport 5000** - Connect to the port labeled I/O Port (J6) with a DB25 to DB9 Serial connector

**Colorado Time Systems System 6** - Tap into the 1/4" Scoreboard Out plug and connect the tip to pin 2 of a Serial DB9 connector and the shoe to pin 5.

### API
Sport classes take a serial port string as an argument and expose an `export` method that returns the current game state.  All sport classes also feature an `on_update` method that is designed to be reimplemented.  It is called everytime the state of the game changes, depending on the settings of the console, this can work out to be 10 times per second or faster.  `on_update` must take a single variable, a Python dictionary that corresponds to the game state values described below for each sport.
```python
from consoles.sports import Football

def do_something(game_state):
    # Do something useful with the parse score console information
    # For example:
    home = game_state['home_score']
    visitor = game_state['visitor_score']
    if home > visitor:
        print(f'The Home Team leads {home} to {visitor}.')
    elif visitor > home:
        print(f'The Visiting Team leads {visitor} to {home}.')
    else:
        print(f'The teams are tied at {home}')

if __name__ == '__main__':
    football = Football('COM1')
    football.on_update = do_something
```

#### :basketball: Basketball
| Key | Type | Description |
| --- | --- | --- |
| `{home/visitor}_score` | int | Team Score |
| `{home/visitor}_timeouts` | int | Team Timeouts Remaining |
| `{home/visitor}_fouls` | int | Team Fouls |
| `{home/visitor}_possesion` | bool | Team Possesion Status |
| `{home/visitor}_bonus` | bool | Team Bonus (1-on-1) Status |
| `{home/visitor}_double_bonus` | bool | Team Double Bonus (2 shots) Status |
| `clock` | str | Main Clock Time (excludes timeout time), Tenths shown under 1 minute if configured in console settings |
| `shot` | str | Shot Clock Time, Tenths shown under 5 seconds if configured in console settings |
| `period` | str | Game Period |

#### :football: Football
| Key | Type | Description |
| --- | --- | --- |
| `{home/visitor}_score` | int | Team Score |
| `{home/visitor}_timeouts` | int | Team Timeouts Remaining |
| `{home/visitor}_possesion` | bool | Team Possesion Status |
| `clock` | str | Main Clock Time |
| `play` | str | Play Clock Time |
| `quarter` | str | Game Quarter |
| `down` | str | Down Number (includes ordination [ex. `1ST`]) |
| `to_go`| int | Yards For First Down |
| `ball_on` | int | Ball Location on the Field (does not include side of field) |
| `flag` | bool | Flag Status (only updated on console button push) |

#### :volleyball: Volleyball
| Key | Type | Description |
| --- | --- | --- |
| `{home/visitor}_score` | int | Team Score in Current Game |
| `{home/visitor}_sets` | int | Team Sets Won |
| `current_set` | int | Game Set |

#### :water_polo: Water Polo
| Key | Type | Description |
| --- | --- | --- |
| `{home/visitor}_score` | int | Team Score |
| `clock` | str | Main Clock Time |
| `shot` | str | Shot Clock Time |
| `period` | str | Game Period |

*Water Polo is supported on both Daktronics and Colorado Time Systems consoles: for Daktronics call `WaterPoloDaktronics`, for Colorado Time Systems call `WaterPolo`*