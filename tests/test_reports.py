import pandas as pd
from src.reports import spending_by_category


def test_spending_by_category_correct_data(sample_transactions):
    result = spending_by_category(sample_transactions, "Еда", "2023-09-30")
    assert not result.empty
    assert len(result) == 2


def test_spending_by_category_empty_dataframe():
    empty_df = pd.DataFrame()
    result = spending_by_category(empty_df, "Еда")
    assert result["error"].iloc[0] == "Переданный DataFrame пуст"


def test_spending_by_category_missing_date_column():
    data = {"Категория": ["Еда"], "Сумма": [100]}
    df = pd.DataFrame(data)
    result = spending_by_category(df, "Еда")
    assert result["error"].iloc[0] == "Отсутствует столбец 'Дата операции'"


def test_spending_by_category_invalid_dates():
    data = {
        "Дата операции": ["2023-09-01", "invalid-date", "2023-08-15"],
        "Категория": ["Еда", "Транспорт", "Еда"],
        "Сумма": [100, 200, 150],
    }
    df = pd.DataFrame(data)
    result = spending_by_category(df, "Еда", "2023-09-30")
    assert not result.empty
    assert len(result) == 2


def test_spending_by_category_no_data_for_category(sample_transactions):
    result = spending_by_category(sample_transactions, "Кино", "2023-09-30")
    assert result.empty


def test_spending_by_category_invalid_category(sample_transactions):
    result = spending_by_category(sample_transactions, "Несуществующая категория", "2023-09-30")
    assert result.empty


def test_spending_by_category_boundary_dates(sample_transactions):
    result = spending_by_category(sample_transactions, "Еда", "2023-07-10")
    assert not result.empty
    assert len(result) == 2


def test_spending_by_category_empty_results_after_filtering(sample_transactions):
    result = spending_by_category(sample_transactions, "Еда", "2023-04-01")
    assert result.empty
