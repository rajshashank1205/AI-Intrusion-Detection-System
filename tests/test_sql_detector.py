from detection.detectors.sql_injection_detector import SQLInjectionDetector

detector = SQLInjectionDetector()

packet = {
    "payload": "GET /login.php?id=1' OR '1'='1 HTTP/1.1"
}

result = detector.detect(packet)

print(result)