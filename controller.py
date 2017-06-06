#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask plot test

based on:
http://hplgit.github.io/web4sciapps/doc/web/index.html
"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import subprocess, re

app = Flask(__name__)
Bootstrap(app)

CMD = [
    'uname -n',
    'uname -mrsv',
    'date',
    'sar -r 1 1',
    'nvidia-smi --query-gpu=gpu_uuid,memory.total,memory.used,memory.free,temperature.gpu,utilization.gpu,utilization.memory --format=csv',
    'sar -P ALL 1 1',
]


def run_cmd(cmd_string):
    try:
        p = subprocess.Popen(cmd_string.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ok = p.wait()
        out, err = p.communicate()
    except FileNotFoundError:
        out = b''
        err = b''
        ok = True

    return ok, out, err


@app.route("/")
def index():
    ok0, out0, err0 = run_cmd(CMD[0])
    ok1, out1, err1 = run_cmd(CMD[1])
    ok2, out2, err2 = run_cmd(CMD[2])
    ok3, out3, err3 = run_cmd(CMD[3])
    ok4, out4, err4 = run_cmd(CMD[4])
    ok5, out5, err5 = run_cmd(CMD[5])

    out3 = out3.decode('utf-8')
    out3 = out3.replace(' PM', 'PM')  # remoce pesky PM
    out3 = out3[out3.find('\n\n') + 2:out3.rfind('\n')]  # ignore first line
    out3 = out3.replace('\n', '</td></tr><tr><td>')
    if out3.endswith('<tr><td>'):
        out3 = out3[:-8]
    out3 = re.sub(r"\s+", '</td><td>', out3)
    tab_mem = '<table class="resultsTable"><tr><td>' + out3 + '</td></tr></table>'

    out4 = out4.decode('utf-8')
    out4 = out4.replace('\n', '</td></tr><tr><td>')
    if out4.endswith('<tr><td>'):
        out4 = out4[:-8]
    tab_gpu = '<table class="resultsTable"><tr><td>' + out4.replace(',', '</td><td>') + '</table>'

    out5 = out5.decode('utf-8')
    out5 = out5[out5.find('Average'):]  # ignore first line
    out5 = out5.replace('\n', '</td></tr><tr><td>')
    if out5.endswith('<tr><td>'):
        out5 = out5[:-8]
    out5 = re.sub(r"\s+", '</td><td>', out5)
    tab_cpu = '<table class="resultsTable"><tr><td>' + out5 + '</table>'

    return render_template('view.html', title='WebStats',
                           ok0=ok0, err0=err0, out0=out0.decode("utf-8").replace('\n', '<br/>'), cmd0=CMD[0],
                           ok1=ok1, err1=err1, out1=out1.decode("utf-8").replace('\n', '<br/>'), cmd1=CMD[1],
                           ok2=ok2, err2=err2, out2=out2.decode("utf-8").replace('\n', '<br/>'), cmd2=CMD[2],
                           ok3=ok3, err3=err3, out3=tab_mem, cmd3=CMD[3],
                           ok4=ok4, err4=err4, out4=tab_gpu, cmd4=CMD[4],
                           ok5=ok5, err5=err5, out5=tab_cpu, cmd5=CMD[5],
                           )


# -----------
if __name__ == "__main__":
    app.run(debug=True)
