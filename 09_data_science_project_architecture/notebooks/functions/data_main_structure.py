def column_mapping(data):
    """
    column_mapping is a function that receives a DataFrame and returns a dictionary
    mapping each column index to its column name.

    :param data: pandas DataFrame
    :return: dictionary in the format {index: column_name}
    """
    idx_col = {}
    for idx, col in enumerate(data.columns):
        idx_col[idx] = col

    return idx_col


def get_columns(data, *args: int):
    """
    get_columns is a function that returns a new DataFrame with the selected columns.

    If you don't know the column indexes, you can use the `column_mapping` function
    to view all columns and their corresponding indexes.

    :param data: pandas DataFrame
    :param args: column indexes to select (variable number of arguments)
    :return: DataFrame containing only the selected columns
    """
    df = data.iloc[:, list(args)]

    return df
