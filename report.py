from jinja2 import Template

class Report(object):
    def __init__(self, results, tpl="report.tpl"):
        self.tpl = tpl
        self.results = results

    def save(self, path):

        with open(self.tpl) as f:
            html = f.read().strip()
        
        t = Template(html)
        content=t.render(results=self.results)
        with open(path, "w") as f:
            f.write(content)