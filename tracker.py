#!/usr/bin/env python3

import sys
from datetime import date, datetime

# ----- CONFIGURATION -----
DELOAD_WEEKS = [6, 10]
DELOAD_FACTOR = 0.9  # 90% of normal load
START_DATE = date(2024, 12, 29)  # Sunday, Dec 29, 2024

# Helper: Round loads to nearest integer
def round_load(value):
    return int(round(value))

def calculate_load(week, base_load, weekly_increment):
    """
    Computes the normal (non-deload) load for the given week.
    e.g., Week 1 => base_load
          Week 2 => base_load + weekly_increment
          ...
    """
    if week < 1: 
        return base_load  # Just a safety check.
    return base_load + (week - 1) * weekly_increment

def deload_adjustment(load):
    """
    Applies the deload factor to a given load.
    """
    return round_load(load * DELOAD_FACTOR)

def get_sets_for_week(week, base_sets):
    """
    Adjust sets if it's a deload week:
      - If base_sets = 4, deload => 3
      - If base_sets = 5, deload => 4
      - If base_sets = 6, deload => 4
    """
    if week in DELOAD_WEEKS:
        if base_sets == 4:
            return 3
        elif base_sets == 5:
            return 4
        elif base_sets == 6:
            return 4
    return base_sets

def get_intervals_for_week(week, base_intervals):
    """
    If base_intervals = 6, in a deload week => 4.
    If base_intervals = 5, in a deload week => 4.
    """
    if week in DELOAD_WEEKS:
        if base_intervals >= 5:
            return 4
    return base_intervals

def get_mph_for_week(week, base_mph, increment):
    """
    For treadmill intervals, e.g., 6 mph + 0.5 mph each week.
    """
    normal_mph = base_mph + (week - 1) * increment
    if week in DELOAD_WEEKS:
        # Usually we don't scale mph for deload, but if you want to:
        # normal_mph *= DELOAD_FACTOR
        pass
    return round_load(normal_mph)

def get_minutes_for_week(week, base_minutes, increment):
    """
    For steady-state runs, e.g., 10 min + 1 min each week until Wk5, etc.
    """
    normal_minutes = base_minutes + (week - 1) * increment
    # If it's a deload week, reduce by 20% or a fixed chunk
    if week in DELOAD_WEEKS:
        # Example approach: 0.9 * minutes OR specific instructions
        normal_minutes = round_load(normal_minutes * 0.8)  # e.g., 80%
    return max(0, normal_minutes)

###############################################################################
# DEFINE THE PROGRAM FOR EACH DAY (Week 1 Baseline)
###############################################################################
# day_of_week: 0=Sunday, 1=Monday, ..., 6=Saturday

