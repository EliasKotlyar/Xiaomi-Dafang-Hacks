#!/bin/sh

awk '

BEGIN { OFS = "\t"; } 

/\<Cell/ {
	# Print previous AP
	if (wpa) {
	  security = "WPA"
	} else if (wep) { 
	  security = "WEP" 
	} else { 
	  security = "None"
	}
	if (essid) print essid, address, security, quality;
	# Reset security flags.
	wep = 0; wpa = 0;

	address = $5
}

/\<ESSID:/ {
	essid = substr($0, index($0, ":") + 1);
	essid = substr(essid, 2, length(essid) - 2)  # discard quotes
}

/\<Quality/ {
	split($1, q, "[:=]"); # q[1] -> "Quality", q[2] -> value
	split(q[2], qvalues, "/");
	if (qvalues[2]) {
		quality = int(qvalues[1] / qvalues[2] * 100); # we have both parts, divide
	} else {
		quality = qvalues[1]; # we have only one part, use it as-is
	}
}

/\<Encryption key:(o|O)n/ { wep = 1 }

/\<IE:.*WPA.*/ { wpa = 1 }

END {
	# Print last AP
	if (wpa) { security = "WPA" } else { if (wep) { security = "WEP" } else { security = "None" }}
	if (essid) print essid, address, security, quality;
}'
