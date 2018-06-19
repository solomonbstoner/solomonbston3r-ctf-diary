# Decrypt Everyone! - 991

> You need access into the Home Invasion network before you can solve this challenge.
>  
> There is only one flag in this challenge. you need to do Stealing Unattended Certificates first
>  
> Its your time to proxy the NSA and listen to everyone's private communications with the light bulb!
>  
> Answer in the form HI{the value of the chal hash attribute in the HTTPS GET request to https://192.168.51.5/lux_fillcolor}


To solve this challenge, we had to solve Stealing Unattended Certificates first. We needed the private key, `example-pem.key`.
```
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

We downloaded the pcap file `securelights192.168.51.5.pcapng` and opened it with Wireshark. We knew from the challenge Probing Ports that there was service running on port 443 (ie HTTPS). Traffic on HTTPS is encrypted, and only the smart light device should be able to decrypt it with its private key. From the challenge Stealing Unattended Certificates, we got a copy of said private key. We were in power to decrypt traffic intended for the smart light, and so we did! :D

This [website](https://support.citrix.com/article/CTX116557) helped us decrypt the traffic. First, we headed to `Edit > Preferences`, then selected `SSL` from `Protocols` tab on the left side.

![](../../img/iot_ctf2018_decrypt_everyone_add_rsa_key.png)

Under `RSA keys list`, we clicked `Edit`, and added the details shown in the screenshot below.

![](../../imgiot_ctf2018_decrypt_everyone_decrypt_traffic.png)

After we saved the settings, Wireshark decrypted the traffic. But we still need to find our packet! We know that the flag is in the HTTPS GET request to `https://192.168.51.5/lux_fillcolor`. So we added `"http.request"` to the filter,  and we found the HTTP GET request! :D


![](../../img/iot_ctf2018_decrypt_everyone_searching_for_http.png)



We followed the SSL traffic, and got the cha1 hash attribute. The flag was `HI{eaa4609bdd922e5b6efee59dd7894b49109ed556}`. (Note: you can follow HTTP traffic too.)

![](../../img/iot_ctf2018_decrypt_everyone_flag.png)
