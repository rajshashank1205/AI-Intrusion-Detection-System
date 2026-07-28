from detection.timeline import timeline


def print_timeline():

    events = timeline.get_events()

    if not events:
        return

    print("\n========== ATTACK TIMELINE ==========")

    for event in events:

        print(
            f"[{event['time'].strftime('%H:%M:%S')}] "
            f"{event['severity']:<8} "
            f"{event['source']:<20} "
            f"{event['event']}"
        )

    print("=====================================")

    # Clear timeline after printing
    timeline.clear()