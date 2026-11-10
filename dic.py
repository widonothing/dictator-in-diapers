"""Dictator in Diapers / Dittatore in Culla.

Compares two parents' birthdays with those of 81 dictators and emperors,
and the child's birth with the anniversary of each one's rise to power.

Terminal version:  python3 dic.py          (Italian)
                   python3 dic.py --en     (English)
Web version:       python3 dic_web.py
"""
import calendar
import sys
import textwrap
from datetime import date
from typing import NamedTuple
from urllib.parse import quote

import texts_en
import texts_it

LANGUAGES = {"it": texts_it.TEXTS, "en": texts_en.TEXTS}


class Dictator(NamedTuple):
    id: str        # key into texts_it / texts_en
    birth: str     # YYYY-MM-DD
    rise: str      # YYYY-MM-DD, the day they took power
    image: str     # file name on Wikimedia Commons (Wikidata property P18)


# Dictators and emperors with an exact, known date of birth.
# Left out: anyone born BC (datetime.date can't represent them) and anyone with an
# uncertain date (Idi Amin, Gaddafi, Genghis Khan, Constantine, Charlemagne...).
# Dates before 1582 follow the Julian calendar.
# Sources for birth and rise dates: Wikipedia (infoboxes) and Wikidata.
DICTATORS = [
    Dictator("vespasian",                       "0009-11-17", "0069-07-01", 'Head of Vespasianus in Palazzo Massimo (Rome).jpg'),
    Dictator("nero",                            "0037-12-15", "0054-10-13", 'Nero Palatino Inv618.jpg'),
    Dictator("titus",                           "0039-12-30", "0079-06-24", 'Titus.jpg'),
    Dictator("domitian",                        "0051-10-24", "0081-09-14", 'Busto di Domiziano - Napoli museo Archeologico.jpg'),
    Dictator("trajan",                          "0053-09-18", "0098-01-28", 'Traianus Glyptothek Munich 336.jpg'),
    Dictator("hadrian",                         "0076-01-24", "0117-08-11", 'Bust Hadrian Musei Capitolini MC817.jpg'),
    Dictator("marcus_aurelius",                 "0121-04-26", "0161-03-07", 'Marcus Aurelius Louvre MR561 n02.jpg'),
    Dictator("septimius_severus",               "0145-04-11", "0193-04-09", 'Septimius Severus Glyptothek Munich 357 cropped.jpg'),
    Dictator("caracalla",                       "0188-04-04", "0211-02-04", 'Caracalla MAN Napoli Inv6033 n01.jpg'),
    Dictator("theodosius_i",                    "0347-01-11", "0379-01-19", 'Theodosius1cng11100822obverse.jpg'),
    Dictator("frederick_ii",                    "1194-12-26", "1220-11-22", 'Frederick II and eagle.jpg'),
    Dictator("timur",                           "1336-04-08", "1370-04-09", 'Timur seated (earliest known portrait), Timurid genealogy, 1405-1409, Samarkand (TSMK, H2152).jpg'),
    Dictator("mehmed_ii",                       "1432-03-30", "1451-02-03", 'Portrait of Mehmet II (cropped). Human Physiognomy Concerning the Personal Dispositions of the Ottomans, 1579 (TSMK H.1563).jpg'),
    Dictator("selim_i",                         "1470-10-10", "1512-04-24", 'Sultan Selim I enthroned, in Istanbul in 1514. Selīm-nāma, by Şūkrī-i Bitlisī, 1524 (National Library of Israel, Ms. Yah. Ar. 1116).jpg'),
    Dictator("suleiman_the_magnificent",        "1494-11-06", "1520-09-30", 'EmperorSuleiman.jpg'),
    Dictator("charles_v",                       "1500-02-24", "1519-06-28", 'Portrait of Charles V, Holy Roman Emperor, seated (1500–1558), formerly attributed to Titian (Alte Pinakothek, Munich).jpg'),
    Dictator("ivan_the_terrible",               "1530-08-25", "1547-01-16", 'Ivan grozny frame.jpg'),
    Dictator("akbar",                           "1542-10-15", "1556-02-11", 'Contemporary seated portrait of Akbar, 1605.jpg'),
    Dictator("oliver_cromwell",                 "1599-04-25", "1653-12-16", 'Oliver Cromwell by Samuel Cooper.jpg'),
    Dictator("aurangzeb",                       "1618-11-03", "1658-07-31", 'Aurangzeb (r. 1658-1707).jpg (Cropped).jpg'),
    Dictator("kangxi_emperor",                  "1654-05-04", "1661-02-05", '清 佚名 《清圣祖康熙皇帝朝服像》.jpg'),
    Dictator("peter_the_great",                 "1672-06-09", "1682-05-07", "Inconnu d'après J.-M. Nattier, Portrait de Pierre Ier (musée de l’Ermitage).jpg"),
    Dictator("qianlong_emperor",                "1711-09-25", "1735-10-18", 'Portrait of the Qianlong Emperor in Court Dress.jpg'),
    Dictator("catherine_the_great",             "1729-05-02", "1762-07-09", 'Catherine II after Roslin, Rokotov (1780s, Kunsthistorisches Museum).jpg'),
    Dictator("napoleon",                        "1769-08-15", "1799-11-09", 'Jacques-Louis David - The Emperor Napoleon in His Study at the Tuileries - Google Art Project.jpg'),
    Dictator("antonio_lopez_de_santa_anna",     "1794-02-21", "1833-05-16", 'Oleo Antonio Lopez de Santa Anna.PNG'),
    Dictator("napoleon_iii",                    "1808-04-20", "1851-12-02", 'Franz Xaver Winterhalter Napoleon III.jpg'),
    Dictator("francisco_solano_lopez",          "1826-07-24", "1862-09-10", 'Solano Lopez 1866 by Garcia.jpg'),
    Dictator("franz_joseph_i_of_austria",       "1830-08-18", "1848-12-02", 'Franz Joseph I of Austria.1910 (cropped).jpg'),
    Dictator("porfirio_diaz",                   "1830-09-15", "1876-11-28", 'Porfirio Diaz.jpg'),
    Dictator("leopold_ii_of_belgium",           "1835-04-09", "1885-07-01", 'Leopold ii garter knight.jpg'),
    Dictator("abdul_hamid_ii",                  "1842-09-21", "1876-08-31", 'Sultan Abdul Hamid II in 1899.jpg'),
    Dictator("emperor_meiji",                   "1852-11-03", "1867-01-30", 'Meiji Emperor.jpg'),
    Dictator("wilhelm_ii",                      "1859-01-27", "1888-06-15", 'Kaiser Wilhelm II of Germany - 1902.jpg'),
    Dictator("nicholas_ii_of_russia",           "1868-05-18", "1894-11-01", 'Nicolas II de russie.jpg'),
    Dictator("miklos_horthy",                   "1868-06-18", "1920-03-01", 'Horthy Miklós 1930.jpg'),
    Dictator("vladimir_lenin",                  "1870-04-22", "1917-11-07", 'Vladímir Lenin (fotografía coloreada).jpg'),
    Dictator("talaat_pasha",                    "1874-09-01", "1913-01-23", 'Mehmed Talat Pasha.jpg'),
    Dictator("joseph_stalin",                   "1878-12-18", "1922-04-03", 'Joseph Stalin official portrait.jpg'),
    Dictator("enver_pasha",                     "1881-11-22", "1913-01-23", 'Ismail Enver.jpg'),
    Dictator("ion_antonescu",                   "1882-06-14", "1940-09-06", 'Ion Antonescu 1941.jpg'),
    Dictator("maximiliano_hernandez_martinez",  "1882-10-21", "1931-12-04", 'General Maximiliano Hernández Martínez, President of El Salvador.jpg'),
    Dictator("benito_mussolini",                "1883-07-29", "1922-10-31", 'Mussolini mezzobusto.jpg'),
    Dictator("hideki_tojo",                     "1884-12-30", "1941-10-18", 'Hideki Tojo.jpg'),
    Dictator("chiang_kai_shek",                 "1887-10-31", "1928-10-10", 'Chiang Kai-shek（蔣中正）.jpg'),
    Dictator("adolf_hitler",                    "1889-04-20", "1933-01-30", 'Adolf Hitler cropped restored 3x4.jpg'),
    Dictator("ante_pavelic",                    "1889-07-14", "1941-04-10", 'Ante Pavelić StAF (3x4 cropped).jpg'),
    Dictator("ho_chi_minh",                     "1890-05-19", "1945-09-02", 'Ho Chi Minh 1946.jpg'),
    Dictator("rafael_trujillo",                 "1891-10-24", "1930-08-16", 'Rafael L. Trujillo en la silla presidencial (cropped).jpg'),
    Dictator("josip_broz_tito",                 "1892-05-07", "1943-11-29", 'Josip Broz Tito uniform portrait.jpg'),
    Dictator("francisco_franco",                "1892-12-04", "1936-10-01", 'RETRATO DEL GRAL. FRANCISCO FRANCO BAHAMONDE (adjusted levels).jpg'),
    Dictator("mao_zedong",                      "1893-12-26", "1949-10-01", 'Mao Tse Tung.jpg'),
    Dictator("hirohito",                        "1901-04-29", "1926-12-25", 'Hirohito in dress uniform.jpg'),
    Dictator("ruhollah_khomeini",               "1902-09-24", "1979-02-11", 'Ruhollah Khomeini portrait 2 (cropped).jpg'),
    Dictator("francois_duvalier",               "1907-04-14", "1957-10-22", 'François Duvalier (cropped).jpg'),
    Dictator("enver_hoxha",                     "1908-10-16", "1944-10-23", 'Enver Hoxha (portret).jpg'),
    Dictator("kim_il_sung",                     "1912-04-15", "1948-09-09", 'Kim Il Sung Portrait-3.jpg'),
    Dictator("yahya_khan",                      "1917-02-04", "1969-03-25", 'Yahya Khan (cropped version).jpg'),
    Dictator("siad_barre",                      "1919-10-06", "1969-10-21", 'Siad Barre.png'),
    Dictator("suharto",                         "1921-06-08", "1967-03-12", 'President Suharto, 1993.jpg'),
    Dictator("ahmed_sekou_toure",               "1922-01-09", "1958-10-02", 'Ahmed Sekoú in 1962 at White House cropped.jpg'),
    Dictator("francisco_macias_nguema",         "1924-01-01", "1968-10-12", 'Don Francisco Macias.jpg'),
    Dictator("robert_mugabe",                   "1924-02-21", "1980-04-18", 'Robert Mugabe May 2015 (cropped 3x4).jpg'),
    Dictator("pol_pot",                         "1925-05-19", "1975-04-17", 'Pol Pot (cropped).jpg'),
    Dictator("jorge_rafael_videla",             "1925-08-02", "1976-03-24", 'Jorge Rafael Videla 1976.PNG'),
    Dictator("anastasio_somoza_debayle",        "1925-12-05", "1967-05-01", '1975 Press Photo Nicaragua President Anastasio Somoza (cropped).png'),
    Dictator("milton_obote",                    "1925-12-28", "1962-04-30", 'Obote cropped.png'),
    Dictator("efrain_rios_montt",               "1926-06-16", "1982-03-23", 'Retrato oficial de Presidente Efraín Ríos Montt (cropped).jpg'),
    Dictator("fidel_castro",                    "1926-08-13", "1959-01-01", 'Fidel Castro 1950s.jpg'),
    Dictator("hafez_al_assad",                  "1930-10-06", "1970-11-13", 'Hafez al-Assad official portrait.jpg'),
    Dictator("yakubu_gowon",                    "1934-10-19", "1966-08-01", 'Yakubu Gowon (cropped).jpg'),
    Dictator("saddam_hussein",                  "1937-04-28", "1979-07-16", 'Saddam Hussein in 1998.png'),
    Dictator("mengistu_haile_mariam",           "1937-05-21", "1977-02-03", 'Mengistu Haile Mariam 4.jpg'),
    Dictator("michel_micombero",                "1940-08-26", "1966-11-28", 'Prime Minister Micombero in 1966.png'),
    Dictator("kim_jong_il",                     "1941-02-16", "1994-07-08", 'Kim Jong il Portrait-2.jpg'),
    Dictator("slobodan_milosevic",              "1941-08-20", "1989-05-08", 'Stevan Kragujević, Slobodan Milošević, portret.jpg'),
    Dictator("hissene_habre",                   "1942-08-13", "1982-06-07", 'President Hissène Habré of Chad.jpg'),
    Dictator("omar_al_bashir",                  "1944-01-01", "1989-06-30", 'Omar al-Bashir, 12th AU Summit, 090202-N-0506A-137 cropped.jpg'),
    Dictator("charles_taylor",                  "1948-01-28", "1997-08-02", 'Charles Taylor 1984 mugshot (cropped).jpg'),
    Dictator("min_aung_hlaing",                 "1956-07-03", "2021-02-01", 'President Min Aung Hlaing 2026 (cropped).jpg'),
    Dictator("bashar_al_assad",                 "1965-09-11", "2000-07-17", '(cropped 2) دیدار بشار اسد و هیئت همراه با سید علی خامنه ای، ۱۰ خرداد ۱۴۰۳ (05).jpg'),
]

