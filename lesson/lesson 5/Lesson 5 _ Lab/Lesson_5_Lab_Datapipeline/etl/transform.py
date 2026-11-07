"""Bước TRANSFORM — làm sạch dữ liệu bằng pandas.

Mỗi dòng là một phép biến đổi, thay cho vòng for thủ công.
"""
import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch bảng thời tiết dạng city/temp_c.

    - Bỏ dòng thiếu city.
    - Chuẩn hoá city: bỏ khoảng trắng thừa + viết hoa đầu chữ.
    - Thêm cột loaded_at để biết dữ liệu nạp lúc nào.
    """
    df = df.dropna(subset=["city"]).copy()
    df["city"] = df["city"].str.strip().str.title()
    df["loaded_at"] = pd.Timestamp.utcnow()
    return df


def transform_open_meteo(df: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch dữ liệu Open-Meteo dạng time/temp_c."""
    df = df.dropna(subset=["temp_c"]).copy()
    df["time"] = pd.to_datetime(df["time"])
    df["loaded_at"] = pd.Timestamp.utcnow()
    return df
