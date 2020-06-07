import os.path
import yaml

import pytest
import writerblocks
import writerblocks.backend
import writerblocks.common
import writerblocks.test.dummy


from typing import Callable, List


@pytest.fixture()
def overwrite_list_dir_fun() -> Callable[[List[str]], None]:
    """For testing things that work off a list of files."""
    def overwrite_listdir(value: List[str]) -> None:
        writerblocks.backend.__list_dir = lambda x: value
    return overwrite_listdir


def __example_path() -> str:
    """Path to the example project."""
    root_path = os.path.dirname(os.path.abspath(writerblocks.__file__))
    return os.path.abspath(os.path.join(root_path, '../example'))


@pytest.fixture(scope='module')
def use_example() -> str:
    """Set base_dir to the example project, return example project path."""
    writerblocks.common.options.base_dir = __example_path()
    return writerblocks.common.options.base_dir


@pytest.fixture(scope='module')
def use_fmt() -> None:
    """Set format to the example project's setup."""
    fmt_file = os.path.join(__example_path(), writerblocks.common.FORMAT_FILENAME)
    with open(fmt_file, 'r') as fmt:
        writerblocks.common.options.fmt = yaml.safe_load(fmt)
