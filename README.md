# Ethiopian Language Toolkit (ethltk)

## Applications

## Installation

- To use this ***ethltk*** package, first install it using pip:

  ```pyhton
    pip install ethltk
  ```

## Usage

1. Amharic Text Preprocessing

- Import the package in your python script and call appropriate functions:
  
  ```pyhton
    from ethltk import amharic_preprocessor, clean_amharic

    # Preprocess text using default preprocess functions in the pipeline
    preprocessed_text = clean_amharic("DHL የዕለቱ My email is john.doe@email.com. እናቀርባለን። amharic 125 <html><h1>Title</h1^X^X></html> 456 processor 18 الرسائل  漢字; simplified Chinese: 汉字; 🤗⭕🤓🤔")
    print(preprocessed_text)
    # output:የዕለቱ እናቀርባለን

    # Preprocess text using custom preprocess functions in the pipeline 
    custom_pipeline = [amharic_preprocessor.remove_tags, amharic_preprocessor.remove_emojis, amharic_preprocessor.remove_punct, amharic_preprocessor.remove_digits, amharic_preprocessor.remove_chinese_chars, amharic_preprocessor.remove_arabic_chars, amharic_preprocessor.remove_english_chars]

    preprocessed_text = clean_amharic("DHL የዕለቱ My email is john.doe@email.com. እናቀርባለን። amharic 125 <html><h1>Title</h1^X^X></html> 456 processor 18 الرسائل  漢字; simplified Chinese: 汉字; 🤗⭕🤓🤔", pipeline=custom_pipeline)

    print(preprocessed_text)
    # output: የዕለቱ     እናቀርባለን
  ```
