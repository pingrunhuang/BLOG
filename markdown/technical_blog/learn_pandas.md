## dataframe.sum()
by default, sum up each cell's value by each column. Specify the `axis` attribute will to change the sum up rule. `0` means by columns, `1` means by rows.

## check if the dataframe has null value
`df.isnull().sum().sum()` will sum up all the true value for each column and then each row.

## replace a certain value with other value
`df['column name'].map({'yes':1, 'no':0})`