PROGRAM = {
    0: {  # Sunday
        "title": "Sunday (Recovery or Light Cardio)",
        "exercises": [
            {
                "name": "Recovery or Light Cardio",
                "description": "Walk, yoga, gentle swim. No heavy lifting."
            }
        ]
    },
    1: {  # Monday
        "title": "Monday",
        "exercises": [
            {
                "name": "Snatch",
                "sets": 4,
                "reps": 3,
                "base_load": 100,     # Week 1 load
                "increment": 2.5     # +2.5 lbs each week
            },
            {
                "name": "Back Squat",
                "sets": 4,
                "reps": 5,
                "base_load": 145,    # Week 1 load
                "increment": 5       # +5 lbs each week (then maybe reduce to 2.5 after Wk6, but we'll keep 5 for simplicity)
            },
            {
                "name": "Ring Push-Ups",
                "sets": 4,
                "reps": 8,
                "base_load": 0,      # Bodyweight
                "increment": 0       # No external load progression
            },
            {
                "name": "Ring Rows",
                "sets": 4,
                "reps": 8,
                "base_load": 0,      # Bodyweight
                "increment": 0
            },
            {
                "name": "Box Jumps",
                "sets": 4,
                "reps": 3,
                "base_load": 0,      # Bodyweight
                "increment": 0
            },
            {
                "name": "Treadmill Intervals",
                "intervals": 5,      # 5 x 1 min
                "base_mph": 6,       # 6 mph in Week 1
                "increment_mph": 0.5 # +0.5 mph each week
            }
        ]
    },
    2: {  # Tuesday
        "title": "Tuesday",
        "exercises": [
            {
                "name": "Clean & Jerk",
                "sets": 4,
                "reps": 3,
                "base_load": 135,
                "increment": 5
            },
            {
                "name": "Bench Press",
                "sets": 4,
                "reps": 5,
                "base_load": 105,
                "increment": 5
            },
            {
                "name": "Ring Chin-Ups",
                "sets": 4,
                "reps": 6,
                "base_load": 0,  # Bodyweight
                "increment": 0
            },
            {
                "name": "Ring Dips",
                "sets": 4,
                "reps": 6,
                "base_load": 0,  # Bodyweight
                "increment": 0
            },
            {
                "name": "Split Squat Jumps",
                "sets": 3,
                "reps": 5,  # per leg
                "base_load": 0,  # Bodyweight
                "increment": 0
            },
            {
                "name": "Pool Intervals",
                "intervals": 6,  # 6x25m
                "base_rest_sec": 30,
                "rest_decrement_sec": 5, # every 2 weeks
            }
        ]
    },
    3: {  # Wednesday
        "title": "Wednesday",
        "exercises": [
            {
                "name": "Deadlift",
                "sets": 4,
                "reps": 5,
                "base_load": 185,
                "increment": 10
            },
            {
                "name": "Overhead Press",
                "sets": 4,
                "reps": 5,
                "base_load": 75,
                "increment": 2.5
            },
            {
                "name": "Ring Bodyweight Row",
                "sets": 3,
                "reps": 10,
                "base_load": 0,
                "increment": 0
            },
            {
                "name": "Ring Push-Ups (Feet Elevated)",
                "sets": 3,
                "reps": 10,
                "base_load": 0,
                "increment": 0
            },
            {
                "name": "Broad Jumps",
                "sets": 4,
                "reps": 2,
                "base_load": 0,
                "increment": 0
            },
            {
                "name": "Treadmill Run",
                "duration": 10,   # 10 min @ ~5 mph (Week 1)
                "increment": 1    # +1 min each week up to Wk5
            }
        ]
    },
    4: {  # Thursday
        "title": "Thursday",
        "exercises": [
            {
                "name": "Extended Mobility",
                "description": "20 min stretch + foam roll"
            },
            {
                "name": "Snatch (Technique)",
                "sets": 3,
                "reps": 3,
                "base_load": 80,  # ~80% of Monday's 100 lbs for Week 1
                "increment": 2.0  # Could track ~80% of main snatch or keep a small increment
            },
            {
                "name": "Pallof Holds (Band)",
                "sets": 3,
                "reps": 10,  # per side
                "base_load": 0,
                "increment": 0
            },
            {
                "name": "DB Walking Lunges",
                "sets": 3,
                "reps": 8,  # per leg
                "base_load": 50,  # 2x25 lbs DB
                "increment": 5
            },
            {
                "name": "Core Plank Variations",
                "sets": 3,
                "duration_sec": 45,  # 45s each
                "increment_sec": 10  # add 5-10s every 2 weeks (example)
            },
            {
                "name": "Zone 2 Cardio",
                "duration": 20,  # 20-25 min moderate
                "increment": 2   # add 2 min every 2 weeks
            }
        ]
    },
    5: {  # Friday
        "title": "Friday",
        "exercises": [
            {
                "name": "Power Clean",
                "sets": 4,
                "reps": 3,
                "base_load": 155,
                "increment": 2.5
            },
            {
                "name": "Front Squat",
                "sets": 4,
                "reps": 3,
                "base_load": 135,
                "increment": 5
            },
            {
                "name": "Ring Supported Push-Up Hold (Top Lock)",
                "sets": 3,
                "duration_sec": 15,  # 15-20s in Week 1
                "increment_sec": 5
            },
            {
                "name": "Single-Leg RDL (DBs)",
                "sets": 3,
                "reps": 8,
                "base_load": 40,  # 2x20 lbs DB
                "increment": 5
            },
            {
                "name": "Sprint Intervals",
                "intervals": 6,  # 6 x 100m
                "description": "~90% effort"
            }
        ]
    },
    6: {  # Saturday
        "title": "Saturday",
        "exercises": [
            {
                "name": "Recovery or Light Cardio",
                "description": "Walk, yoga, gentle swim. No heavy lifting."
            }
        ]
    }
}

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tracker.py YYYY-MM-DD")
        sys.exit(1)

    # Parse input date
    try:
        current_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)

    # Calculate how many days since program start
    day_offset = (current_date - START_DATE).days

    # Program is 12 weeks -> 84 days total
    if day_offset < 0:
        print(f"Program starts on {START_DATE}. Today is too early.")
        return
    if day_offset > 83:
        print("The 12-week program has been completed.")
        return

    # Determine which week (1-12) and day of the week
    week = (day_offset // 7) + 1
    day_of_week = day_offset % 7

    day_data = PROGRAM[day_of_week]
    title = day_data["title"]
    exercises = day_data["exercises"]

    print(f"\n--- DAILY WORKOUT ---")
    print(f"Date: {current_date.strftime('%Y-%m-%d')}")
    print(f"Week: {week}  |  Day: {title}")
    print("-" * 40)

    for ex in exercises:
        # Handle purely descriptive items (no progression)
        if "description" in ex and len(ex.keys()) == 2:
            # e.g., Recovery or Light Cardio entry
            print(f"- {ex['name']}: {ex['description']}")
            continue

        name = ex["name"]

        # Handle sets, reps, base_load, increment, intervals, etc.
        # Check if it's a barbell lift or something with load-based progression
        if "base_load" in ex and "increment" in ex:
            base_load = ex["base_load"]
            increment = ex["increment"]
            normal_load = calculate_load(week, base_load, increment)

            # If deload week, reduce load by factor
            if week in DELoad_WEEKS:
                adjusted_load = deload_adjustment(normal_load)
            else:
                adjusted_load = round_load(normal_load)

            sets = get_sets_for_week(week, ex["sets"]) if "sets" in ex else None
            reps = ex["reps"] if "reps" in ex else None

            if sets and reps:
                print(f"- {name}: {sets}x{reps} @ {adjusted_load} lbs")
            elif sets:
                print(f"- {name}: {sets} sets @ {adjusted_load} lbs")
            else:
                # Fallback
                print(f"- {name}: {adjusted_load} lbs")

        # Handle intervals (like treadmill intervals, sprints, pool intervals)
        elif "intervals" in ex:
            intervals = ex["intervals"]
            # Treadmill Intervals or Sprint Intervals
            if "Treadmill Intervals" in ex["name"]:
                base_mph = ex["base_mph"]
                mph_increment = ex["increment_mph"]

                normal_mph = get_mph_for_week(week, base_mph, mph_increment)
                intervals = get_intervals_for_week(week, intervals)
                print(f"- {name}: {intervals} x 1 min @ {normal_mph} mph (1 min rest)")
            elif "Sprint Intervals" in ex["name"]:
                intervals = get_intervals_for_week(week, intervals)
                desc = ex.get("description", "")
                print(f"- {name}: {intervals}x100m {desc}")
            elif "Pool Intervals" in ex["name"]:
                base_rest_sec = ex["base_rest_sec"]
                rest_decrement = ex["rest_decrement_sec"]
                # Decrease rest by 5s every 2 weeks
                # e.g., rest = base_rest_sec - 5 * ((week-1)//2)
                rest_sec = base_rest_sec - rest_decrement * ((week - 1) // 2)
                if week in DELoad_WEEKS:
                    intervals = get_intervals_for_week(week, intervals)
                # Limit rest_sec not to go negative
                rest_sec = max(5, rest_sec)
                print(f"- {name}: {intervals}x25m (~{rest_sec}s rest)")
            else:
                print(f"- {name}: {intervals} intervals (no specific logic)")

        # Handle time or duration-based (e.g., Treadmill Run, Zone 2 Cardio)
        elif "duration" in ex and "increment" in ex:
            base_duration = ex["duration"]
            increment = ex["increment"]
            actual_minutes = get_minutes_for_week(week, base_duration, increment)
            print(f"- {name}: {actual_minutes} min")

        # Handle sets/duration-based (e.g., Plank holds, Ring Supported Holds)
        elif "duration_sec" in ex and "increment_sec" in ex:
            base_sec = ex["duration_sec"]
            inc_sec = ex["increment_sec"]
            # Increase every week or every 2 weeks?
            # We'll do: total_sec = base_sec + inc_sec*((week-1)//2) as an example
            # Or simply base_sec + inc_sec*(week-1).
            # Modify if deload
            total_sec = base_sec + inc_sec * (week - 1)
            if week in DELoad_WEEKS:
                total_sec = round_load(total_sec * DELOAD_FACTOR)
            sets = get_sets_for_week(week, ex["sets"])
            print(f"- {name}: {sets}x ~{int(total_sec)}s")

        # Handle sets/reps with no load (e.g., ring push-ups at bodyweight)
        elif "sets" in ex and "reps" in ex:
            sets = get_sets_for_week(week, ex["sets"])
            reps = ex["reps"]
            print(f"- {name}: {sets}x{reps}, Bodyweight")

        # Catch-all fallback
        else:
            # If there's any textual leftover
            print(f"- {name}")

    print("-" * 40)
    print("Enjoy your training!\n")


if __name__ == "__main__":
    # Adjust the constant for deload weeks, if typed incorrectly
    DELoad_WEEKS = DELOAD_WEEKS  # Just referencing for clarity
    main()
