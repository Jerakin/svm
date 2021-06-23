# SvenskaMagic - CSV Converter

This is a converter for [SvenskaMagic.com](https://www.svenskamagic.com) a Swedish Magic the Gathering community.

The intent with the script is to quickly be able to convert a CSV file from a different source than SVM into the format SVM expects.

For a "to the point" example check out the [example](https://github.com/Jerakin/svm/tree/master/example/example.py)

## Usage

There only one interface you need to interact with and that is the SVM class. You can also overwrite the default values that are used.  
The SVM header (which should *not* be changed) and the default values are
```python 
"SVM ID", "Antal", "Namn", "Exp", "Skick", "Språk", "Signerad", "Foil", "För Byte", "För Sälj", "Dold", "Pris", "Valuta", "Kommentar", "Bild"
""      , None   , None,    None, "n/a"  , "n/a"  , "Nej"     , "Nej" , "Nej"     , "Nej"     , "Ja"  , None  , "SEK"   , ""         , ""
```

The recommended way to overwrite these values is to get the index of the value and then use that. 
```python
salj_index = svm.SVM_HEADER.index("För Sälj")
svm.SVM_DEFAULT[salj_index] = "Ja"
```

Because a lot of data is different between websites/services but still consistent in your data you can convert a cell in
your data in a manner you want. This is done with the optional argument `converters`, see the [example](https://github.com/Jerakin/svm/tree/master/example/example.py)
for an example of how to use them.

## API

### `SVM(input_tsv, [expand_antal], [header], [converters])`
 This class function is to read the CSV data and put each row into a `Card`, it can then later save into a different CSV file.
 
**PARAMETERS**
* `input_csv` (Pathlike object|string) - The csv/tsv file to convert
* `expand_antal` (bool) - *Default:* `True`, if you want rows with more than 1 cards in it to be added as multiple rows
* `header` (list|set) - *Default:* `converter.DEFAULT_HEADER`, the expected input rows. They need to have the same rows as SVM expects.
* `converters` (list|set) - *Default:* `()`, a list/set of functions to run on the input_csv cells, the required signature is `index, row`.
Where `index` is the cell positional index and `row` is the whole row of that card.  


### translation.json
SVM differs a bit on how it names some cards and sets, this file is to translate from other common formats into the format that SVM expects.


## Workflow proposal 
Before you can do anything with this you would need to have your cards in a CSV format. I have found the easiest and fastest way to do this is to use a app for your phone that can scan cards. The one I use is called Delver Lens and this is how I use it.

1. Sort my cards into expansions (this helps reduce wrong scans and removes the need to change it afterwards)
2. Set my phone on a tripod (I a cheap GorillaPod) and angle it downwards
3. Put a white paper under it.
4. Set the expansion in the scan setting
5. Scan your cards
6. Export your new list as csv and then run the script on it.
7. Upload the converted file into SVM.

# Moxfield format
You can export your collection from [SVM](https://www.svenskamagic.com/profil/export-and-import.php) and then run that have/want file through the moxfield converter to be able to upload the list there. See the `example/moxfield.py`-
