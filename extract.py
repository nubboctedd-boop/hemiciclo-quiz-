import re
import json
import urllib.request
import os
import html

html_file = r"C:\Users\Sergio\.gemini\antigravity-cli\brain\a2883a1a-4e73-450c-b78a-3c67325ae1a7\.system_generated\steps\4\content.md"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# The HTML uses &quot; for quotes in the props attribute.
content = html.unescape(content)

# We want to extract candidates from the JSON-like structures.
# Example: "dni":[0,"40433187"],"name":[0,"Miguel Angel Torres Morales"],"partyCode":[0,1366],"mode":[0,"nacional"],"districtName":[0,"Distrito Nacional Único"],"listNumber":[0,1],"votes":[0,285572],"candidateId":[0,18],"photoUrl":[0,"https://mpesije.jne.gob.pe/apidocs/789b7714-8633-4a59-a89b-7fab4646fef1.jpeg"]

pattern = r'"dni":\[0,"(.*?)"\],"name":\[0,"(.*?)"\],"partyCode":\[0,(\d+)\],"mode":\[0,"(.*?)"\],"districtName":\[0,"(.*?)"\],"listNumber":\[0,(\d+)\],"votes":\[0,(\d+)\],"candidateId":\[0,(\d+)\],"photoUrl":\[0,"(.*?)"\]'

matches = re.findall(pattern, content)

candidates = []
for m in matches:
    candidate = {
        "dni": m[0],
        "name": m[1],
        "partyCode": int(m[2]),
        "mode": m[3],
        "districtName": m[4],
        "listNumber": int(m[5]),
        "votes": int(m[6]),
        "candidateId": int(m[7]),
        "photoUrl": m[8]
    }
    # To avoid duplicates
    if not any(c['dni'] == candidate['dni'] for c in candidates):
        candidates.append(candidate)

print(f"Found {len(candidates)} unique candidates.")

os.makedirs('C:/Users/Sergio/hemiciclo_data', exist_ok=True)
os.makedirs('C:/Users/Sergio/hemiciclo_data/images', exist_ok=True)

for c in candidates:
    img_url = c['photoUrl']
    ext = img_url.split('.')[-1]
    img_filename = f"C:/Users/Sergio/hemiciclo_data/images/{c['dni']}.{ext}"
    c['localPhotoPath'] = f"images/{c['dni']}.{ext}"
    
    if not os.path.exists(img_filename):
        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(img_filename, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Downloaded image for {c['name']}")
        except Exception as e:
            print(f"Failed to download image for {c['name']}: {e}")

with open('C:/Users/Sergio/hemiciclo_data/candidatos.json', 'w', encoding='utf-8') as f:
    json.dump(candidates, f, indent=4, ensure_ascii=False)

print("Extraction complete. Data saved to C:/Users/Sergio/hemiciclo_data/candidatos.json")
