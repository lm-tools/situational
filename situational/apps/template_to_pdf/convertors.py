import subprocess


class PrinceXML():
    def convert(self, html_string):
        p = subprocess.Popen(['prince', '--media', 'screen', '-'],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.write(bytes(html_string, 'utf-8'))
        p.stdin.close()
        return p.stdout.read()