# Probability by distance (in days, ignoring the year) from a dictator's birthday.
# (maximum distance, percentage)
BANDS = [
    (0, 100),
    (3, 80),
    (7, 60),
    (14, 40),
    (30, 20),
    (60, 10),
]
MINIMUM = 0

# The child uses the same bands against the anniversary of each rise to power
# (the year doesn't count; being born on the exact date is only flagged).
CHILD_BANDS = BANDS

# Weight of the two factors in the final result (they add up to 1).
# 100% is only possible if both parents share a dictator's birthday
# AND the child is born on the anniversary of a rise to power.
PARENTS_WEIGHT = 0.7
CHILD_WEIGHT = 0.3


def image_url(dictator, width=400):
    return (f"https://commons.wikimedia.org/wiki/Special:FilePath/"
            f"{quote(dictator.image.replace(' ', '_'))}?width={width}")


def day_of_year(d):
    # Fake leap year, so that 29 February always exists
    return date(2000, d.month, d.day).timetuple().tm_yday


def days_apart(a, b):
    """Distance between two dates ignoring the year (circular over 366 days)."""
    diff = abs(day_of_year(a) - day_of_year(b))
    return min(diff, 366 - diff)


def closest(when, date_of):
    """Return (minimum distance, list of dictators tied at that distance).
    date_of(d) gives the dictator's date to compare with."""
    distances = [(d, days_apart(when, date_of(d))) for d in DICTATORS]
    smallest = min(dist for _, dist in distances)
    return smallest, [d for d, dist in distances if dist == smallest]


