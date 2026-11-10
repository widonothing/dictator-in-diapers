# Dictator in Diapers · Dittatore in Culla

A tongue-in-cheek "newspaper" that estimates the odds of a baby becoming a dictator.
It compares both parents' birthdays with those of 81 dictators and emperors, and the
baby's birth date with the anniversary of the day each of them seized power.
The result reads like an investigation: a red thread runs through the centuries,
stopping at every connected file, all the way to the cradle.

Available in Italian and English.

> It's a game: your birthday doesn't decide anyone's fate. Victim counts are rough,
> debated estimates; dates come from Wikipedia and Wikidata, portraits from Wikimedia Commons.

## Run it

Only Python 3 is needed (standard library). An internet connection shows the portraits.

```
python3 dic_web.py      # web page, opens http://localhost:8000
python3 dic.py          # terminal version (Italian)
python3 dic.py --en     # terminal version (English)
```

## Files

| File | What it does |
|---|---|
| `dic.py` | core data (dates, portraits), scoring and terminal version |
| `texts_it.py` / `texts_en.py` | names, biographies, victims, fun facts in each language |
| `dic_web.py` | small local web server |
| `dic_web.html` | the page (horizontal newspaper, bookshelf, red thread) |
| `fonts/` | optional licensed fonts, see `fonts/README.txt` |

## Scoring

- Each parent's birthday vs every dictator's (year ignored): 100% on the same day, then 80/60/40/20/10% within 3/7/14/30/60 days. Worth 70%.
- The baby's birthday vs the anniversary of every rise to power, same bands. Worth 30%.
- 100% only when everything lines up.
