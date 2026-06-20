TEAM_FLAGS = {

    "Mexico":           "mx", "South Africa":    "za", "South Korea":     "kr",
    "Canada":           "ca", "Switzerland":     "ch", "Qatar":           "qa",
    "Brazil":           "br", "Morocco":         "ma", "Haiti":           "ht",
    "Scotland":         "gb-sct", "USA":          "us", "Paraguay":       "py",
    "Australia":        "au", "Germany":         "de", "Curaçao":         "cw",
    "Ivory Coast":      "ci", "Ecuador":         "ec", "Netherlands":     "nl",
    "Japan":            "jp", "Tunisia":         "tn", "Argentina":       "ar",
    "England":          "gb-eng", "France":       "fr", "Spain":          "es",
    "Portugal":         "pt", "Italy":           "it", "Belgium":        "be",
    "Uruguay":          "uy", "Colombia":        "co", "Chile":           "cl",
    "Croatia":          "hr", "Denmark":         "dk", "Serbia":          "rs",
    "Poland":           "pl", "Senegal":         "sn", "Ghana":           "gh",
    "Cameroon":         "cm", "Nigeria":         "ng", "Costa Rica":      "cr",
    "Iran":             "ir", "Russia":           "ru", "Saudi Arabia":   "sa",
    "South Korea":      "kr", "Algeria":         "dz", "Egypt":          "eg",
    "Peru":             "pe", "Sweden":          "se", "Hungary":         "hu",
    "Czechoslovakia":   "cz", "Yugoslavia":      "rs", "Bolivia":        "bo",
    "Romania":          "ro", "Austria":         "at", "Cuba":            "cu",
    "Norway":           "no", "Netherlands Indies": "id", "India":        "in",
    "East Germany":     "de", "West Germany":    "de", "Turkey":          "tr",
    "Wales":            "gb-wls", "Northern Ireland": "gb-nir",
    "Bulgaria":         "bg", "Israel":          "il", "New Zealand":     "nz",
    "Honduras":         "hn", "Slovakia":        "sk", "Slovenia":        "si",
    "Greece":           "gr", "Togo":            "tg", "Trinidad and Tobago": "tt",
    "Ukraine":          "ua", "Angola":          "ao", "Czech Republic":  "cz",
    "Switzerland":      "ch", "Ecuador":         "ec", "United Arab Emirates": "ae",
    "El Salvador":      "sv", "Haiti":           "ht", "Zaire":          "cd",
    "East Germany":     "de", "Kuwait":          "kw", "New Zealand":     "nz",
    "Iraq":             "iq", "Canada":          "ca", "Denmark":         "dk",
    "United States":    "us", "UAE":             "ae", "China":           "cn",
    "Senegal":          "sn", "Turkey":          "tr", "Panama":          "pa",
    "Iceland":          "is", "Egypt":           "eg", "DR Congo":        "cd",
    "Côte d'Ivoire":    "ci", "Republic of Ireland": "ie", "Ireland":    "ie",
}

def get_flag_url(team_name, width=20):

    iso2 = TEAM_FLAGS.get(team_name, "un") 
    return f"https://flagcdn.com/w{width}/{iso2}.png"

def flag_html(team_name, width=20):

    url = get_flag_url(team_name, width)
    return f'<img src="{url}" width="{width}" style="vertical-align:middle; margin-right:5px;">'