def birth_date(d):
    return date.fromisoformat(d.birth)


def rise_date(d):
    return date.fromisoformat(d.rise)


def band_value(distance, bands, default=0):
    for limit, value in bands:
        if distance <= limit:
            return value
    return default


def card(d, lang="it"):
    """Everything the page (or the terminal) needs to show one dictator."""
    text = LANGUAGES[lang][d.id]
    return {
        "number": DICTATORS.index(d) + 1,
        "id": d.id,
        "name": text["name"],
        "birth": d.birth,
        "rise": d.rise,
        "event": text["event"],
        "who": text["who"],
        "victims": text["victims"],
        "fun_fact": text["fun_fact"],
        "biography": text["biography"],
        "image": image_url(d),
    }


def expected_birth(today=None):
    """Estimated birth date: today + 9 months (if that day doesn't exist, the last of the month)."""
    today = today or date.today()
    month = today.month + 9
    year = today.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(today.day, last_day))


def compute(parents, child_birth=None, lang="it"):
    """parents: list of (name, date).
    child_birth: date, or None to use the estimate (today + 9 months).
    Returns a dictionary with every result (used by the terminal and the web page)."""
    if lang not in LANGUAGES:
        raise ValueError(f"unknown language: {lang}")
    estimated = child_birth is None
    if estimated:
        child_birth = expected_birth()

    result = {"parents": [], "child": None}
    percents = []
    for name, born in parents:
        distance, matches = closest(born, birth_date)
        percent = band_value(distance, BANDS, MINIMUM)
        percents.append(percent)
        result["parents"].append({
            "name": name,
            "birth": born.isoformat(),
            "distance": distance,
            "percent": percent,
            "dictators": [card(d, lang) for d in matches],
        })
    parents_avg = sum(percents) / len(percents)

    distance, matches = closest(child_birth, rise_date)
    same_date = any(rise_date(d) == child_birth for d in matches)
    child_percent = band_value(distance, CHILD_BANDS)
    result["child"] = {
        "birth": child_birth.isoformat(),
        "estimated": estimated,
        "distance": distance,
        "percent": child_percent,
        "same_date": same_date,
        "dictators": [card(d, lang) for d in matches],
    }

    result["parents_avg"] = round(parents_avg)
    result["parents_weight"] = round(PARENTS_WEIGHT * 100)
    result["child_weight"] = round(CHILD_WEIGHT * 100)
    result["total"] = round(PARENTS_WEIGHT * parents_avg + CHILD_WEIGHT * child_percent)
    return result


