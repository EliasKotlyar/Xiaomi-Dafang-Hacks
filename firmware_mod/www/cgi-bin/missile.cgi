#!/bin/sh

echo "Content-type: text/html"
echo ""

cat << EOF
<!DOCTYPE html>
<html>

<head>
    <title>Fang Hacks</title>
    <style type="text/css">
        body { background-color: #B0E0E6; font-family: verdana, sans-serif; }
        .err { color: red; }
        hr { height: 1px; border: 0; border-top: 1px solid #aaa; }
        button, input[type=submit] { background-color: #ddeaff; }
        .tbl { border-collapse: collapse; border-spacing: 0;}
        .tbl th { text-align: left; vertical-align: top; font-weight: bold; padding: 10px 5px; border-style: solid; border-width: 1px; overflow: hidden; word-break: normal; }
        .tbl td { padding: 10px 5px; border-style: solid; border-width: 1px; overflow: hidden; word-break: normal; }
    </style>
</head>

<body>
EOF

source header.cgi

cat << EOF
<br/>
<br/>
</div>
</p>
<hr/>
<table class='tbl'>
    <script>
        function call(url){
                var xhr = new XMLHttpRequest();
                xhr.open('GET', url, true);
                xhr.send();
        }
    </script>
    <tr>
        <th>Missile:</th>
        <td>
            &nbsp;&nbsp;&nbsp;&nbsp;<button title="" type="button" onclick="call('missile_cmd.cgi?cmd=-U')">&nbsp;Up&nbsp;</button>
            <br>
            <button title="" type="button" onclick="call('missile_cmd.cgi?cmd=-L')">Left</button>&nbsp;
            <button title="" type="button" onclick="call('missile_cmd.cgi?cmd=-R')">Right</button>
            <br> &nbsp;&nbsp;&nbsp;
            <button title="" type="button" onclick="call('missile_cmd.cgi?cmd=-D')">Down</button> &nbsp;&nbsp;&nbsp;
            <button title='' type='button' onClick="call('missile_cmd.cgi?cmd=-F')">Fire</button>
        </td>
        <td>
            <button title='' type='button' onClick="call('missile_cmd.cgi?cmd=-F')">Fire</button>
        </td>

    </tr>

</table>
</div>
</body>

</html>
EOF
