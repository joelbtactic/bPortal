from datetime import datetime, timedelta

def doli_get_calendar_days_in_sql_format(option, days, field_name):
    filter_date = datetime.now()
    today = filter_date.strftime("%Y-%m-%d")

    if option == 'this_month':
        first_month = filter_date.replace(day=1).strftime("%Y-%m-%d")
        second_month = filter_date.replace(day=1, month=filter_date.month+1).strftime("%Y-%m-%d")
        query = f"(t.{field_name}:>:'{first_month}') and (t.{field_name}:<:'{second_month}') and "

    elif option == 'last':
        last_days = filter_date - timedelta(days)
        last_days = last_days.strftime("%Y-%m-%d")
        query = f"(t.{field_name}:>:'{last_days}') and (t.{field_name}:<:'{today}') and "

    elif option == 'last_month':
        first_month = filter_date.replace(day=1, month=filter_date.month-1).strftime("%Y-%m-%d")
        second_month = filter_date.replace(day=1).strftime("%Y-%m-%d")
        query = f"(t.{field_name}:>:'{first_month}') and (t.{field_name}:<:'{second_month}') and "

    elif option == 'next_month':
        first_month = filter_date.replace(day=1, month=filter_date.month+1).strftime("%Y-%m-%d")
        second_month = filter_date.replace(day=1, month=filter_date.month+2).strftime("%Y-%m-%d")
        query = f"(t.{field_name}:>:'{first_month}') and (t.{field_name}:<:'{second_month}') and "

    elif option == 'last_year':
        first_month = filter_date.replace(day=1, month=1, year=filter_date.year-1).strftime("%Y-%m-%d")
        second_month = filter_date.replace(day=1, month=1).strftime("%Y-%m-%d")
        query = f"(t.{field_name}:>:'{first_month}') and (t.{field_name}:<:'{second_month}') and "

    elif option == 'next_year':
        first_month = filter_date.replace(day=1, month=1, year=filter_date.year+1).strftime("%Y-%m-%d")
        second_month = filter_date.replace(day=1, month=1, year=filter_date.year+2).strftime("%Y-%m-%d")
        query = f"(t.{field_name}:>:'{first_month}') and (t.{field_name}:<:'{second_month}') and "

    elif option == 'this_year':
        first_month = filter_date.replace(day=1, month=1, year=filter_date.year).strftime("%Y-%m-%d")
        second_month = filter_date.replace(day=1, month=1, year=filter_date.year+1).strftime("%Y-%m-%d")
        query = f"(t.{field_name}:>:'{first_month}') and (t.{field_name}:<:'{second_month}') and "

    else:
        next_days = filter_date + timedelta(days)
        next_days = next_days.strftime("%Y-%m-%d")
        query = f"(t.{field_name}:>:'{today}') and (t.{field_name}:<:'{next_days}') and "
    return query

def doli_get_datetime_option_in_mysql_format(option, field_name, params=None):
    params = params or []

    if option == '=' and params[0]:
        return f"(t.{field_name}:=:'{params[0]}') and "
    if option == 'not_equal' and params[0]:
        return f"(t.{field_name}:<:'{params[0]}') or (t.{field_name}:>:'{params[0]}') and "
    if option == 'greater_than' and params[0]:
        return f"(t.{field_name}:>:'{params[0]}') and "
    if option == 'less_than' and params[0]:
        return f"(t.{field_name}:<:'{params[0]}') and "
    if option == 'between' and params[0] and params[1]:
        return f"(t.{field_name}:>:'{params[0]}') and (t.{field_name}:<:'{params[1]}') and "
    if option == 'last_7_days':
        return doli_get_calendar_days_in_sql_format("last", 7, field_name)
    if option == 'next_7_days':
        return doli_get_calendar_days_in_sql_format("next", 7, field_name)
    if option == 'last_30_days':
        return doli_get_calendar_days_in_sql_format("last", 30, field_name)
    if option == 'next_30_days':
        return doli_get_calendar_days_in_sql_format("next", 30, field_name)
    if option == 'last_month':
        return doli_get_calendar_days_in_sql_format("last_month", 0, field_name)
    if option == 'this_month':
        return doli_get_calendar_days_in_sql_format("this_month", 0, field_name)
    if option == 'next_month':
        return doli_get_calendar_days_in_sql_format("next_month", 0, field_name)
    if option == 'last_year':
        return doli_get_calendar_days_in_sql_format("last_year", 0, field_name)
    if option == 'this_year':
        return doli_get_calendar_days_in_sql_format("this_year", 0, field_name)
    if option == 'next_year':
         return doli_get_calendar_days_in_sql_format("next_year", 0, field_name)

    return None
