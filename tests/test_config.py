# -*- coding: utf-8 -*-

"""
Test for: config
"""


from nose.tools import raises, eq_, ok_, assert_raises
from m2bk import config
import yaml, os


def_config = {
    'test': 'hello',
    'moonwatcher': 'Oh my god!. It\'s full of stars!'
}


def setup():
    config.clear()


def test_default_cfg():
    # Test set_default_cfg with valid dict
    config.set_default(def_config)
    eq_(def_config, config.get_config(),
        msg="def_config should be equal to the dict returned by "
            "config.get_config")


@raises(TypeError)
def test_default_cfg_nondict():
    # Test set_default_cfg with other types of variables
    config.set_default("No!, I am your father!")


def test_set_get_entry():
    # Test whether set_entry is working well
    config.set_entry('x', 'y')
    eq_(config.get_entry('x'), 'y',
        msg="Value under entry 'x' should have a value of 'y'")
    config.set_entry('x', 'w')
    eq_(config.get_entry('x'), 'w',
        msg="'x' does not have expected value after modifying it")


@raises(KeyError)
def test_set_entry_key():
    # Test set_entry with invalid key (not string)
    config.set_entry(1, 4)


def test_get_entry_key():
    assert_raises(TypeError, config.get_entry, 1)
    assert_raises(KeyError,config.get_entry, 'i_do_not_exist')


def test_list_merge():
    # Test _list_merge
    dst = def_config
    src = {'beatles': ['paul', 'john', 'ringo', 'george']}
    # we put the fab four into the party
    config._list_merge(src, dst)
    eq_(dst['beatles'], src['beatles'])
    # we add yoko
    src['beatles'].append('yoko')
    config._list_merge(src, dst)
    ok_('yoko' in dst['beatles'])
    # ---
    # src could have a key whose value is a list
    # and does not yet exist on dest
    src['boom'] = {}
    config._list_merge(src, dst)
    ok_('boom' in dst)


@raises(FileNotFoundError)
def test_nonexistent_file():
    # Test set_from_file with non-existent file
    config.set_from_file("thisisnothere.txt")


#@raises(ValueError)
@raises(yaml.reader.ReaderError)
def test_set_from_file_bin():
    # Test set_from_file with binary file
    file_name = '/tmp/random.bin'
    with open(file_name, 'wb') as bf:
        for b in range(0, 99):
            bf.write(bytes(b))
    config.set_from_file(file_name)


@raises(TypeError)
def test_set_from_file_nonstr():
    config.set_from_file(45)


def test_set_from_file():
    # Test set_from_file with valid json file
    file_name = '/tmp/thisisnothere.yaml'
    with open(file_name, 'w') as file:
        yaml.dump(def_config, file)
    config.set_from_file(file_name)
    eq_(config.get_config(), def_config)
