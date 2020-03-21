<!DOCTYPE html>
<html>
<head>
    <title>>Test Report</title>
</head>
<body>
    <h1>Test Report</h1>
    <table border="1px;">
        <tr bgcolor="#CCC"><th>Case Name</th><th>Url</th><th>Result</th></tr>
        {% for case in results %}
        <tr><td>{{ case[0] }}</td><td>{{ case[1][0][0] }}</td><td>{{ case[1][0][1] }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>