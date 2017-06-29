__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'
__date__ = "26/06/2017"
import subprocess
import sys

from gams_add_on_exception import GamsAddOnException


class DomainInfo(object):
    def __init__(self, gdx_file):
        gdx_file = gdx_file.replace('\\', '/')
        self.gdx_file = gdx_file
        self.symbols = dict()
        self.alias = dict()
        if sys.platform in ['linux2', 'darwin']:
            proc = subprocess.Popen(['gdxdump %s Symbols' % gdx_file, ""],
                                    stdout=subprocess.PIPE, shell=True,
                                    stderr=subprocess.STDOUT)
        elif sys.platform in ['win32']:
            proc = subprocess.Popen(['gdxdump', '%s' % gdx_file, 'Symbols', ''],
                                    stdout=subprocess.PIPE, shell=True,
                                    stderr=subprocess.STDOUT)
        else:
            raise GamsAddOnException('ERROR {platform} not handled'.format(platform=sys.platform))
        (out, err) = proc.communicate()
        if 'GDX file not found' in out:
            msg = out.replace('\n', ' ')
            raise IOError(msg)
        for l, line in enumerate(out.split('\n')):
            info = [l for l in line.strip().split(' ') if l is not '']

            if info and info[3] == 'Alias':
                self.alias[info[1]] = info[-1]

        if sys.platform in ['linux2', 'darwin']:
            proc = subprocess.Popen(["gdxdump \"%s\" DomainInfo" % gdx_file, ""], stdout=subprocess.PIPE, shell=True,
                                    stderr=subprocess.STDOUT)
        elif sys.platform in ['win32']:
            proc = subprocess.Popen(['gdxdump', '%s' % gdx_file, 'DomainInfo', ''], stdout=subprocess.PIPE,
                                    shell=True,
                                    stderr=subprocess.STDOUT)
        else:
            raise GamsAddOnException('ERROR {platform} not handled'.format(platform=sys.platform))
        (out, err) = proc.communicate()
        # print out, err
        for l, line in enumerate(out.split('\n')):
            try:
                sets = [s.strip() for s in line[line.index('(') + 1: line.index(')')].split(',')]
            except ValueError:
                sets = None
                pass
            line = [l for l in line.strip().split(' ') if l is not '']
            if line and line[1] in ['Set', 'Par', 'Var', 'Equ']:
                name = line[3].split('(')[0]
                # print name, sets
                self.symbols[name] = (line[1], sets, None)
            elif line and line[1] in ['Alias']:
                name = line[3].split('(')[0]
                sets = None
                self.symbols[name] = (line[1], sets, self.alias[name])
            else:
                # print line
                pass

                # print "program output:", out

    def get_sets(self, symbol):
        if symbol in self.symbols:
            if self.symbols[symbol][0] == "Alias":
                return self.symbols[symbol][2]
            return self.symbols[symbol][1]
        else:
            return None

    def check_alias(self, symbol):
        if self.symbols[symbol][1]:
            return self.symbols[symbol][1]
        else:
            return symbol

    def __str__(self):
        res = '+' + '-' * 60 + '+\n'
        res += '| %-58s |\n' % 'DomainInfo'
        res += '+' + '-' * 60 + '+\n'
        res += '| %-58s |\n' % self.gdx_file
        res += '+' + '-' * 60 + '+\n'
        for symbol in sorted(self.symbols):
            res += '| %-15s' % symbol + ' -> ' + '%-40s|\n' % str(self.symbols[symbol])

        res += '+' + '-' * 60 + '+\n'
        return res
