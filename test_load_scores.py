import pytest
from load_scores import load_scores

# 정상 ① (작성 완료)
def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5

# 정상 ②: 빈 줄 건너뛰기
def test_빈_줄은_건너뛴다(tmp_path):
    p = tmp_path / "blank.csv"
    p.write_text("이름,점수\n김하나,88\n\n이둘,92\n", encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert len(kept) == 2

# 정상 ③: 이름에 쉼표 포함 (따옴표 처리 등 명세에 맞게 기대값 확인)
def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    p = tmp_path / "comma.csv"
    p.write_text('이름,점수\n"Kim, Hana",88\n', encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert len(kept) == 1

# 예외 ①: 없는 파일 → FileNotFoundError 발생 확인
def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")

# 예외 ②: 헤더만 있는 빈 파일 → 빈 리스트 반환 확인
def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []

# 경계 ①~③: 0점·100점은 통과, -1점·101점은 제외
@pytest.mark.parametrize("점수, 유효한가", [
    (-1,  False),
    (0,   True),
    (1,   True),
    (99,  True),
    (100, True),
    (101, False),
])
def test_점수_경계값(tmp_path, 점수, 유효한가):
    p = tmp_path / "temp.csv"
    p.write_text(f"이름,점수\n홍길동,{점수}\n", encoding="utf-8")
    kept, skipped = load_scores(str(p))
    assert (len(kept) == 1) == 유효한가