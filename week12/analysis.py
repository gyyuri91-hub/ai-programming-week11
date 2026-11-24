import pandas as pd


def 정제(df):
    # 1) 점수가 비어있는 행을 삭제한다.
    df = df.dropna(subset=["점수"]).copy()
    print(len(df))

    # 2) 모든 열이 완전히 같은 행은 하나만 남긴다.
    df = df.drop_duplicates()
    print(len(df))

    # 3) 반과 과목의 앞뒤 공백을 제거한다.
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    print(len(df))

    # 4) 점수가 정수이며 0 이상 100 이하인 행만 남긴다.
    numeric_score = pd.to_numeric(df["점수"], errors="coerce")
    valid_score = (
        numeric_score.notna()
        & (numeric_score >= 0)
        & (numeric_score <= 100)
        & (numeric_score % 1 == 0)
    )
    df = df.loc[valid_score].copy()
    print(len(df))

    return df


def 반별평균(df):
    점수 = pd.to_numeric(df["점수"], errors="coerce")
    return df.assign(점수=점수).groupby("반", sort=True)["점수"].mean()


if __name__ == "__main__":
    df = pd.read_csv("scores_2026.csv")
    df = 정제(df)
