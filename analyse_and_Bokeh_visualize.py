
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, ColorBar
from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap

input_data = pd.read_csv('to_check.csv',  sep=';', decimal=",")
# print(input_data.head())


def select_last_quater(input_data, debug=True):

    if debug:
        print('input_data len', len(input_data))

    last_Q_condition = input_data.loc[:, 'DATA'] > '2018-09-01'
    last_quarter = input_data.loc[last_Q_condition, :]
    last_quarter = last_quarter.reset_index()

    if debug:
        print('fourth_quarter_2018 len', len(fourth_quarter_2019))

    return last_quarter

last_quarter = select_last_quater(input_data, False)


def calculate_value(last_quarter, debug=True):

    # calculate new column - value
    last_quarter.loc[:,'WART'] = last_quarter.loc[:,'CSNJ_B'] * last_quarter.loc[:,'IL']

    if debug:
        print(last_quarter)

    return last_quarter

last_quarter = calculate_value(last_quarter, False)


def change_date_to_rounded_time(last_quarter, _round='30min', debug=True):

    if debug:
        print('fourth_quarter_2019 len', len(last_quarter))

    # change date to datetime
    last_quarter.loc[:,'DATA'] = pd.to_datetime(last_quarter.loc[:,'DATA'])

    # round
    last_quarter.loc[:,'time_rounded_DATA'] = last_quarter.loc[:,'DATA'].dt.round(_round)

    if debug:
        print('rounded_time len', len(last_quarter))

    return last_quarter

last_quarter = change_date_to_rounded_time(last_quarter, debug=False)


def round_hour_and_minute_to_decimal(last_quarter, debug=True):

    # amend to hours and minutes
    last_quarter.loc[:,'hour'] = last_quarter.loc[:,'time_rounded_DATA'].dt.hour.astype(float)
    last_quarter.loc[:,'minute'] = last_quarter.loc[:,'time_rounded_DATA'].dt.minute.astype(float)/60

    # amend hour and minute float to decimal
    last_quarter.loc[:,'time'] = last_quarter.loc[:,'hour'] + last_quarter.loc[:,'minute']

    if debug:
        print(last_quarter)

    return last_quarter

last_quarter = round_hour_and_minute_to_decimal(last_quarter, False)


# print(last_quarter)
last_quarter.to_csv('last_quarter.csv', index = 0)
last_quarter.to_csv('last_quarter_copy.csv', index = 0)


last_quarter = pd.read_csv('last_quarter.csv')
# print(last_quarter)


def gen_weekday_number(last_quarter, debug=False):

    # change to datetime
    last_quarter.loc[:,'DATA'] = pd.to_datetime(last_quarter.loc[:,'DATA'])
    # generate weekday
    last_quarter.loc[:, 'WEEK_DAY'] = last_quarter.loc[:, 'DATA'].dt.weekday

    if debug:
        print(last_quarter)

    return last_quarter

last_quarter = gen_weekday_number(last_quarter, False)


def grouped_sum_bill_values_per_weekday_number(last_quarter, debug=True):

    last_quarter = last_quarter.groupby(['WEEK_DAY', 'RACH_ID'])['WART'].sum()
    last_quarter = last_quarter.reset_index()

    if debug:
        print(last_quarter)

    return last_quarter

last_quarter = grouped_sum_bill_values_per_weekday_number(last_quarter, False)


def filter_values(last_quarter, n=3, debug=True):

    if debug:
        print('WART len', len(last_quarter))

    # count average value
    s = last_quarter.loc[:, 'WART'].mean()
    # multiple average n times
    last_quarter['filtered_value'] = last_quarter['WART'].apply(lambda x: x if (x < n * s) else n * s)

    if debug:
        print('WART len', len(last_quarter))
        print(s)
        print(last_quarter)

    return last_quarter

last_quarter = filter_values(last_quarter, n=3, debug=False)


def round_filetered_bill_value(last_quarter, _mod=2, debug=True):

    if debug:
        print('WART len', len(last_quarter))

    # round values and change to integer
    last_quarter.loc[:,'rounded_filtered_value'] = last_quarter.loc[:,'filtered_value'].round(0).astype(int)

    # modulo round
    last_quarter.loc[:,'rounded_filtered_value_mod'] = last_quarter.loc[:,'rounded_filtered_value'].apply(
        lambda x: x - x % _mod)

    if debug:
        print('rounded_filtered_value_mod len', len(last_quarter))
        print(last_quarter)

    return last_quarter

last_quarter = round_filetered_bill_value(last_quarter, _mod=2, debug=False)


