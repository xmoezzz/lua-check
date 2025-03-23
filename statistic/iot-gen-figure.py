import json
import re
import matplotlib.pyplot as plt
from collections import Counter, defaultdict


with open('iot-related-cve-results.json', 'r', encoding='utf-8') as f:
    iot_data = json.load(f)

year_pattern = re.compile(r'CVE-(\d{4})')


cwe_pattern = re.compile(r'CWE-\d+')

year_counter = Counter()
for item in iot_data:
    match = year_pattern.search(item['file'])
    if match:
        year = match.group(1)
        year_counter[year] += 1

cwe_counter = Counter()
for item in iot_data:
    if not item['cwes']:
        cwe_counter['Other'] += 1
    else:
        for cwe in item['cwes']:
            if cwe_pattern.match(cwe):
                cwe_counter[cwe] += 1
            else:
                cwe_counter['Other'] += 1



# -- 1. bar chart --
years = sorted(year_counter.keys())
counts = [year_counter[y] for y in years]

plt.figure(figsize=(10, 5))
plt.bar(years, counts)
plt.xlabel('Year')
plt.ylabel('Number of IoT Vulnerabilities')
plt.title('IoT Vulnerabilities by Year')
plt.xticks(rotation=45, ha='right') 
plt.tight_layout()
plt.savefig('iot_vulns_by_year.png')
plt.show()

# -- 2. CWE pie chart --
top_n = 8
most_common = cwe_counter.most_common(top_n)
other_count = sum([count for cwe, count in cwe_counter.items() if (cwe, count) not in most_common])
labels = [cwe for cwe, _ in most_common]
sizes = [count for _, count in most_common]

# if other_count > 0:
#     labels.append('Other')
#     sizes.append(other_count)

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('IoT Vulnerabilities by CWE Category')
plt.axis('equal')  # Equal aspect ratio ensures the pie is a circle.
plt.tight_layout()
plt.savefig('iot_vulns_by_cwe.png')
plt.show()
