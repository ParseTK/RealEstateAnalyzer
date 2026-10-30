# Tyler Kirchner
# Assignment: Real Estate and Files
# I struggle with getting started and how I wanted to approach the assignment. I wanted to make sure I understood what you were looking for in this assignment
# I decided to use basic file operations (this way I was getting the raw csv and getting full control over how I wanted to work with the csv file)
# I used four dictionaries.
# I learned more about loading vs streaming and a bunch about different modules and packages (before starting this assignment I went into a rabbit hole(a good one))
# I hope it's okay I got more stats on the properties by type, zip and city.

from pathlib import Path


def get_data_input(file: Path) -> list[str]:
    """Takes in a path object as a parameter, initializes an empty list, opens the file with read access, skips header,
    loops through each line, appends the line as a string to the previously initialized list, and returns the list.
    :param file: Path object
    :return: list[str]
    """
    l_records_tk: list[str] = []
    with file.open('r') as f:
        next(f)
        for record in f:
            l_records_tk.append(record.strip())
    return l_records_tk


def get_columns(record: str) -> tuple[str, str, str, float] | float:
    """takes in a record of type string, splits each record at each comma and assigns as a list of strings. assigns
    each field by column index, returns the tuple, and switch for price return only.
    :param record: string
    :return: tuple[str, str, str, float] or float"""
    l_columns_tk: list[str] = record.split(',')

    s_city_tk: str = l_columns_tk[1].strip()
    s_property_type_tk: str = l_columns_tk[7].strip()
    s_zip_code_tk: str = l_columns_tk[2].strip()
    f_price_tk: float = float(l_columns_tk[8])

    if not s_city_tk or not s_property_type_tk or not s_zip_code_tk:
        raise ValueError("Missing Fields")


    return s_city_tk, s_property_type_tk, s_zip_code_tk, f_price_tk


def get_prices(records: list[str]) -> tuple[
                                            dict[str, list[float]],
                                            dict[str, list[float]],
                                            dict[str, list[float]],
                                            list[float]]:
    """Receives records, initializes three dictionaries and a list,assigns each element to
    match the sequential index from the split_columns() tuple (tuple unpacking). if the city, property_type, or zip does not exist
    initialize a new list return it, and append the price, otherwise get the list and append the price, catches valueError and skips bad record
    then returns the three dictionaries and a list as a tuple.
    :param records: list[str]
    :return: tuple[dict[str, list[float]], dict[str, list[float]], dict[str, list[float]], list[float]]"""

    d_city_prices_tk: dict[str, list[float]] = {}
    d_prop_prices_tk: dict[str, list[float]] = {}
    d_zip_prices_tk: dict[str, list[float]] = {}
    l_all_prices_tk: list[float] = []

    for record in records:
        s_city_tk, s_property_type_tk, s_zip_code_tk, f_price_tk = get_columns(record)
        d_city_prices_tk.setdefault(s_city_tk, []).append(f_price_tk)
        d_prop_prices_tk.setdefault(s_property_type_tk, []).append(f_price_tk)
        d_zip_prices_tk.setdefault(s_zip_code_tk, []).append(f_price_tk)
        l_all_prices_tk.append(f_price_tk)

    return d_city_prices_tk, d_prop_prices_tk, d_zip_prices_tk, l_all_prices_tk


def get_median(sorted_prices: list[float]) -> float:
    """Takes in a sorted list as a parameter and returns the median, raises valueError if the list is empty.
    :param sorted_prices: list[float]
    :return: float"""

    if not sorted_prices:
        raise ValueError('No prices')

    i_temp_tk: int = len(sorted_prices)
    i_middle_num_tk: int = i_temp_tk // 2

    if i_temp_tk % 2 == 0:
        return (sorted_prices[i_middle_num_tk - 1] + sorted_prices[i_middle_num_tk]) / 2
    return sorted_prices[i_middle_num_tk]


def get_summary(prices: list[float]) -> tuple[float, float, float, float, float]:
    """returns the min, max, total, average, and median of list of prices
    :param prices: list
    :return: tuple[float, float, float, float, float]"""
    if not prices:
        raise ValueError('Empty price list')

    l_sort_price_tk: list[float] = sorted(prices)

    f_min_price_tk: float = l_sort_price_tk[0]
    f_max_price_tk: float = l_sort_price_tk[-1]
    f_total_tk: float = sum(l_sort_price_tk)
    f_average_tk: float = f_total_tk / len(l_sort_price_tk)
    f_median_tk: float = get_median(l_sort_price_tk)

    return f_min_price_tk, f_max_price_tk, f_total_tk, f_average_tk, f_median_tk


# I should split responsibility here
def print_summary(header: str, data: dict[str, list[float]], prefix: str = "") -> None:
    """Prints the summary of formatted prices, k represents a group name, loops through the sorted dictionary assigns
    each value as a list of float price
    :param header: header of the data
    :param data:  dictionary mapping group name to lists of prices
    :param prefix: prefix of the data
    :return: None"""
    print(f"\n=== {header} ===")
    for k in sorted(data):
        l_prices_tk: list[float] = data[k]
        if not l_prices_tk:
            continue

        f_min_price_tk, f_max_price_tk, f_total_tk, f_average_tk, f_median_tk = get_summary(l_prices_tk)
        s_label_tk: str = f"{prefix}{k}"

        print(f"{s_label_tk}")
        print(f"{'Min:':<15} {f_min_price_tk:15,.2f}")
        print(f"{'Max:':<15} {f_max_price_tk:15,.2f}")
        print(f"{'Average:':<15} {f_average_tk:15,.2f}")
        print(f"{'Median:':<15} {f_median_tk:15,.2f}")
        print(f"{'Total:':<15} {f_total_tk:15,.2f}\n")


def show_menu() -> None:
    """Prints the menu
    :return: None"""
    print("\t=== Menu ===")
    print("1. Show City Summary")
    print("2. Show Property Summary")
    print("3. Show Zip Summary")
    print("4. Show Overall Summary")
    print("5. Exit")


def get_menu_choice() -> str:
    """Loops for valid input then returns users choice
    :return: str"""
    while True:
        s_choice_tk: str = input("Choose an option [1-5]\n").strip()
        if s_choice_tk in {"1", "2", "3", "4", "5"}:
            return s_choice_tk
        print("Invalid choice")


def main() -> None:
    """Entry point
    :return: None"""
    p_file_tk: Path = Path("RealEstateData.csv")

    try:
        records: list[str] = get_data_input(p_file_tk)
        if not records:
            raise ValueError("No records provided")

        d_city_prices_tk, d_prop_prices_tk, d_zip_prices_tk, l_all_prices_tk = get_prices(records)
        if not d_city_prices_tk and not d_prop_prices_tk and not d_zip_prices_tk:
            raise ValueError("No data provided")

    except FileNotFoundError:
        print("File not found")
        return
    except PermissionError:
        print("Permission denied")
        return
    except Exception as e:
        print(e)
        return

    while True:
        show_menu()
        s_choice_tk: str = get_menu_choice()

        if s_choice_tk == "1":
            print_summary("Price by city", d_city_prices_tk, prefix="City: ")
        elif s_choice_tk == "2":
            print_summary("Price by property type", d_prop_prices_tk, prefix="Property Type: ")
        elif s_choice_tk == "3":
            print_summary("Price by zip", d_zip_prices_tk, prefix="Zip: ")
        elif s_choice_tk == "4":
            print_summary("Overall Summary", {"City, Property Type, Zip": l_all_prices_tk}, prefix="Stats for: ")
        elif s_choice_tk == "5":
            return



if __name__ == '__main__':
    main()