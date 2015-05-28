import os
import configparser

config_default = {
    'qt_server': 'https://survey.qualtrics.com/WRAPI/ControlPanel/api.php',
    'db_dbname': 'qted',
    'db_user': 'qted',
    'db_password': 'qted'
    }

def split_name(arg):
    """
    Parse an (optionally) dot-separated configuration variable name into two
    parts and return them as a 2-tuple.  E.g. given 'a.b.c' return
    ('a', 'b.c'), and given 'a' return ('', 'a').
    """
    sp = arg.split('.')
    len_sp = len(sp)
    if len_sp == 0:
        return ['', '']
    elif len_sp == 1:
        return ['', sp[0]]
    elif len_sp == 2:
        return sp
    else: # len_sp > 2
        return (sp[0], '.'.join(sp[1:]))

def set_default_section(name, default):
    """
    Given the 2-tuple name = (K, S), if K = '' then return (K', S) where
    K' = default, otherwise return (K, S).
    """
    if name[0] == '':
        return (default, name[1])
    else:
        return name

def get_config_file_name():
    """
    Return the configuration path/file name in the home directory.
    """
    return os.getenv('HOME', '.') + '/.qted'

def write_config(section, key, value):
    """
    Write a value to the configuration file.
    """
    config_file_name = get_config_file_name()
    config = configparser.ConfigParser()
    config.read(config_file_name)
    if section not in config.sections():
        config[section] = {}
    config[section][key] = value
    with open(config_file_name, 'w') as file:
        config.write(file)

def read_config(section, key):
    """
    Read a value from the configuration file.
    """
    config_file_name = get_config_file_name()
    config = configparser.ConfigParser()
    config.read(config_file_name)
    if section not in config.sections():
        return ''
    value = config[section].get(key)
    return value

def parse_name(name):
    """
    Split the given configuration variable name into two parts, section and
    key, and return them as a 2-tuple, supplying the default section if none
    is given.  E.g. given 'a.b.c' return ('a', 'b.c'), and given 'a' return
    ('qted', 'a').
    """
    pair = split_name(name)
    return set_default_section(pair, 'qted')

def set_config(var, value):
    """
    Set the value of a configuration variable var in the form 'section.key'.
    """
    (section, key) = parse_name(var)
    write_config(section, key, value)

def get_config_default(key):
    """
    Return the default value for a configuration variable, or None if there is
    no default.
    """
    value = config_default.get(key)
    return '' if value is None else value

def get_config(var):
    """
    Get the value of a configuration variable var in the form 'section.key'.
    """
    (section, key) = parse_name(var)
    value = read_config(section, key)
    return get_config_default(key) if value is None else value

if __name__ == '__main__':
    pass

