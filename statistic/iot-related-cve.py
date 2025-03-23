import glob
import json
import re

iot_keywords = [
    r'router', r'routers', r'switch', r'switches',
    r'access point', r'ap', r'gateway', r'modem',
    r'ip camera', r'security camera', r'webcam',
    r'smart plug', r'smart bulb', r'smart light',
    r'smart lock', r'smart thermostat', r'smart home',
    r'smart tv', r'smart speaker', r'smart doorbell',
    r'nas', r'media server', r'dvr', r'nvr',
    r'plc', r'scada', r'rfid', r'mcu', r'firmware',
    r'iot', r'internet of things', r'embedded device',
    r'edge device', r'sensor network', r'm2m', r'z-wave', r'zigbee'
]

iot_pattern = re.compile(r'(?i)\b(?:' + '|'.join(iot_keywords) + r')\b')


cwe_pattern = re.compile(r'CWE-\d+')


iot_related = []

for file_path in glob.glob('**/*.json', recursive=True):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            descriptions = data.get('descriptions', [])
            for desc in descriptions:
                if desc.get('lang') == 'en':
                    value = desc.get('value', '')
                    if iot_pattern.search(value):
                        cwes = []
                        for weakness in data.get('weaknesses', []):
                            for d in weakness.get('description', []):
                                if d.get('lang') == 'en':
                                    match = cwe_pattern.search(d.get('value', ''))
                                    if match:
                                        cwes.append(match.group())

                        iot_related.append({
                            'file': file_path,
                            'description': value,
                            'cwes': list(set(cwes))
                        })
                        break
    except Exception as e:
        print(f"Error reading {file_path}: {e}")


print(f"\nTotal IoT-related files: {len(iot_related)}\n")
for item in iot_related:
    print(f"File: {item['file']}")
    print(f"Description: {item['description']}")
    print(f"CWEs: {', '.join(item['cwes']) if item['cwes'] else 'None'}")
    print('-' * 80)

with open("iot-related-cve-results.json", "w") as f:
    json.dump(iot_related, f, indent=4)