from ypc import tag_utils


def test_tag():
    # first method : string matching
    metadata = tag_utils.get_metadata("Pinback - Loro")
    if not metadata.artist_name == "Pinback":
        raise AssertionError()
    if not metadata.track_name == "Loro":
        raise AssertionError()

    # second method : itunes search
    metadata = tag_utils.get_metadata("radiohead in limbo")
    print(metadata)
    if not metadata.artist_name == "Radiohead":
        raise AssertionError()
    if not metadata.track_name == "In Limbo":
        raise AssertionError()


def test_tag_invalid():
    metadata = tag_utils.get_metadata("test metadata invalid")
    if metadata is not None:
        raise AssertionError()
