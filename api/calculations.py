import math
import datetime
import random

# Get the difference in minutes between the start time and end time provided
def calc_timeframe(start_time, end_time):
    start_time = datetime.datetime.strptime(start_time, "%H:%M")
    end_time = datetime.datetime.strptime(end_time, "%H:%M")

    time_difference = end_time - start_time

    # If start time is higher than end time (i.e. crosses midnight)
    if time_difference.days < 0:
        time_difference = datetime.timedelta(
            days=0,
            seconds=time_difference.seconds
        )
    time_diff_mins = int(time_difference.total_seconds() / 60) if int(time_difference.total_seconds() / 60) >= 10 else 10
    return time_diff_mins


# Calculates how much time each night will be attributed to a person's shift
def calc_slots(persons, timeframe):

    # Rounds the time per person up to 10 mins
    slot_rounded = math.ceil((timeframe / len(persons)) / 10.0) * 10
    slots_list = []
    for person in persons:
        slots_list.append(slot_rounded)
    
    # Deducts the remainder created by rounding up, starting from people on mid-night shifts
    remainder = slot_rounded*len(persons) - timeframe
    if remainder >= 10:
        i = math.ceil(len(slots_list)/2)
        step = 0
        sign = -1
    while remainder >= 10:
        slots_list[i + step] -= 10
        if step >= 0:
            step = (step + 1)*sign
        else:
            step = -step
        sign = -sign
        remainder -= 10
    return slots_list


# Calculates hours and minutes from what time till what time each shift will take place
def get_time_slots(slots_list, start_time):
    time_slots = []
    time = datetime.datetime.strptime(start_time, "%H:%M")

    for slot in slots_list:
        time_slots.append(
            {
                'from': time.strftime("%H:%M"),
                'to': (time + datetime.timedelta(minutes=slot)).strftime("%H:%M")
            }
        )
        time = time + datetime.timedelta(minutes=slot)
    return time_slots


# Calculates how many nights there are between the start date and the end date
def get_night_count(start_date, end_date):
    start_date = datetime.date.fromisoformat(start_date)
    end_date = datetime.date.fromisoformat(end_date)
    num_of_nights = (end_date - start_date).days

    # Validation - if end date is earlier than start date, return 1 night iso negative number
    if num_of_nights <= 0:
        num_of_nights = 1
    # Validation - ensure that there is a maximum of 10 nights
    elif num_of_nights > 10:
        num_of_nights = 10
    
    return num_of_nights

# Create a dictionary of from-to dates for each night for a group
def get_dates(start_date, num_of_nights):
    dates_list = []
    dt = datetime.date.fromisoformat(start_date)
    for x in range(num_of_nights):
        dates_list.append(
            {
                'from': dt.strftime("%Y-%m-%d"),
                'to': (dt + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            }
        )
        dt = dt + datetime.timedelta(days=1)

    return dates_list


# Randomize the list of names provided by the user
def randomize_persons(persons):
    randomized_persons = random.sample(persons, len(persons))  
    return randomized_persons


# Create a dictionary for each night, containing time slots and names assigned to them
def calc_shifts(dates_list, persons, time_slots):
    shifts_list = []
    for day in dates_list:
            randomized_persons = randomize_persons(persons)
            shifts_list.append(
                        {
                            'date': {'from': day['from'], 'to': day['to']},
                            'shift_slots': []
                        }
                    )
            for x in range(len(randomized_persons)):
                shift_member = {
                    'from': time_slots[x]['from'],
                    'to': time_slots[x]['to'],
                    'name': randomized_persons[x]
                }
                shifts_list[dates_list.index(day)]['shift_slots'].append(shift_member)

    return shifts_list
