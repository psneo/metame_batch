# metame batch
Script to bulk process EXEs for [metame](https://github.com/a0rtega/metame).

1) Must have metame installed
2) Additonal -b flag to enable batch processing
3) Output default to current working directory if no specified
4) metame_ouput folder will be created in the output directory
5) any unsuccessful mutation will be stored in metame.log located in metame_ouput folder

```python metame_batch.py -b -i <INPUT_dir> -o <OUTPUT_dir>```
