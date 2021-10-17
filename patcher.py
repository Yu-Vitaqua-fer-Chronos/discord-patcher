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
system('apktool d -r discord.apk')
chdir('discord')
print("\nDecompiled the apk, beginning patching process.")

# Things that need some renaming to actually work correctly should be edited and reviewed here every update
bugfixes = [
]

protocol = ('http://', 'ws://')
if config['secure']:
    protocol = ('https://', 'wss://')

# Basic replacements throughout the code to replace discord routes with fosscord routes
# NOTE: Order of replacements is VERY important and will probably have to do stupid stuff to make it customisable
replacements = [
  ('https://cdn.discordapp.com', protocol[0]+config['cdn_url']), # cdn.discord.com to cdn url
  ('https://media.discordapp.net', protocol[0]+config['cdn_url']), # discord media proxy to cdn url
  ('https://gateway.discord.gg', protocol[1]+config['gateway_url']), # gateway.discord.com to gateway url
  ('https://discord.com', protocol[0]+config['base_url']), # discord.com to the base url
  ('https://discordapp.com', protocol[0]+config['base_url']), # Extra change just in case discordapp is still used in the code somewhere
  ('https://discord.gg', protocol[0]+config['invite_url']), # discord.gg to the invite url
  ('https://discord.new/', protocol[0]+config['base_url']+'/template') # discord.new to template url
]

if config.get('debug'):
    replacements.append(("DEBUG:Z = false", "DEBUG:Z = true")) # Enables debug if it's true in the config

def patchfile(file):
    code = system("patch -p1 --no-backup-if-mismatch -i ../patches/"+file)
    if code != 0:
        print("Failed to apply patchfile `"+file+"`")
        return
    print("Applied patchfile `"+file+"`")

system("mv AndroidManifest.xml ..")

def patch(folder):
    for root, _, files in walk(path.join('.', folder)):
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

patch('smali')
patch('smali_classes2')
patch('smali_classes3')
patchfile('nozlib.patch')

system("mv ../AndroidManifest.xml .")

#if config['package_name']:
#   with open('AndroidManifest.xml') as f:
#        manifest = f.read()
#    manifest = manifest.replace(config['original_package_name'], config['package_name'])
#    print("Applied patches to `AndroidManifest.xml`")
print("\nFinished applying patches\n\nRecompiling APK...")
chdir('..')
system('apktool b discord/ -o fosscord.unsigned.apk')
print("\nRecompiled APK.\nChecking if keystore exists...")
if not path.exists('keystore.jks'):
    print("\nNo keystore exists, creating one...")
    system('keytool -genkey -v -keystore keystore.jks -keyalg RSA -keysize 2048 -validity 10000')
print("\nSigning APK...")
system('apksigner sign --ks keystore.jks --out fosscord.signed.apk fosscord.unsigned.apk')
print("\nFinished signing the APK, the APK's name is `fosscord.signed.apk`.")
