from ypc import tag_utils


def test_tag():
    metadata = tag_utils.get_metadata("Pinback - Loro")
    if not metadata.artist_name == "Pinback":
        raise AssertionError()
    if not metadata.track_name == "Loro":
        raise AssertionError()
    if not metadata.primary_genre_name == "Pop":
        raise AssertionError()


def test_tag_invalid():
    metadata = tag_utils.get_metadata("test metadata invalid")
    if metadata is not None:
        raise AssertionError()
