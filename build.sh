echo "Decompiling APK"
echo
apktool d discord-beta.apk
echo
cd discord-beta/
echo "Running the patcher"
echo
python ../patcher.py
echo
cd ..
echo "Recompiling the APK with patches"
apktool b -f -d discord-beta/ -o fosscord.unsigned.apk
echo
echo "APK compiled"
# Command to sign the apk
echo
echo "I am not able to sign the APK so you'll need to do it manually"
