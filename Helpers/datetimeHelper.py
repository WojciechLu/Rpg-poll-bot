import datetime
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)
    
def translate_weekday(weekday):
    match weekday:
        case 0:
            return "Pon"
        case 1:
            return "Wt"
        case 2:
            return "Śr"
        case 3:
            return "Czw"
        case 4:
            return "Piąt"
        case 5:
            return "Sob"
        case 6:
            return "Niedz"