# ---------------------------------------------------------------- terminal version

CLI_TEXT = {
    "it": {
        "parent_name": "Nome del genitore {i}: ",
        "parent_birth": "Data di nascita di {name} (YYYY-MM-DD): ",
        "child_birth": "Data di nascita del figlio (YYYY-MM-DD, invio = stima a 9 mesi da oggi): ",
        "bad_date": "Formato non valido, riprova (es. 1990-04-20).",
        "same_day": "{name} è nato lo stesso giorno di {list}! -> {p}%",
        "closest_one": "{name}: dittatore più vicino {list}, a {n} giorni -> {p}%",
        "closest_many": "{name}: dittatori più vicini {list}, a {n} giorni -> {p}%",
        "child_estimated": "Figlio: nascita stimata il {d} (9 mesi da oggi)",
        "child_exact": "nato proprio il giorno esatto, anno compreso",
        "child_anniversary": "nato nell'anniversario",
        "child_days": "a {n} giorni dall'anniversario",
        "child_line": "Figlio: ascesa al potere più vicina {list}, {when} -> {p}%",
        "weights": "Genitori {a}% (peso {wa}%) + figlio {c}% (peso {wc}%)",
        "total": "Probabilità che il figlio di {a} e {b} diventi un dittatore: {p}%",
        "cards": "--- Schede dei dittatori trovati (vittime: stime indicative) ---",
        "card_head": "{name} (nato il {birth}, al potere dal {rise})",
        "who": "Chi era", "victims": "Vittime", "fun_fact": "Fun fact",
    },
    "en": {
        "parent_name": "Name of parent {i}: ",
        "parent_birth": "{name}'s date of birth (YYYY-MM-DD): ",
        "child_birth": "Child's date of birth (YYYY-MM-DD, enter = estimate 9 months from today): ",
        "bad_date": "Invalid format, try again (e.g. 1990-04-20).",
        "same_day": "{name} was born on the same day as {list}! -> {p}%",
        "closest_one": "{name}: closest dictator {list}, {n} days away -> {p}%",
        "closest_many": "{name}: closest dictators {list}, {n} days away -> {p}%",
        "child_estimated": "Child: estimated birth {d} (9 months from today)",
        "child_exact": "born on the exact date, year included",
        "child_anniversary": "born on the anniversary",
        "child_days": "{n} days from the anniversary",
        "child_line": "Child: closest rise to power {list}, {when} -> {p}%",
        "weights": "Parents {a}% (weight {wa}%) + child {c}% (weight {wc}%)",
        "total": "Probability that {a} and {b}'s child becomes a dictator: {p}%",
        "cards": "--- The dictators found (victims: rough estimates) ---",
        "card_head": "{name} (born {birth}, in power from {rise})",
        "who": "Who", "victims": "Victims", "fun_fact": "Fun fact",
    },
}


