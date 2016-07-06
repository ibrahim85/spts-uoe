import pickle

empty_entries = find_zero_periods(readings, 'NbBikes')
empty_periods = group_ellapsed(empty_entries).sort_values(by=['Ellapsed'], ascending=False)
empty_periods_sum = group_ellapsed(empty_periods).groupby('Id').sum().sort_values(by=['Ellapsed'], ascending=False).reset_index()
