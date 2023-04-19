import pytest
from transaction import Transaction


# Start pytest method: execute command "pytest current file path"
@pytest.fixture
def transaction():
    # Use in-memory database for testing
    return Transaction(":memory:")


def test_create_transaction(transaction):
    transaction.create_transaction("Project A", 100, "Category A", "2022-01-01", "Description A")
    assert transaction.read_transaction(1) == (1, "Project A", 100, "Category A", "2022-01-01", "Description A")


def test_read_transaction(transaction):
    # Need to create new data for each test of a new method
    transaction.create_transaction("Project A", 100, "Category A", "2022-01-01", "Description A")
    assert transaction.read_transaction(1) == (1, "Project A", 100, "Category A", "2022-01-01", "Description A")


def test_read_all_transactions(transaction):
    transaction.create_transaction("Project A", 100, "Category A", "2022-01-01", "Description A")
    transaction.create_transaction("Project B", 200, "Category B", "2022-01-02", "Description B")
    assert transaction.read_all_transactions() == \
           [(1, "Project A", 100, "Category A", "2022-01-01", "Description A"),
            (2, "Project B", 200, "Category B", "2022-01-02", "Description B")]


def test_update_transaction(transaction):
    transaction.create_transaction("Project A", 100, "Category A", "2022-01-01", "Description A")
    transaction.update_transaction(1, item="Project B", amount=200)
    assert transaction.read_transaction(1) == (1, "Project B", 200, "Category A", "2022-01-01", "Description A")


def test_delete_transaction(transaction):
    transaction.create_transaction("Project A", 100, "Category A", "2022-01-01", "Description A")
    transaction.delete_transaction(1)
    assert transaction.read_transaction(1) == None


def test_aggregate_by_category(transaction):
    transaction.create_transaction("Project A", 100, "Category A", "2022-01-01", "Description A")
    transaction.create_transaction("Project B", 200, "Category A", "2022-01-02", "Description B")
    transaction.create_transaction("Project C", 300, "Category B", "2022-01-03", "Description C")
    assert transaction.aggregate_by_category() == [("Category A", 300), ("Category B", 300)]


def test_aggregate_by_date(transaction):
    transaction.create_transaction("Project A", 100, "Category A", "2022-01-01", "Description A")
    transaction.create_transaction("Project B", 200, "Category A", "2022-01-02", "Description B")
    transaction.create_transaction("Project C", 300, "Category B", "2022-01-03", "Description C")
    assert transaction.aggregate_by_date() == [("2022-01-01", 100), ("2022-01-02", 200), ("2022-01-03", 300)]


def test_aggregate_by_month(transaction):
    transaction.create_transaction("Project A", 100, "Category A", "2022-01-01", "Description A")
    transaction.create_transaction("Project B", 200, "Category A", "2022-02-02", "Description B")
    transaction.create_transaction("Project C", 300, "Category B", "2022-03-03", "Description C")
    assert transaction.aggregate_by_month() == [("2022-01", 100), ("2022-02", 200), ("2022-03", 300)]


def test_aggregate_by_year(transaction):
    transaction.create_transaction("Project A", 100, "Category A", "2022-01-01", "Description A")
    transaction.create_transaction("Project B", 200, "Category A", "2023-02-02", "Description B")
    transaction.create_transaction("Project C", 300, "Category B", "2024-03-03", "Description C")
    assert transaction.aggregate_by_year() == [("2022", 100), ("2023", 200), ("2024", 300)]
