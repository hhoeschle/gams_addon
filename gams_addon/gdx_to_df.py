__author__ = 'Hanspeter Hoeschle <hanspeter.hoeschle@gmail.com>'
__date__ = "26/06/2017"
import subprocess
import sys
from StringIO import StringIO

import pandas as pd

from domain_info import DomainInfo
from gams_add_on_exception import GamsAddOnException


def gdx_to_df(gdx_file, symbol, gams_type='L', domain_info=None, fillna=0.0):
    # Derive domain info
    if domain_info is None:
        domain_info = DomainInfo(gdx_file)
    if symbol not in domain_info.symbols:
        raise GamsAddOnException('"%s" not in Domain of "%s"' % (symbol, gdx_file))
    symbol_type = domain_info.symbols[symbol][0]

    # Sets
    if symbol_type == "Set":
        return __gdx_to_df_set(gdx_file, symbol, domain_info)

    # Parameter
    if symbol_type == "Par":
        return __gdx_to_df_par(gdx_file, symbol, domain_info, fillna)

    # Variable
    if symbol_type == "Var":
        return __gdx_to_df_var(gdx_file, symbol, domain_info, gams_type.upper(), fillna)

    # Equation
    if symbol_type == "Equ":
        return __gdx_to_df_equ(gdx_file, symbol, domain_info, gams_type.upper(), fillna)


def __gdx_to_df_equ(gdx_file, symbol, domain_info, gams_type, fillna):
    sets = domain_info.get_sets(symbol)
    if sets and any([s == "*" for s in sets]):
        print "-" * 80
        print "WARNING: Sets have not been specified for: %s" % symbol
        print "-" * 80
        (out, err) = __call_gdxdump(gdx_file, symbol, gams_type)
        df_in = pd.read_csv(StringIO(out), sep=",")
        if gams_type == "L":
            idx = list(df_in.columns[:-1])
            df_in.set_index(idx, inplace=True)
            df_in.columns = [symbol]
            return df_in
        else:
            idx = list(df_in.columns[:-5])
            df_in.set_index(idx, inplace=True)
            if gams_type == "M":
                df_in[symbol] = df_in["Marginal"]
            elif gams_type == "LO":
                df_in[symbol] = df_in["Lower"]
            elif gams_type == "UP":
                df_in[symbol] = df_in["Upper"]
            elif gams_type == "SCALE":
                df_in[symbol] = df_in["Scale"]
            else:
                raise GamsAddOnException("gams_type %s not defined" % gams_type)
            return pd.DataFrame(df_in[symbol])
    else:
        set_names = []
        set_index = []

        if sets:
            for s in sets:
                ss = s
                while ss in set_names:
                    ss = ss + s[-1]
                set_names.append(ss)
                if s != "*":
                    idx = __gdx_to_df_set(gdx_file, s, domain_info)
                    idx = idx[idx[s]].index
                else:
                    idx = [0]
                set_index.append(list(idx))
                df = pd.DataFrame(index=pd.MultiIndex.from_product(set_index))
                df.index.names = set_names
        else:
            return __gdx_to_df_scalar(gdx_file, symbol, gams_type)

        df[symbol] = fillna

        (out, err) = __call_gdxdump(gdx_file, symbol, gams_type)
        df_in = pd.read_csv(StringIO(out), sep=",")
        if gams_type == "L":
            df_in.columns = df.index.names + [symbol]
        else:
            exit()

        df[symbol] = df_in[symbol]
        return df.fillna(fillna)


def __gdx_to_df_var(gdx_file, symbol, domain_info, gams_type, fillna):
    sets = domain_info.get_sets(symbol)
    if sets is None:
        return __gdx_to_df_scalar(gdx_file, symbol, gams_type=gams_type, fillna=fillna)

    set_names = []
    set_index = []

    for s in sets:
        ss = s
        while ss in set_names:
            ss = ss + s[-1]
        set_names.append(ss)
        idx = __gdx_to_df_set(gdx_file, s, domain_info)
        idx = idx[idx[s]].index
        set_index.append(list(idx))
    df = pd.DataFrame(index=pd.MultiIndex.from_product(set_index))
    df.index.names = set_names
    df[symbol] = fillna

    (out, err) = __call_gdxdump(gdx_file, symbol, gams_type)
    df_in = pd.read_csv(StringIO(out), sep=",")
    if gams_type == "L":
        index = list(df_in.columns[:-1])
        df_in.set_index(index, inplace=True)
        df[symbol] = df_in["Val"]
    else:
        index = list(df_in.columns[:-5])
        df_in.set_index(index, inplace=True)
        if gams_type == "M":
            df[symbol] = df_in["Marginal"]
        elif gams_type == "LO":
            df[symbol] = df_in["Lower"]
        elif gams_type == "UP":
            df[symbol] = df_in["Upper"]
        elif gams_type == "SCALE":
            df[symbol] = df_in["Scale"]
        else:
            raise GamsAddOnException("gams_type %s not defined" % gams_type)

    return df.fillna(fillna)