def group_bill_values_per_weekday(last_quarter, debug=True):

    grouped_filtered_value_and_weekday = last_quarter.groupby(['rounded_filtered_value_mod', 'WEEK_DAY']).size()
    grouped_filtered_value_and_weekday = grouped_filtered_value_and_weekday.reset_index()

    grouped_filtered_value_and_weekday.columns = ['RFV', 'WD', 'S']

    grouped_filtered_value_and_weekday = grouped_filtered_value_and_weekday.sort_values(by=['S'], ascending=False)
    grouped_filtered_value_and_weekday = grouped_filtered_value_and_weekday.reset_index()

    if debug:
        print(grouped_filtered_value_and_weekday)

    return grouped_filtered_value_and_weekday

grouped_filtered_value_and_weekday = group_bill_values_per_weekday(last_quarter, False)


last_quarter_copy = pd.read_csv('last_quarter_copy.csv')
# print(last_quarter_copy)


def grouped_sum_bill_values_per_rounded_time(last_quarter_copy, debug=True):

    last_quarter_copy = last_quarter_copy.groupby(['time', 'RACH_ID'])['WART'].sum()
    last_quarter_copy = last_quarter_copy.reset_index()

    if debug:
        print(last_quarter_copy)

    return last_quarter_copy

last_quarter_copy = grouped_sum_bill_values_per_rounded_time(last_quarter_copy, False)


def filter_values(last_quarter_copy, n=3, debug=True):

    if debug:
        print('WART len', len(last_quarter_copy))

    # count average value
    s = last_quarter.loc[:, 'WART'].mean()
    # multiple average n times
    last_quarter_copy['filtered_value'] = last_quarter_copy['WART'].apply(lambda x: x if (x < n * s) else n * s)

    if debug:
        print('WART len', len(last_quarter_copy))
        print(s)
        print(last_quarter_copy)

    return last_quarter_copy

last_quarter_copy = filter_values(last_quarter_copy, n=3, debug=False)


def round_filetered_bill_value(last_quarter_copy, _modu=5, debug=True):

    if debug:
        print('WART len', len(last_quarter_copy))

    # round values and change to integer
    last_quarter_copy.loc[:,'rounded_filtered_value'] = last_quarter_copy.loc[:,'filtered_value'].round(0).astype(int)

    # modulo round
    last_quarter_copy.loc[:,'rounded_filtered_value_mod'] = last_quarter_copy.loc[:,'rounded_filtered_value'].apply(
        lambda x: x - x % _modu)

    if debug:
        print('rounded_filtered_value_mod len', len(last_quarter_copy))
        print(last_quarter_copy)

    return last_quarter_copy

last_quarter_copy = round_filetered_bill_value(last_quarter_copy, _modu=5, debug=False)


def group_bill_values_per_rounded_time(last_quarter_copy, debug=True):

    grouped_filtered_value_and_time = last_quarter_copy.groupby(['rounded_filtered_value_mod', 'time']).size()
    grouped_filtered_value_and_time = grouped_filtered_value_and_time.reset_index()

    grouped_filtered_value_and_time.columns = ['RFV', 'T', 'S']

    grouped_filtered_value_and_time = grouped_filtered_value_and_time.sort_values(by=['S'], ascending=False)
    grouped_filtered_value_and_time = grouped_filtered_value_and_time.reset_index()

    if debug:
        print(grouped_filtered_value_and_time)

    return grouped_filtered_value_and_time

grouped_filtered_value_and_time = group_bill_values_per_rounded_time(last_quarter_copy, False)


output_file("bills per week day.html", title="Sum of bill values / week day 0=Monday, 6=Sunday")

x = grouped_filtered_value_and_weekday.loc[:,'WD']
y = grouped_filtered_value_and_weekday.loc[:,'RFV']
z = grouped_filtered_value_and_weekday.loc[:,'S']

#Use the field name of the column source
mapper = linear_cmap(field_name='z', palette=Spectral6, low=min(z), high=max(z))

source = ColumnDataSource(dict(x=x,y=y,z=z))

p = figure(plot_width=600, plot_height=600, title="Sum of bill values / week day 0=Monday, 6=Sunday")

p.circle(x='x', y='y', line_color=mapper, color=mapper, fill_alpha=1, size=10, source=source)

color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0))

p.add_layout(color_bar, 'right')

show(p)


output_file("bills per hour.html", title="Sum of bill values per hour")

x=grouped_filtered_value_and_time.loc[:,'T']
y=grouped_filtered_value_and_time.loc[:,'RFV']
z=grouped_filtered_value_and_time.loc[:,'S']

#Use the field name of the column source
mapper = linear_cmap(field_name='z', palette=Spectral6, low=min(z), high=max(z))

source = ColumnDataSource(dict(x=x,y=y,z=z))

p = figure(plot_width=600, plot_height=600, title="Sum of bill values per hour")

p.circle(x='x', y='y', line_color=mapper, color=mapper, fill_alpha=1, size=10, source=source)

color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0))

p.add_layout(color_bar, 'right')

show(p)
