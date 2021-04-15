# ScoreBox Consoles
[![PyPI version](https://badge.fury.io/py/scorebox-consoles.svg)](https://badge.fury.io/py/scorebox-consoles)

Python interface for scoreboard consoles manufactured by Daktronics and Colorado Time Systems

## Supported Consoles
- Daktronics All Sport 5000
    - :basketball: Basketball
    - :football: Football
    - :volleyball: Volleyball
    - :water_polo: Water Polo
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
*Call to sport class must be protected by an `if __name__ == '__main__'` because the serial connection is read in a seperate process*

### Connecting a Console
Consoles are connected with via a Serial to USB cable.

**Daktronics All Sport 5000** - Connect to the port labeled I/O Port (J6) with a DB25 to DB9 Serial connector

**Colorado Time Systems System 6** - Tap into the 1/4" Scoreboard Out plug and connect the tip to pin 2 of a Serial DB9 connector and the shoe to pin 5.

### API
Sport classes take a serial port string as an argument and expose an `export` method that returns the current game state.

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

#### :swimmer: Swimming
*Work in Progress*