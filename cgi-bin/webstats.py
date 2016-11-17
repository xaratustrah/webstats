#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple CGI script that shows server's GPU, CPU and memory load on the browser.

Xaratustrah
2016

"""

import subprocess
from jinja2 import Template

CMD = [
    'uname -n',
    'uname -mrsv',
    'date',
    'sar -r 1 1',
    'sar -P ALL 1 1',
    'nvidia-smi',
]

HTML_TMPL = """
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>

    <!--Check JavaScript-->

    <noscript>
      <img src="no_js.gif"
    alt="Why did you disable JavaScript? Without JavaScript you can't see the navigation bar."/>
    </noscript>

    <link href="http://thomasf.github.io/solarized-css/solarized-dark.min.css" rel="stylesheet"></link>

    <!--Here comes the document title-->

    <title>{{title}}</title>

    <a href="https://github.com/xaratustrah/webstats"><img style="position: absolute; top: 0; right: 0; border: 0;"
    src="https://camo.githubusercontent.com/652c5b9acfaddf3a9c326fa6bde407b87f7be0f4/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f6f72616e67655f6666373630302e706e67"
    alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_orange_ff7600.png"></a>
  </head>

  <body>

    <br/>

    <br/>
    Hello from
    <br/>
    {% if not ok0 %}
    <b><code>{{ out0 }}</code></b>
    {% else %}
    Failed to run {{ cmd0 }}:
    <b><code>{{ err0 }}</b></code>
    {% endif %}
    <br/>

    <br/>
    Running:
    <br/>
    {% if not ok1 %}
    <b><code>{{ out1 }}</code></b>
    {% else %}
    Failed to run {{ cmd1 }}:
    <b><code>{{ err1 }}</b></code>
    {% endif %}
    <br/>

    <br/>
    Time:
    <br/>
    {% if not ok2 %}
    <b><code>{{ out2 }}</code></b>
    {% else %}
    Failed to run {{ cmd2 }}:
    <b><code>{{ err2 }}</b></code>
    {% endif %}
    <br/>

    <br/>
    Memory:
    <br/>
    {% if not ok3 %}
    <b><code>{{ out3 }}</code></b>
    {% else %}
    Failed to run {{ cmd3 }}:
    <b><code>{{ err3 }}</b></code>
    {% endif %}
    <br/>

    <br/>
    CPU:
    <br/>
    {% if not ok4 %}
    <b><code>{{ out4 }}</code></b>
    {% else %}
    Failed to run {{ cmd4 }}:
    <b><code>{{ err4 }}</b></code>
    {% endif %}
    <br/>

    <br/>
    GPU:
    <br/>
    {% if not ok5 %}
    <b><code>{{ out5 }}</code></b>
    {% else %}
    Failed to run {{ cmd5 }}:
    <b><code>{{ err5 }}</b></code>
    {% endif %}
    <br/>

  </body>
</html>

 """


def run_cmd(cmd_string):
    try:
        p = subprocess.Popen(cmd_string.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ok = p.wait()
        out, err = p.communicate()
    except FileNotFoundError:
        out = None
        err = None
        ok = True

    return ok, out, err


def main():
    tmpl = Template(HTML_TMPL)

    ok0, out0, err0 = run_cmd(CMD[0])
    ok1, out1, err1 = run_cmd(CMD[1])
    ok2, out2, err2 = run_cmd(CMD[2])
    ok3, out3, err3 = run_cmd(CMD[3])
    ok4, out4, err4 = run_cmd(CMD[4])
    ok5, out5, err5 = run_cmd(CMD[5])

    html = tmpl.render(title='WebStats',
                       ok0=ok0, err0=err0, out0=out0, cmd0=CMD[0],
                       ok1=ok1, err1=err1, out1=out1, cmd1=CMD[1],
                       ok2=ok2, err2=err2, out2=out2, cmd2=CMD[2],
                       ok3=ok3, err3=err3, out3=out3, cmd3=CMD[3],
                       ok4=ok4, err4=err4, out4=out4, cmd4=CMD[4],
                       ok5=ok5, err5=err5, out5=out5, cmd5=CMD[5],
                       )

    print(html)


# -------------

if __name__ == '__main__':
    main()
