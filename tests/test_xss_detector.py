from detection.detectors.xss_detector import XSSDetector

detector = XSSDetector()

packet = {
    "src_port" : 54321,
    "dst_port" : 8000,
    "payload" : "<script>alert('Hacked'</script>)"
}

result = detector.detect(packet)

print(result)