def ask_date(prompt, t, optional=False):
    while True:
        answer = input(prompt).strip()
        if optional and not answer:
            return None
        try:
            return date.fromisoformat(answer)
        except ValueError:
            print(t["bad_date"])


def print_card(c, t):
    indent = " " * 4
    print("\n  " + t["card_head"].format(name=c["name"], birth=c["birth"], rise=c["rise"]))
    for label, text in [(t["who"], c["biography"]), (t["victims"], c["victims"]), (t["fun_fact"], c["fun_fact"])]:
        print(textwrap.fill(f"{label}: {text}", width=90, initial_indent=indent, subsequent_indent=indent + "  "))


def main():
    lang = "en" if "--en" in sys.argv else "it"
    t = CLI_TEXT[lang]
    parents = []
    for i in (1, 2):
        name = input(t["parent_name"].format(i=i)).strip()
        parents.append((name, ask_date(t["parent_birth"].format(name=name), t)))
    child = ask_date(t["child_birth"], t, optional=True)

    r = compute(parents, child, lang)
    cards = {}

    print()
    for p in r["parents"]:
        names = ", ".join(f"{d['name']} ({d['birth']})" for d in p["dictators"])
        for d in p["dictators"]:
            cards[d["id"]] = d
        if p["distance"] == 0:
            line = t["same_day"]
        else:
            line = t["closest_many"] if len(p["dictators"]) > 1 else t["closest_one"]
        print(line.format(name=p["name"], list=names, n=p["distance"], p=p["percent"]))

    c = r["child"]
    names = ", ".join(f"{d['name']} ({d['rise']}: {d['event']})" for d in c["dictators"])
    for d in c["dictators"]:
        cards[d["id"]] = d
    if c["same_date"]:
        when = t["child_exact"]
    elif c["distance"] == 0:
        when = t["child_anniversary"]
    else:
        when = t["child_days"].format(n=c["distance"])
    if c["estimated"]:
        print(t["child_estimated"].format(d=c["birth"]))
    print(t["child_line"].format(list=names, when=when, p=c["percent"]))

    print("\n" + t["weights"].format(a=r["parents_avg"], wa=r["parents_weight"], c=c["percent"], wc=r["child_weight"]))
    print(t["total"].format(a=parents[0][0], b=parents[1][0], p=r["total"]))

    print("\n" + t["cards"])
    for card_data in cards.values():
        print_card(card_data, t)


if __name__ == "__main__":
    main()
