import pytest

from load_scores import load_scores


def test_reads_valid_rows_and_skips_header(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text(
        "이름,점수\n"
        " 홍길동 , 88 \n"
        "홍길동,91\n"
        '"Kim, Hana",77\n',
        encoding="utf-8",
    )

    kept, skipped = load_scores(path)

    assert kept == [("홍길동", 88), ("홍길동", 91), ("Kim, Hana", 77)]
    assert skipped == []


def test_skips_blank_lines_without_recording_them(tmp_path):
    path = tmp_path / "blank.csv"
    path.write_text(
        "이름,점수\n"
        "홍길동,88\n"
        "\n"
        "이순신,92\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(path)

    assert kept == [("홍길동", 88), ("이순신", 92)]
    assert skipped == []


def test_records_invalid_rows_with_line_number_original_and_reason(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text(
        "이름,점수\n"
        "열하나\n"
        "열,둘,셋\n"
        ",80\n"
        "이름,\n"
        "이름,결석\n"
        "낮은점수,-1\n"
        "높은점수,101\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, "열하나", "열 개수가 2가 아님"),
        (3, "열,둘,셋", "열 개수가 2가 아님"),
        (4, ",80", "이름이 비어 있음"),
        (5, "이름,", "점수가 비어 있음"),
        (6, "이름,결석", "점수가 정수가 아님"),
        (7, "낮은점수,-1", "점수가 0~100 밖"),
        (8, "높은점수,101", "점수가 0~100 밖"),
    ]


@pytest.mark.parametrize(
    ("score", "expected_kept", "expected_reason"),
    [
        (-1, [], "점수가 0~100 밖"),
        (0, [("홍길동", 0)], None),
        (1, [("홍길동", 1)], None),
        (99, [("홍길동", 99)], None),
        (100, [("홍길동", 100)], None),
        (101, [], "점수가 0~100 밖"),
    ],
)
def test_score_boundaries(tmp_path, score, expected_kept, expected_reason):
    path = tmp_path / "boundary.csv"
    path.write_text(f"이름,점수\n홍길동,{score}\n", encoding="utf-8")

    kept, skipped = load_scores(path)

    assert kept == expected_kept
    if expected_reason is None:
        assert skipped == []
    else:
        assert skipped == [(2, f"홍길동,{score}", expected_reason)]


def test_header_only_file_returns_empty_lists(tmp_path):
    path = tmp_path / "header.csv"
    path.write_text("이름,점수\n", encoding="utf-8")

    assert load_scores(path) == ([], [])


@pytest.mark.parametrize(
    "path_kind",
    ["missing_file", "missing_folder"],
)
def test_missing_file_or_folder_raises_file_not_found_error(tmp_path, path_kind):
    if path_kind == "missing_file":
        path = tmp_path / "missing.csv"
    else:
        path = tmp_path / "missing_folder" / "scores.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(path)