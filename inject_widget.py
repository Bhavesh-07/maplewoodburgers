import os

template_dir = 'templates'

script_code = """
    <!-- LeadConnector Chat Widget -->
    {% if settings.chat_widget_key %}
    <script src="https://widgets.leadconnectorhq.com/loader.js" 
            data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" 
            data-widget-id="{{ settings.chat_widget_key }}">
    </script>
    {% endif %}
"""

def inject_widget(filepath):
    # Skip admin and login pages
    if 'admin.html' in filepath or 'login.html' in filepath:
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Avoid duplicate injection
    if 'LeadConnector Chat Widget' in content:
        return

    # Inject before </body>
    if '</body>' in content:
        new_content = content.replace('</body>', script_code + '\n</body>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Injected widget into {filepath}")

for filename in os.listdir(template_dir):
    if filename.endswith('.html'):
        inject_widget(os.path.join(template_dir, filename))
