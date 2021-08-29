#!/bin/sh

echo "Decompiling APK"
echo
apktool d -r Aliucord.apk
echo
cd Aliucord/
echo "Running the patcher"
echo
python3 ../patcher.py
echo
cd ..
echo "Recompiling the APK with patches"
apktool b -f -d Aliucord/ -o fosscord.unsigned.apk
echo
echo "APK compiled"
# Command to sign the apk
if [ ! -f "keystore.jks" ]; then
 echo "Keystore file doesn't exist, generating"
 keytool -genkey -v -keystore keystore.jks -keyalg RSA -keysize 2048 -validity 10000
else
 echo "Keystore file exists, skipping generation"
fi
echo "Signing apk"
apksigner sign --ks keystore.jks --out fosscord.signed.apk fosscord.unsigned.apk
