"""Test backend functionality."""

import pytest

from writerblocks import backend
from writerblocks.test import dummy


@pytest.mark.usefixtures('use_fmt', 'use_example')
@pytest.mark.parametrize('index_filename,expected_output',
                         [('index.yaml', dummy.full_text_i),
                          ('alt_index.yaml', dummy.full_text_a),
                          ])
def test_combine_from_index(index_filename, expected_output):
    index_file = backend.full_path(index_filename)
    output = backend.combine_from_index(index_filename=index_file,
                                        include_tags=False)
    assert output == expected_output


@pytest.mark.usefixtures('use_example')
@pytest.mark.parametrize('filename,expected_tags', [
    (filename, dummy.files_to_tags[filename]) for filename in dummy.files_to_tags
])
def test_extract_tags_from_file(filename, expected_tags):
    filename = backend.full_path(filename)
    tags = backend.extract_tags_from_file(filename=filename)
    assert tags == expected_tags


@pytest.mark.usefixtures('use_example')
@pytest.mark.parametrize('tag,blacklist', [
    (tag, blacklist) for tag in dummy.full_tags for blacklist in (True, False)
])
def test_get_files_tagged_single(tag, blacklist):
    all_files = [backend.full_path(filename) for filename in
                 dummy.files_to_tags.keys()]
    expected_files = [backend.full_path(filename) for filename in
                      dummy.tags_to_files[tag]]
    if not blacklist:
        files = backend.get_files_tagged(filenames=all_files, tags=[tag])
        assert sorted(files) == sorted(expected_files), (
            "Expected files: {} for tag {} but saw {}!".format(files, tag, expected_files))
    else:
        files = backend.get_files_tagged(filenames=all_files, tags=[], blacklist_tags=[tag])
        for filename in expected_files:
            assert filename not in files, (
                "Got file {} with blacklisted tag {}".format(filename, tag))


@pytest.mark.usefixtures('use_example')
@pytest.mark.parametrize('tag', dummy.full_tags)
def test_get_files_tagged_multi(tag):
    all_files = [backend.full_path(filename) for filename in
                 dummy.files_to_tags.keys()]
    all_tagged_files = [backend.full_path(filename) for filename in
                        dummy.tags_to_files[tag]]
    full, partial, non = dummy.get_matchsets(tag=tag)
    full_files = backend.get_files_tagged(filenames=all_files, tags=full + [tag],
                                          match_all=True)
    partial_files = backend.get_files_tagged(filenames=all_files, tags=partial + [tag],
                                             match_all=False)

    if full:
        # Other tags that are found in every file that has this tag.
        assert sorted(full_files) == sorted(all_tagged_files)
    if partial:
        partial_expected = list(set([backend.full_path(filename)
                                     for t in partial + [tag]
                                     for filename in dummy.tags_to_files[t]]))
        assert sorted(partial_files) == sorted(partial_expected)
    if non:
        non_expected = list(set([backend.full_path(filename)
                                 for t in non
                                 for filename in dummy.tags_to_files[t]]))
        assert not any(t in full_files for t in non_expected)


@pytest.mark.usefixtures('use_example')
@pytest.mark.parametrize('filename,candidates', [
    (fname, dummy.all_index_files) for fname in dummy.all_index_files ] + [
    (None, dummy.all_index_files), (None, dummy.best_index_files), (None, dummy.good_index_files)
])
def test_get_index_file_path_positive(overwrite_list_dir_fun, filename, candidates):
    overwrite_list_dir_fun(candidates)
    expected = filename or candidates[0]
    found = backend.get_index_file_path(filename=filename)
    assert found == backend.full_path(expected)


@pytest.mark.usefixtures('use_example')
def test_get_index_file_path_negative(overwrite_list_dir_fun):
    overwrite_list_dir_fun(dummy.bad_index_files)
    with pytest.raises(AssertionError):
        backend.get_index_file_path(filename=None)


@pytest.mark.parametrize('source,expected_type', [
    ('scenes/foo.md', backend.FileInfo),
    (['scenes/foo.md', 'scenes/bar.md'], backend.SectionInfo),
    ({'Something': 'scenes/foo.md'}, backend.FileInfo),
    ({'Something': ['scenes/foo.md', 'scenes/bar.md']}, backend.SectionInfo)
])
def test_smart_info(source, expected_type):
    item = backend.smart_info(source=source)
    assert type(item) == expected_type
