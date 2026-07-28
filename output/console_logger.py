from output.timeline_logger import print_timeline


def print_flow_analysis(flow_key, features, analysis):
    """
    Displays flow information, detector outputs,
    AI analysis, behavior analysis,
    final threat score and timeline.
    """

    # ------------------------------------
    # Flow Features
    # ------------------------------------

    print("\n========== FLOW FEATURES ==========")

    for key, value in features.items():
        print(f"{key:25}: {value}")

    print("===================================")

    # ------------------------------------
    # Flow Detectors
    # ------------------------------------

    print("\n========== FLOW DETECTORS ==========")

    if analysis["flow_detectors"]:
        for detector in analysis["flow_detectors"]:
            print(detector)
    else:
        print("No flow detector output.")

    print("====================================")

    # ------------------------------------
    # Host Detectors
    # ------------------------------------

    print("\n========== HOST DETECTORS ==========")

    if analysis["host_detectors"]:
        for detector in analysis["host_detectors"]:
            print(detector)
    else:
        print("No host detector output.")

    print("====================================")

    # ------------------------------------
    # AI Engine
    # ------------------------------------

    print("\n========== AI ENGINE ==========")

    ai = analysis["ai"]

    print(f"Detected : {ai['detected']}")
    print(f"Score    : {ai['score']}")
    print(f"Reason   : {ai['reason']}")

    print("================================")

    # ------------------------------------
    # Activity Classification
    # ------------------------------------

    behavior = analysis["behavior"]

    print("\n====== ACTIVITY CLASSIFICATION ======")
    print(f"Activity   : {behavior.activity}")
    print(f"Confidence : {behavior.confidence}")
    print("=====================================")

    # ------------------------------------
    # Behavior Analysis
    # ------------------------------------

    print("\n========== BEHAVIOR ANALYSIS ==========")

    print(f"Detected : {behavior.detected}")
    print(f"Attack   : {behavior.attack}")
    print(f"Score    : {behavior.score}")
    print(f"Severity : {behavior.severity}")

    print("\nReasons:")

    if behavior.reasons:
        for reason in behavior.reasons:
            print(f"• {reason}")
    else:
        print("• No suspicious behaviour detected.")

    print("=======================================")

    # ------------------------------------
    # Final Threat
    # ------------------------------------

    print("\n========== FINAL THREAT ==========")

    threat = analysis["threat"]

    print(f"Attack   : {threat['attack']}")
    print(f"Score    : {threat['score']}/100")
    print(f"Severity : {threat['severity']}")

    print("\nEvidence:")

    if threat["reasons"]:
        for reason in threat["reasons"]:
            print(f"• {reason}")
    else:
        print("• No evidence collected.")

    print("===================================")

    # ------------------------------------
    # Timeline
    # ------------------------------------

    print_timeline()