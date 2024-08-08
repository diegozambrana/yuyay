def get_values_list_pages(total_stargazers, iterations = 15):
    """
    This function returns a list of values to be used in the pagination of the stargazers history.
    total_stargazers: int
    iterations: int (default 10)
    """
    if total_stargazers > 40000:
        result = [1]
        value = 1333 / iterations
        for i in range(1, iterations + 1):
            result.append(int(i * value))
        return result
    else:
        result =  [1]
        value = (total_stargazers // 30) / iterations
        for i in range(1, iterations + 1):
            result.append(int(i * value))
        return result