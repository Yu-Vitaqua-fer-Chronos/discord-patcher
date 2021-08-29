from os import walk, path
from json import load as jload

with open('settings.json') as f:
    config = jload(f)

# Things that need some renaming to actually work correctly should be edited and reviewed here every update
bugfixes = [
]

# Basic replacements throughout the code to replace discord routes with fosscord routes
# NOTE: Order of replacements is VERY important and will probably have to do stupid stuff to make it customisable
replacements = [
  ('cdn.discord.com', 'REPLACE CDN URL HERE'),
  ('gateway.discord.gg', 'REPLACE GATEWAY URL HERE')
  ('discord.com', config['base_url']), # discord.com to the base url of settungs.json
  ('discord.gg', config['invite_url']), # discord.gg to the invite url
  ('REPLACE CDN URL HERE', config['cdn_url']),
  ('REPLACE GATEWAY URL HERE', config['gateway_url']),
]

if config.get('debug').lower():
    replacements.append(("DEBUG:Z = false", "DEBUG:Z = true")) # Enables debug if it's true in the config

# TODO: Potentially add support for patching files with .patch files?

for root, _, files in walk('.'):
    for file in files:
        fpath = path.join(root, file)
        try:
            with open(fpath) as f:
                data = tmp = f.read()
            for bugfix in bugfixes:
                data = data.replace(*bugfix)
            for replacement in replacements:
                data = data.replace(*replacement)
            if tmp != data:
                with open(fpath, 'w+') as f:
                    f.write(data)
                print(f"Applied patches to `{fpath}`")
        except UnicodeDecodeError:
            pass