def __gdx_to_df_par(gdx_file, symbol, domain_info, fillna):
    sets = domain_info.get_sets(symbol)
    if sets is None:
        return __gdx_to_df_scalar(gdx_file, symbol)

    set_names = []
    set_index = []

    for s in sets:
        ss = s
        while ss in set_names:
            ss = ss + s[-1]
        set_names.append(ss)
        idx = __gdx_to_df_set(gdx_file, s, domain_info)
        idx = idx[idx[s]].index
        set_index.append(list(idx))

    df = pd.DataFrame(index=pd.MultiIndex.from_product(set_index))
    df.index.names = set_names
    df[symbol] = fillna

    (out, err) = __call_gdxdump(gdx_file, symbol)
    df_in = pd.read_csv(StringIO(out), sep=",")

    index = list(df_in.columns[:-1])
    df_in.set_index(index, inplace=True)

    df[symbol] = df_in["Val"]
    df.fillna(fillna, inplace=True)
    return df


def __gdx_to_df_scalar(gdx_file, symbol, gams_type="L", fillna=0.0):
    (out, err) = __call_gdxdump(gdx_file, symbol, gams_type)
    df = pd.read_csv(StringIO(out), sep=",")
    if gams_type == "L":
        return float(df.loc[0, "Val"])
    elif gams_type == "M":
        return float(df.loc[0, "Marginal"])
    elif gams_type == "LO":
        return float(df.loc[0, "Lower"])
    elif gams_type == "UP":
        return float(df.loc[0, "Upper"])
    elif gams_type == "SCALE":
        return float(df.loc[0, "Scale"])
    else:
        raise GamsAddOnException("gams_type %s not defined" % gams_type)


def __gdx_to_df_set(gdx_file, symbol, domain_info):
    sets = domain_info.get_sets(symbol)

    # Set with a undefined set, also 1-dimensional sets
    if any([s == "*" for s in sets]):
        (out, err) = __call_gdxdump(gdx_file, symbol)
        df = pd.read_csv(StringIO(out), sep=",", index_col=range(len(sets)))
        df[symbol] = True
        if len(sets) == 1:
            df.index.names = [symbol]
        return df

    elif sets != ["*"] and [symbol] != sets:
        set_names = sets
        set_index = []
        for s in sets:
            set_index.append(list(__gdx_to_df_set(gdx_file, s, domain_info).index))

        df = pd.DataFrame(index=pd.MultiIndex.from_product(set_index))
        df.index.names = set_names
        (out, err) = __call_gdxdump(gdx_file, symbol)
        df_in = pd.read_csv(StringIO(out), sep=",")
        df_in[symbol] = True
        index = list(df_in.columns[:-1])
        df_in.set_index(index, inplace=True)
        df = pd.merge(df, df_in, how="left", left_index=True, right_index=True).fillna(False)
        df.index.names = set_names
        return df


    else:
        raise GamsAddOnException("Check handling of sets %s", sets)


def __call_gdxdump(gdx_file, symbol, gams_type="L"):
    if gams_type == "L":
        if sys.platform in ['linux2', 'darwin']:
            proc = subprocess.Popen(
                ['gdxdump %s Symb=%s Format=csv Delim=comma FilterDef=N EpsOut=0.0' % (gdx_file, symbol), ""],
                stdout=subprocess.PIPE, shell=True,
                stderr=subprocess.STDOUT)
        elif sys.platform in ['win32']:
            proc = subprocess.Popen(
                ['gdxdump', '%s' % gdx_file, 'Symb=%s' % symbol, 'FilterDef=N', 'Format=csv', 'Delim=comma',
                 'EpsOut=0.0'],
                stdout=subprocess.PIPE, shell=True,
                stderr=subprocess.STDOUT)
        else:
            raise GamsAddOnException('ERROR {platform} not handled'.format(platform=sys.platform))
    else:
        if sys.platform in ['linux2', 'darwin']:
            proc = subprocess.Popen(
                ['gdxdump %s Symb=%s Format=csv Delim=comma FilterDef=N EpsOut=0.0' % (gdx_file, symbol), ""],
                stdout=subprocess.PIPE, shell=True,
                stderr=subprocess.STDOUT)
        elif sys.platform in ['win32']:
            cmd = ['gdxdump', '%s' % gdx_file, 'Symb=%s' % symbol, 'FilterDef=N', 'Format=csv', 'Delim=comma',
                   'CSVAllFields', 'EpsOut=0.0']
            proc = subprocess.Popen(cmd,
                                    stdout=subprocess.PIPE, shell=True,
                                    stderr=subprocess.STDOUT)
        else:
            raise GamsAddOnException('ERROR {platform} not handled'.format(platform=sys.platform))
    return proc.communicate()
