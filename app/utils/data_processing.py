import pandas as pd
import re

def load_and_preprocess_coffee_data(csv_path: str) -> pd.DataFrame:
    """
    - CSV 파일( origin, desc_1, desc_3, roast, agtron )을 로드
    - 텍스트 전처리(소문자화, 불필요한 공백 제거 등)
    """
    df = pd.read_csv(csv_path)

    # 컬럼 존재 여부 확인
    required_columns = ["origin", "desc_1", "desc_3", "roast", "agtron"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"[에러] {col} 컬럼이 CSV에 없습니다.")
    
    # 전처리: 소문자화, 불필요한 특수문자 제거 등
    text_cols = ["origin", "desc_1", "desc_3", "roast", "agtron"]
    for col in text_cols:
        # 소문자 변환
        df[col] = df[col].astype(str).apply(lambda x: x.strip().lower())
        # 필요에 따라 특수문자 제거 (알파벳, 숫자, 일부 기호만 남김)
        df[col] = df[col].apply(lambda x: re.sub(r'[^a-z0-9\s,/:\-\.]+', '', x))

    return df

if __name__ == "__main__":
    coffee_df = load_and_preprocess_coffee_data("../data/coffee_data.csv")
    print(coffee_df.head())
