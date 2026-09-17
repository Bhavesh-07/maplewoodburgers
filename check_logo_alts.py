import os, glob, re

templates_dir = r'c:/wamp64/www/maplewood-live-project/templates'
skip = {'admin.html', 'admin-backup.html', 'login.html', 'loyalty_admin.html', 'reviews_admin.html', 'settings.html'}
files = sorted(glob.glob(os.path.join(templates_dir, '*.html')))

for f in files:
    name = os.path.basename(f)
    if name in skip:
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    # Find all img tags with the logo filename
    matches = re.findall(r'<img[^>]*Maplewood-Burgers-Logo[^>]*>', content, re.IGNORECASE)
    if matches:
        print(f'\n=== {name} ===')
        for m in matches:
            print(' ', m)
