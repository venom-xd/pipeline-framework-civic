import pandas as pd

class MissingValuesTask:
    def __init__(self, columns, thresholds):
        self.columns = columns
        self.thresholds = thresholds

    def execute(self, df):
        result = {}
        for column in self.columns:
            if column in df.columns:
                missing_percentage = df[column].isnull().mean() * 100
                exceeds_threshold = missing_percentage > self.thresholds.get(column, 0)
                result[column] = {
                    'missing_percentage': missing_percentage,
                    'exceeds_threshold': exceeds_threshold
                }
        return result

class DuplicateRowsTask:
    def __init__(self, subset):
        self.subset = subset

    def execute(self, df):
        duplicate_count = df.duplicated(subset=self.subset).sum()
        return {
            'duplicate_count': duplicate_count,
            'columns_checked': self.subset
        }
