# discord-patcher
This patches the discord.apk for use with different backends/implementations. Edit settings.json to customise options.

## Config
`base_url` - The base URL, this is used for API routes like `/api/`.

`gateway_url` - The gateway URL, this is used for the gateway connection (via websockets).

`cdn_url` - The CDN url, for uploaded files, images, etc.

`invite_url` - The invite URL, for guild invites.

`package_name` - The package name you want the app to be under, so you can install it alongside your existing discord installation. This may take longer to compile and decompile, but it's recommended.
NOTE: This is broken and will be installed under `com.discord` no matter what the config is set to.

`original_package_name` - The original package name for the APK you're decompiling. It's recommended to leave this alone.
NOTE: Currently useless i don't know why it's still here

`download_url` - The download url of the apk to decompile, it's recommended to leave this alone.

`debug` - The option to enable or disable debugging options built into the discord apk. It's recommended to leave this alone.


## Current Issues
This uses discord's endpoint URLs, and uncommenting the replacer script just gives a network error when attempting to login.

## Notes
This is currently broken, you are welcome to make PRs if you wish
