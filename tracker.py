#!/usr/bin/env python3

import sys
from datetime import datetime, date

def get_program_data():
    """
    Returns a dictionary keyed by day of the week (0=Sunday, ..., 6=Saturday)
    Each value is the baseline workout for that day (Week 1).
    For deload weeks (6 & 10), certain adjustments will be made in the code.
    """
    program = {
        0: {  # SUNDAY
            "title": "Sunday (Recovery or Light Cardio)",
            "workout": [
                "Recovery / Optional Light Cardio (walk, yoga, gentle swim)",
                "No heavy lifting; focus on rest, mobility, quality sleep."
            ],
        },
        1: {  # MONDAY
            "title": "Monday",
            "workout": [
                "Warm-Up (Dynamic, ~5 Min)",
                "Snatch: 4x3 @ 100 lbs (Week 1). Add 2.5 lbs each week.",
                "Back Squat: 4x5 @ 145 lbs (Week 1). Add 5 lbs/week initially.",
                "Ring Push-Ups: 4x8, Bodyweight (progress with vest after Week 4).",
                "Ring Rows: 4x8, Bodyweight (progress angle/vest).",
                "Box Jumps (Mid-Height): 4x3, Bodyweight focus on power.",
                "Treadmill Intervals: 5 x 1 min @ 6 mph (1 min rest). +0.5 mph each week."
            ],
        },
        2: {  # TUESDAY
            "title": "Tuesday",
            "workout": [
                "Warm-Up (Dynamic + Light DB, ~5-10 Min)",
                "Clean & Jerk: 4x3 @ 135 lbs (Week 1). +5 lbs/week initially.",
                "Bench Press: 4x5 @ 105 lbs. +5 lbs/week initially.",
                "Ring Chin-Ups: 4x6, Bodyweight (add +5 lbs every 3-4 weeks).",
                "Ring Dips: 4x6, Bodyweight (add +5 lbs every 3-4 weeks).",
                "Split Squat Jumps: 3x5/leg, Bodyweight.",
                "Pool Intervals: 6x25m (~30s rest). Decrease rest by 5s every 2 weeks."
            ],
        },
        3: {  # WEDNESDAY
            "title": "Wednesday",
            "workout": [
                "Warm-Up (Dynamic + PVC Drills, ~5 Min)",
                "Deadlift: 4x5 @ 185 lbs. +10 lbs/week initially.",
                "Overhead Press: 4x5 @ 75 lbs. +2.5 lbs/week.",
                "Ring Bodyweight Row: 3x10 (adjust angle/vest).",
                "Ring Push-Ups (Feet Elevated): 3x10, Bodyweight.",
                "Broad Jumps: 4x2, Bodyweight power.",
                "Treadmill Run: 10 min @ ~5 mph. +1 min/week up to 15 min by Week 5."
            ],
        },
        4: {  # THURSDAY
            "title": "Thursday",
            "workout": [
                "Extended Mobility (20 Min Stretch + Foam Roll)",
                "Snatch (Technique): 3x3 @ ~80% Monday’s load (80 lbs in Week 1).",
                "Pallof Holds (Band): 3x10/side, light band.",
                "DB Walking Lunges: 3x8/leg, 2x25 lbs DBs. +5 lbs total every 2 weeks.",
                "Core Plank Variations (Front/Side): 3x45s each.",
                "Zone 2 Cardio (Pool/Tread): 20-25 min moderate."
            ],
        },
        5: {  # FRIDAY
            "title": "Friday",
            "workout": [
                "Warm-Up (Dynamic + Light Plyos)",
                "Power Clean: 4x3 @ 155 lbs. +2.5 lbs/week.",
                "Front Squat: 4x3 @ 135 lbs. +5 lbs/week initially.",
                "Ring Supported Push-Up Hold: 3x15-20s (top position).",
                "Single-Leg RDL (DBs): 3x8/leg, 2x20 lbs DBs. +5 lbs total every 2 weeks.",
                "Sprint Intervals: 6x100m (~90% effort). Reduce rest by 5s every 2 weeks."
            ],
        },
        6: {  # SATURDAY
            "title": "Saturday",
            "workout": [
                "Recovery / Optional Light Cardio (walk, yoga, gentle swim)",
                "No heavy lifting; focus on rest, mobility, quality sleep."
            ],
        }
    }
    return program

def apply_deload_adjustments(workout_list, week):
    """
    Adjust sets/reps/loads for deload weeks (6 & 10).
    We’ll assume a simple approach:
    - For barbell lifts, reduce set count from 4 to 3 and load to ~90% of that day’s baseline.
    - For intervals, reduce # of intervals from 6 to 4 (if present).
    - For ring exercises, reduce 1 set if 4 sets are prescribed (4 -> 3).
    """
    adjusted = []
    for line in workout_list:
        line_lower = line.lower()

        # Reduce sets from 4 to 3 for barbell lifts
        if ("4x" in line_lower or "4x" in line) and any(
            x in line_lower for x in ["snatch", "clean", "press", "bench", "deadlift", "squat"]
        ):
            # Example: "Snatch: 4x3 @ 100 lbs" -> "Snatch: 3x3 @ ~90% of Week 5 load"
            # We'll do a simplistic replacement
            # Also reduce load mention by ~90%
            new_line = line.replace("4x", "3x")
            if "lbs" in new_line:
                # Find numeric portion quickly
                parts = new_line.split("@")
                if len(parts) > 1:
                    weight_part = parts[1].strip()
                    # We'll just insert a note about 90%
                    new_line = f"{parts[0]}@ ~90% of baseline load"
            adjusted.append("(Deload) " + new_line)
        
        # Reduce # of intervals from 6 to 4 if it exists
        elif ("6x" in line_lower or "6x" in line_lower) and any(
            w in line_lower for w in ["interval", "sprint"]
        ):
            new_line = line.replace("6x", "4x")
            adjusted.append("(Deload) " + new_line)

        # If ring exercises are 4x sets, reduce to 3x
        elif "ring" in line_lower and ("4x" in line_lower):
            new_line = line.replace("4x", "3x")
            adjusted.append("(Deload) " + new_line)

        else:
            adjusted.append(line)

    return adjusted

def main():
    # Hard-coded program start date: Sunday, Dec 29, 2024
    start_date = date(2024, 12, 29)

    if len(sys.argv) < 2:
        print("Usage: python daily_workout.py YYYY-MM-DD")
        sys.exit(1)
    
    # Parse input date
    try:
        current_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)

    # Calculate how many days since start_date
    day_offset = (current_date - start_date).days

    # If day_offset is negative, program hasn't started; if > 83, program is past 12 weeks
    if day_offset < 0:
        print(f"Program starts on {start_date}. Today is too early.")
        sys.exit(0)
    if day_offset > 83:
        print("The 12-week program (84 days) has been completed.")
        sys.exit(0)

    # Determine which week (1-12) and day of the week (0=Sunday..6=Saturday)
    week = (day_offset // 7) + 1
    day_of_week = day_offset % 7

    program = get_program_data()
    day_info = program[day_of_week]
    day_title = day_info["title"]
    workout_list = day_info["workout"]

    # Check for deload in Week 6 or Week 10
    if week == 6 or week == 10:
        workout_list = apply_deload_adjustments(workout_list, week)

    # Print results
    print(f"\n--- DAILY WORKOUT ---")
    print(f"Date: {current_date.strftime('%Y-%m-%d')}")
    print(f"Week: {week}  |  Day: {day_title}")
    print("-" * 40)
    for item in workout_list:
        print(f"- {item}")
    print("-" * 40)
    print("Enjoy your training!\n")


if __name__ == "__main__":
    main()