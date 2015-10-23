__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'
import sys
import re
import subprocess
import csv
from collections import OrderedDict

from pandas import DataFrame, MultiIndex

from domain_info import DomainInfo
from gams_add_on_exception import GamsAddOnException


def gdx_to_df(gdx_file, name, type='L', domain_info=None):
    def __get_set(gdx_file, set_name):
        if sys.platform in ['linux2', 'darwin']:
            proc = subprocess.Popen(['gdxdump %s Symb=%s Format=csv NoHeader' % (gdx_file, set_name), ""],
                                    stdout=subprocess.PIPE, shell=True,
                                    stderr=subprocess.STDOUT)
        elif sys.platform in ['win32']:
            proc = subprocess.Popen(['gdxdump', '%s' % gdx_file, 'Symb=%s' % set_name, 'Format=csv', 'NoHeader', ''],
                                    stdout=subprocess.PIPE, shell=True,
                                    stderr=subprocess.STDOUT)
        else:
            raise GamsAddOnException('ERROR {platform} not handled'.format(platform=sys.platform))
        (out, err) = proc.communicate()
        try:
            csv_in = csv.reader(out.split('\n'), delimiter=',')
            return [int(row[0]) for row in csv_in if row]
        except ValueError:
            csv_in = csv.reader(out.split('\n'), delimiter=',')
            return [row[0] for row in csv_in if row]

    def __int(v):
        try:
            return int(v)
        except ValueError:
            return v

    def __float(v):
        try:
            return float(v)
        except ValueError:
            return v

    if domain_info is None:
        domain_info = DomainInfo(gdx_file)
    if name not in domain_info.symbols:
        raise GamsAddOnException('"%s" not in Domain of "%s"' % (name, gdx_file))

    sets = domain_info.get_sets(name)
    index = OrderedDict()
    if sets is None:
        index['Idx'] = [1]
        sets = ['Idx']
    else:
        for s in sets:
            if s in domain_info.symbols:
                set_values = __get_set(gdx_file, s)
                set_name = s
                while set_name in index.keys():
                    set_name = set_name + s
                index[set_name] = set_values
            elif s == '*':
                index[s] = ['---PLACEHOLDER---']
            else:
                raise GamsAddOnException('Set "%s" of "%s" not in Domain of "%s"' % (s, name, gdx_file))

    # print index.values()+[['l', 'm']]

    if domain_info.symbols[name][0] in ['Var', 'Equ']:
        multi_index = MultiIndex.from_product([index[s] for s in sets] + [['L', 'M', 'LO', 'UP', 'SCALE']])
        # print multi_index
        df = DataFrame(0, index=multi_index, columns=[name])
        df.index.names = index.keys() + ['Type']
    else:
        multi_index = MultiIndex.from_product([index[s] for s in index.keys()])
        df = DataFrame(0, index=multi_index, columns=[name])
        df.index.names = index.keys()
    if sys.platform in ['linux2', 'darwin']:
        proc = subprocess.Popen(['gdxdump %s Symb=%s FilterDef=N' % (gdx_file, name), ""],
                                stdout=subprocess.PIPE, shell=True,
                                stderr=subprocess.STDOUT)
    elif sys.platform in ['win32']:
        proc = subprocess.Popen(['gdxdump', '%s' % gdx_file, 'Symb=%s' % name, 'FilterDef=N', ''],
                                stdout=subprocess.PIPE, shell=True,
                                stderr=subprocess.STDOUT)
    else:
        raise GamsAddOnException('ERROR {platform} not handled'.format(platform=sys.platform))
    (out, err) = proc.communicate()
    out = out.replace('\n', '')
    content = re.search(r'/.*/', out).group(0)[1:-1].replace('\'', '').strip().split(',')

    if err:
        raise GamsAddOnException('ERROR: {err}'.format(err=err))
    elif content is []:
        raise GamsAddOnException('ERROR: No content found for {name}'.format(name=name))
    else:
        indices = []
        values = []
        if domain_info.symbols[name][0] in ['Set']:
            df[name] = False
            for data in content:
                if '.' in data:
                    indices.append(tuple([__int(d) for d in data.strip().split('.')]))
                else:
                    indices.append(__int(data.strip()))
                values.append(True)
        else:
            for data in content:
                data = data.strip().split(' ')
                if len(data) == 1:
                    indices.append(1)
                    values.append(__float(data[0]))
                else:
                    index = data[0]
                    if '.' in index:
                        index = tuple([__int(i) for i in index.split('.')])
                        indices.append(index)
                    else:
                        indices.append(__int(index))
                    values.append(__float(data[1]))
        try:
            # print 'NAME:', name, indices, values, len(values), df
            if len(values) == 1 and values[0] == '':
                return df
            else:
                # df.loc[indices, name] = values
                # print df.index
                df.loc[indices, name] = values
                # for i,idx in enumerate(indices):
                #     df.loc[idx, name] = values[i]
        except KeyError as ke:
            print 'Warning', ke
            if '*' in df.index.names:
                for i, idx in enumerate(indices):
                    df.loc[idx, name] = True
                df.drop('---PLACEHOLDER---', inplace=True)

        if type is not None and 'Type' in df.index.names:
            # print type
            # print df.head()
            return df.query('Type == "%s"' % type)
        else:
            return df
