from matplotlib import pyplot as plt
import pandas as pd

from lab1 import functions
from lab2.functions import groupby_aggregate, groupby, my_csv_loader


LAST_FIVE_YEARS = ['2016', '2017', '2018', '2019', '2020']
DATASET_PATH = 'datasets/pop_year_trim.csv'


if __name__ == '__main__':
    type_map = {
        '2016': int, '2017': int, '2018': int, '2019': int, '2020': int
    }
    column_names, rows = my_csv_loader(DATASET_PATH, type_map)
    regional_populations_by_year = pd.DataFrame(rows, columns=column_names)
    assert(
        regional_populations_by_year.shape == pd.read_csv(DATASET_PATH).shape
    )
    print(regional_populations_by_year.head())

    # Only show populations with post-secondary education
    college_graduates = regional_populations_by_year[
        regional_populations_by_year['level of education']
        == 'post secondary education'
    ]
    norrbotten_college_graduate_populations = college_graduates[
        college_graduates.region == '25 Norrbotten county'
    ][LAST_FIVE_YEARS].values[0]
    my_mean = functions.mean(norrbotten_college_graduate_populations)
    assert(my_mean == norrbotten_college_graduate_populations.mean())
    print('Mean population with post-secondary education in Norrbotten '
          f'region in the last 5 years: {my_mean:.1f}')

    my_stdev = functions.standard_deviation(
        norrbotten_college_graduate_populations, biased=True
    )
    assert(my_stdev == norrbotten_college_graduate_populations.std())
    print(
        'Standard deviation of the populations with post-secondary education '
        f'in Norrbotten region in the last 5 years: {my_stdev:.1f}'
    )

    # Plot the mean of the regional populations over the last 5 years
    population_sums_by_region = groupby_aggregate(
        groupby(regional_populations_by_year, 'region'),
        cols=LAST_FIVE_YEARS,
        fn_aggregate=functions.my_sum,
        group_column_name='region'
    )
    assert(
            population_sums_by_region.shape ==
            regional_populations_by_year.groupby('region')[
                LAST_FIVE_YEARS
            ].sum().reset_index().shape
    )
    population_sums_by_region['mean population'] = [
        functions.mean(p) for p
        in population_sums_by_region[LAST_FIVE_YEARS].values
    ]
    print(population_sums_by_region.head())
    population_sums_by_region[['region', '2020']].set_index('region').plot.bar()
    plt.show()


