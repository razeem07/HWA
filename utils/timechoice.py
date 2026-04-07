def generate_time_choices():
    times = []
    for hour in range(0, 24):
        for minute in [0, 30]:  # 30 min interval (change if needed)
            time_24 = f"{hour:02d}:{minute:02d}"
            
            # Convert to 12-hour format
            hour_12 = hour % 12 or 12
            am_pm = "AM" if hour < 12 else "PM"
            time_12 = f"{hour_12:02d}:{minute:02d} {am_pm}"

            times.append((time_24, time_12))
    
    return times


TIME_CHOICES = generate_time_choices()