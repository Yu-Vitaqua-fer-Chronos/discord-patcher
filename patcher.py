#!/usr/bin/python3

import typing
import os
import shutil
import subprocess
from json import load as jload
from os import chdir, path, system, unlink, walk

verbose = True
stdout = subprocess.PIPE if verbose else subprocess.DEVNULL
stderr = subprocess.STDOUT if verbose else subprocess.DEVNULL

with open('settings.json') as f:
    config = jload(f)

if not os.path.isfile("discord.apk"):
    print("[Download] Downloading Discord APK...")
    code = system(f'curl -L {config["download_url"]} -o discord.apk')
    if code != 0:
        print("[Download] Failed to download APK!")
        raise SystemExit(code)
    print("[Download] APK Downloaded")
else:
    print("[Download] APK already downloaded")

if os.path.exists("discord"):
    print("[Patch] Removing old decompiled files")
    shutil.rmtree("discord")

print("[Decompile] Decompiling APK, this may take a minute...")
r = subprocess.Popen('apktool d -f discord.apk', shell=True, text=True, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr)
r.stdin.write('\r\n' if os.name=='nt' else '\n')
r.communicate()
chdir('discord')

# Things that need some renaming to actually work correctly should be edited and reviewed here every update
bugfixes = []

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
        print(f"[PatchFile] Failed to apply patchfile {file}")
        return
    if verbose:
        print(f"[PatchFile] Applied patchfile {file}")

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
                    if verbose:
                        print(f"[Patch] Applied patches to `{fpath}`")
            except UnicodeDecodeError:
                pass

print("[Patcher] Patching...")
patch('smali')
patch('smali_classes2')
patch('smali_classes3')

print("[Patcher] Patching AndroidManifest.xml...")
with open('AndroidManifest.xml') as f:
    manifest = f.read()
    # manifest = manifest.replace(config['original_package_name'], config['new_package_name'])
    if config["old_app_name"] != config["new_app_name"]:
        manifest = manifest.replace(config['old_app_name'], config['new_app_name'])
    if verbose:
        print("[Patcher] Patched AndroidManifest.xml")

    with open('AndroidManifest.xml', 'w') as f:
        f.write(manifest)

print("[Patcher] Patching complete")
chdir('..')

'''
print("[Icon] Replacing icon...")
shutil.copyfile("assets/icon.png", "discord/res/mipmap-hdpi/ic_logo_round.png")
shutil.copyfile("assets/icon.png", "discord/res/mipmap-hdpi/ic_logo_square.png")
shutil.copyfile("assets/icon.png", "discord/res/mipmap-xhdpi/ic_logo_round.png")
shutil.copyfile("assets/icon.png", "discord/res/mipmap-xhdpi/ic_logo_square.png")
shutil.copyfile("assets/icon.png", "discord/res/mipmap-xxhdpi/ic_logo_round.png")
shutil.copyfile("assets/icon.png", "discord/res/mipmap-xxhdpi/ic_logo_square.png")
shutil.copyfile("assets/icon.png", "discord/res/mipmap-xxhdpi/logo.png")
shutil.copyfile("assets/icon.png", "discord/res/mipmap-xxxhdpi/ic_logo_round.png")
shutil.copyfile("assets/icon.png", "discord/res/mipmap-xxxhdpi/ic_logo_square.png")
shutil.copyfile("assets/icon.png", "discord/res/mipmap-xxxhdpi/logo.png")
'''

print("[Build] Rebuilding APK...")
r = subprocess.Popen('apktool b discord/ -o fosscord.unsigned.apk', shell=True, text=True, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr)
r.stdin.write('\r\n' if os.name=='nt' else '\n')
r.communicate()
print("[Build] APK rebuilt")

print("[Sign] Signing APK...")
r = subprocess.Popen('java -jar uber-apk-signer.jar --apks fosscord.unsigned.apk -o .', shell=True, text=True, stdout=stdout, stderr=stderr)
r.communicate()
print("[Sign] APK signed")

print("[Clean] Cleaning up...")
shutil.rmtree("discord")
unlink("fosscord.unsigned.apk")

print("All done!")
