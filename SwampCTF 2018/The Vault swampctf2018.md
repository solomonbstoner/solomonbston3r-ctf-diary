#For The Vault in swampctf 2018


We are given a login form. Whatever credentials we enter to the form is submitted to the function `login()`.
```
<form class="form-signin" onsubmit="return login()">
```


### Analysis of the login function

This is the `login()` function:
```
<script>
function login(){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4) {
			if(this.status == 200){
				alert(xhttp.responseText);
				window.location.href = 'https://youtu.be/rWVeZx2IP30?t=3';
			} else {
				alert('Invalid Credentials')
			}
		}
	};
	xhttp.open("POST", "/login/"+document.getElementById('inputName').value+"."+document.getElementById('inputPassword').value, true);
	xhttp.send();
	return false;
}

</script>
```


You may ignore the youTube link. If the user credentials are correct, we execute `alert(xttp.responseText);`. I assume the flag is in there. If the credentials are wrong, we execute `alert('Invalid Credentials')`. 


Remember, javascript is executed on the client side, so that means we are free to change how the user credentials are sent to the server via AJAX and what we do with the response.

Assuming the flag is in `xhttp.responseText`, I thought I could bypass the login by changing the script to
```
	if(this.status == 200){
		alert(xhttp.responseText);
		window.location.href = 'https://youtu.be/rWVeZx2IP30?t=3';
	} else {
		console.log(xhttp.responseText);
	}
```

I gave a random input username: `user` and password: `password`. I got this response:
```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>No such user: user</pre>
</body>
</html>
```

Ok, so... which user exists? Hint: "Only the DUNGEON_MASTER may enter the vault".

Let's try the input username: `DUNGEON_MASTER` and password: `password`. I got this response:
```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>test_hash [5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8] does not match real_hash[40f5d109272941b79fdf078a0e41477227a9b4047ca068fff6566104302169ce]</pre>
</body>
</html>
```

This is a big, big clue. `hash` means a hashing algorithm is involved. There are 64 characters in the hash, each of them representing a nibble (ie 4 bits).  It smells of SHA-256.


### Decoding the password

I headed over to the online [hash decryptor](https://hashtoolkit.com/) and tested the hash `5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8` to see if it was the SHA-256 hash of `password`.

It was. This confirms that the login does not include a salt of any kind, meaning that we can simply decrypt the `real_hash`, and that will be our input password.

I [tested it out](http://hashtoolkit.com/reverse-hash/?hash=40f5d109272941b79fdf078a0e41477227a9b4047ca068fff6566104302169ce), and it worked. The DUNGEON_MASTER's password is `smaug123`.

### Winning

Giving input username:`DUNGEON_MASTER` and password:`smaug123` returns us the flag `flag{somewhere_over_the_rainbow_tables}`.


END
