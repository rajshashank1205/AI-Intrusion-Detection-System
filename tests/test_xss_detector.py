from detection.detectors.xss_detector import XSSDetector

detector = XSSDetector()

packet = {
    "payload": "<script>alert('Hacked')</script>"
}

result = detector.detect(packet)

print(result)