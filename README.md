# discord-patcher

This patches the discord.apk for use with different backends/implementations. Edit settings.json to customise options.

# How to use this tool

- copy `example.settings.json` to `settings.json`
- edit `settings.json` as needed
- run `pip install -r requirements.txt` to install python dependencies
- download uber apk signer and place it in the folder, rename it to `uber-apk-signer.jar`
- download apktool and place it in the folder, rename it to `apktool.jar`
- run `python patcher.py` and wait for it to complete. it can take a while.

The URL for the discord APK is set as the last discord stable version using
Java source code.

This tool does not work with the React Native APK, likely because it uses Hermes
bytecode, whereas we're patching smali code (decompiled .dex files).

Icon replacement does not work currently.

Package renaming also does not work.

## Config

`secure` - if `https`/`wss` is used instead of `http`/`ws`.

`base_url` - The base URL, this is used for API routes like `/api/`.

`gateway_url` - The gateway URL, this is used for the gateway connection (via websockets).

`cdn_url` - The CDN url, for uploaded files, images, etc.

`invite_url` - The invite URL, for guild invites.

`package_name` - The package name you want the app to be under, so you can install it alongside your existing discord installation. This may take longer to compile and decompile, but it's recommended.

NOTE: This is broken and will be installed under `com.discord` no matter what the config is set to.

`original_package_name` - The original package name for the APK you're decompiling. dont touch this.

`new_package_name` - the new package name for replacement.

`old_app_name` - the old app name string, dont touch this.

`new_app_name` - the new app name

`download_url` - The download url of the apk to decompile, it's recommended to leave this alone.

`debug` - The option to enable or disable debugging options built into the discord apk. It's recommended to leave this alone.

# Contributions
Thanks to `Puyodead1` for fixing the script after months of neglect :p

