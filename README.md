# SvenskaMagic - CSV Converter

This is a quick converter for [SvenskaMagic.com](https://www.svenskamagic.com) a Swedish Magic the Gathering community.

The intent with the script is to quickly be able to convert a CSV file from a different source than SVM into the format SVM expects.

For a "to the point" example check out the [example](https://github.com/Jerakin/svm/tree/master/example/example.py)

There are two main classes in the scrip, `Card` which simply holds a csv row of information and is able to validate it and 

### `SVM(input_tsv, [expand_antal], [header], [converters])`
 This class function is to read the CSV data and put each row into a `Card`, it can then later save into a different CSV file.
 
**PARAMETERS**
* `input_csv` (Pathlike object|string) - The csv/tsv file to convert
* `expand_antal` (bool) - *Default:* `True`, if you want rows with more than 1 cards in it to be added as multiple rows
* `header` (list|set) - *Default:* `converter.DEFAULT_HEADER`, the expected input rows. They need to have the same rows as SVM expects.
* `converters` (list|set) - *Default:* `()`, a list/set of functions to run on the input_csv cells, item at index 0 will be run on index 0 of the row.


### translation.json
SVM differs a bit on how it names some cards and sets, this file is to translate from other common formats into the format that SVM expects.
