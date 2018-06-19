# Stealing Unattended Certificates - 775

> You need access into the Home Invasion network before you can solve this challenge.
>  
> There is only one flag in this challenge. You need the Lux G1 firmware first! The inner HEXADECIMAL is ALL LOWERCASE LETTERS
>  
> I wonder if you can extract any (supposed to be secret) key that MAY be in the firmware! Answer in the form HI{first 5 bytes of SSL private key registered to LuxCorp in hexadecimal form}

To solve this challenge, we had to first solve the challenge, Firmware Reverse Easy. After downloading the firmware and inspecting it with `binwalk`, we noticed a file called `"Private key in DER format"`.
```
➜  iotctf2018 binwalk LUXFirmware-G1-Sat16June2018-003.bin 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
43932         0xAB9C          SHA256 hash constants, little endian
308701        0x4B5DD         Private key in DER format (PKCS header length: 4, sequence length: 315
309020        0x4B71C         Unix path: /Users/ragulbalaji/Library/Arduino15/packages/esp8266/hardware/esp8266/2.4.1/libraries/ESP8266WiFi/src/include/DataSource.h
312633        0x4C539         XML document, version: "1.0"
359575        0x57C97         Unix path: /Users/ragulbalaji/Library/Arduino15/packages/esp8266/hardware/esp8266/2.4.1/cores/esp8266/abi.cpp
```

A private key is supposed to be secret, so we knew that the flag was in there. We extracted it for further analysis.
```
➜  iotctf2018 binwalk --dd=".*" LUXFirmware-G1-Sat16June2018-003.bin

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
43932         0xAB9C          SHA256 hash constants, little endian
308701        0x4B5DD         Private key in DER format (PKCS header length: 4, sequence length: 315
309020        0x4B71C         Unix path: /Users/ragulbalaji/Library/Arduino15/packages/esp8266/hardware/esp8266/2.4.1/libraries/ESP8266WiFi/src/include/DataSource.h
312633        0x4C539         XML document, version: "1.0"
359575        0x57C97         Unix path: /Users/ragulbalaji/Library/Arduino15/packages/esp8266/hardware/esp8266/2.4.1/cores/esp8266/abi.cpp

➜  _LUXFirmware-G1-Sat16June2018-003.bin-0.extracted file *
4B5DD: DER Encoded Key Pair, 512 bits
4B71C: DIY-Thermocam raw data (Lepton 2.x), scale 29556-24946, spot sensor temperature 0.000000, unit celsius, color scheme 0, calibration: offset 0.000000, slope 9671406556917033397649408.000000
4C539: data
57C97: data
AB9C:  data
```

The file of interest with our private key is now in the file `4B5DD`. It's an arbitrary name given by the extraction tool.

This [website](http://fileformats.archiveteam.org/wiki/DER_encoded_RSA_private_key) was helpful in teaching us how to extract the private key from the key pair. 

At first we ran `openssl rsa -noout -text -inform DER -in 4B5DD`. It was wrong. It gave us the *components* of the key, not the key itself.
```
➜  _LUXFirmware-G1-Sat16June2018-003.bin-0.extracted  openssl rsa -noout -text -inform DER -in 4B5DD
Private-Key: (512 bit)
modulus:
    00:af:81:fd:06:b4:76:b5:5b:5d:47:37:8c:8a:d5:
    25:30:26:bd:74:d8:60:d4:2f:80:1f:73:fc:6f:74:
    3e:9f:02:9a:23:83:1d:46:2c:cc:44:38:98:d7:9c:
    e5:d6:f8:98:68:51:ee:b1:65:48:59:5e:67:ea:2e:
    e4:69:4f:3a:53
publicExponent: 65537 (0x10001)
privateExponent:
[...]
    2d:cd:4d
exponent2:
    1c:13:52:95:77:ea:dc:f5:67:f1:a0:5f:33:0a:0b:
    98:b9:22:0f:26:7c:cb:e5:40:71:f2:5d:2e:b7:97:
    c7:d1
coefficient:
    65:53:f4:03:ae:b5:ae:d1:f2:b6:a9:53:e2:ab:f2:
    07:27:dc:da:af:ed:ed:c0:b6:00:f8:40:f3:98:12:
    52:45
```

The correct command to run was:
```
➜  _LUXFirmware-G1-Sat16June2018-003.bin-0.extracted openssl rsa -inform DER -in 4B5DD -out example-pem.key
writing RSA key
➜  _LUXFirmware-G1-Sat16June2018-003.bin.extracted cat example-pem.key 
-----BEGIN RSA PRIVATE KEY-----
MIIBOwIBAAJBAK+B/Qa0drVbXUc3jIrVJTAmvXTYYNQvgB9z/G90Pp8CmiODHUYs
zEQ4mNec5db4mGhR7rFlSFleZ+ou5GlPOlMCAwEAAQJBAIMTwBer3CSicc3ojMx7
V+TYahLEL70JJNVY2KWc2dAC8enp6aRSGwy+VzxMImxgVM5qqMm0mIOOOwh3Ixef
Z6ECIQDlMaXmctvYzY9beIJgWHTCUpkhMj6eIpfmg7fsda95uwIhAMQI6NaOYf6W
zIiZoii6TaUIGDpGCjYPSHlk8nJbRkxJAiEAmd5RAHuP+OdYHRK0hLYd/O+y+kRf
IY8b55f6fHctzU0CIBwTUpV36tz1Z/GgXzMKC5i5Ig8mfMvlQHHyXS63l8fRAiBl
U/QDrrWu0fK2qVPiq/IHJ9zar+3twLYA+EDzmBJSRQ==
-----END RSA PRIVATE KEY-----
```

> A key file is plain text, with base64-encoded payload data. It contains a line that reads "-----BEGIN RSA PRIVATE KEY-----".
>  
> --[Source](http://fileformats.archiveteam.org/wiki/PEM_encoded_RSA_private_key)

The RSA key is in base64 format. The flag is the first 5 *bytes*. We used an online base64 to bytes converter to get our flag.


![](../../img/iot_ctf2018_stealing_unatt_certs_base64_to_bytes.png)

Our flag was therefore `HI{3082013b02}`.

### Alternate, easier method

Actually, there is a way easier method. We could just do a hexdump of the key, `4B5DD`. We actually tried that, but we forgot to take little endinanness into account, so we did not get the flag. We went one big round instead.
```
➜  _LUXFirmware-G1-Sat16June2018-003.bin-0.extracted hexdump 4B5DD | head
0000000 8230 3b01 0102 0200 0041 81af 06fd 76b4
0000010 5bb5 475d 8c37 d58a 3025 bd26 d874 d460
[...]
```
