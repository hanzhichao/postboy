<html>
<head>
    <title>{{title}}</title>
    <meta charset="UTF-8">
</head>
<body>
<h1>{{title}}</h1>
<table style="border: 1px; width: 100%">
    <tr>
        <th>用例</th>
        <th>结果</th>
    </tr>
    {% for case in cases %}
    <tr>
        <td>{{case.case_name}}</td>
        <td>{{case.result}}</td>
    </tr>
    {% endfor %}
</table>
</body>
</html>
