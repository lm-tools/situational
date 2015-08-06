from subprocess import *


class PrinceXML():
    def convert(self, html_string):
        p = Popen(["prince", "-"], stdin=PIPE, stdout=PIPE)
        p.stdin.write(bytes(html_string, 'utf-8'))
        p.stdin.close()
        return p.stdout.read()
