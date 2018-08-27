
# Import Libraries
from matplotlib import pyplot
from pandas import Series
from sklearn.model_selection import TimeSeriesSplit


def method_multipleSplits(num_splits, file_name):
    series = Series.from_csv(file_name, header=0)
    data = series.values
    splits = TimeSeriesSplit(n_splits=num_splits)
    pyplot.figure(1)
    index = 1
    for train_index, test_index in splits.split(data):
        train = data[train_index]
        test = data[test_index]
        print("Training observations: {}".format(len(train)))
        print("Testing observations: {}".format(len(test)))
        print("Total observations: {}\n".format(len(train) + len(test)))
        pyplot.subplot((num_splits * 100) + 10 + index)
        pyplot.plot(train)
        pyplot.plot([None for i in train] + [x for x in test])
        index += 1
