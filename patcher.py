#!/usr/bin/python3

from os import walk, path, chdir, system
from json import load as jload

with open('settings.json') as f:
    config = jload(f)

print("Downloading `discord.apk`....")
code = system(f'wget {config["download_url"]} -O discord.apk -o download.log')
if code != 0:
    print("Something went wrong while downloading the file, check `download.log`")
    raise SystemExit(code)
print("APK downloaded\nDecompiling APK...")
if not config['package_name']:
    system('apktool d -r discord.apk')
else:
    print(f"Custom package name will be `{config['package_name']}`. This may take longer to decompile and build.")
    system('apktool d discord.apk')
chdir('discord')
print("\nDecompiled the apk, beginning patching process.")

# Things that need some renaming to actually work correctly should be edited and reviewed here every update
bugfixes = [
]

# Basic replacements throughout the code to replace discord routes with fosscord routes
# NOTE: Order of replacements is VERY important and will probably have to do stupid stuff to make it customisable
replacements = [
  ('cdn.discordapp.com', config['cdn_url']),
  ('gateway.discord.gg', config['gateway_url']),
  ('discord.com', config['base_url']), # discord.com to the base url of settungs.json
  ('discordapp.com', config['base_url']), # Extra change just in case discordapp is still used in the code somewhere
  ('discord.gg', config['invite_url']), # discord.gg to the invite url
]

if config.get('debug'):
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

if config['package_name']:
    with open('AndroidManifest.xml') as f:
        manifest = f.read()
    manifest = manifest.replace(config['original_package_name'], config['package_name'])
    print("Applied patches to `AndroidManifest.xml`")
print("\nFinished applying patches\n\nRecompiling APK...")
chdir('..')
system('apktool b -f -d discord/ -o fosscord.unsigned.apk')
print("\nRecompiled APK.\nChecking if keystore exists...")
if not path.exists('keystore.jks'):
    print("\nNo keystore exists, creating one...")
    system('keytool -genkey -v -keystore keystore.jks -keyalg RSA -keysize 2048 -validity 10000')
print("\nSigning APK...")
system('apksigner sign --ks keystore.jks --out fosscord.signed.apk fosscord.unsigned.apk')
print("\nFinished signing the APK, the APK's name is `fosscord.signed.apk`. You should be able to install this alongside your current discord installation.")
