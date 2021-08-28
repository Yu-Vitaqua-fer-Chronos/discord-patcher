from os import walk, path

# Things that need some renaming to actually work correctly should be edited and reviewed here every update
bugfixes = [
]

# Basic replacements throughout the code to replace discord routes with fosscord routes
replacements = [
  ('discord.com', 'dev.fosscord.com'), # discord.com to dev.fosscord.com
  ('discord.gg', 'dev.fosscord.com/invite'), # discord.gg to dev.fosscord.com/invite
  ('DEBUG:Z = false', 'DEBUG:Z = true') # Enabling debugging
]

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
