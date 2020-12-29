unicode
=======

A kichen knife tool for unicode.  The features are below for example.

- Reading string, with or without normalizing.
- Display charactors of unicode specified.
- Showing categories and charactors.

```
% unicode.py show -nN 'SMILING FACE WITH OPEN MOUTH' | unicode.py read -l
No.  Chr    EAA SZ CP   Name
==== ====== === == ==== ==========
  1: [😃 ] W   2: 0001F603 SMILING FACE WITH OPEN MOUTH
  2: [😄 ] W   2: 0001F604 SMILING FACE WITH OPEN MOUTH AND SMILING EYES
  3: [😅 ] W   2: 0001F605 SMILING FACE WITH OPEN MOUTH AND COLD SWEAT
  4: [😆 ] W   2: 0001F606 SMILING FACE WITH OPEN MOUTH AND TIGHTLY-CLOSED EYES
```

## Reading String

It decodes the input string into Unicode and to show the encoded string.
Usually, it normalizes with NFC to show the string.
So, you can normalize a decomposed string like below.

```
% cat sample/hoge.nfd.txt
ほげはげ

% cat sample/hoge.nfd.txt | unicode.py read
ほげはげ
```

If you want to see a decomposed string, you can use the -n NFD option.

```
% echo ほげはげ | unicode.py read -n NFD
ほげはげ
```

With the -l option, you can see the charactors in detail.

```
No.  Chr    EAA SZ CP   Name
==== ====== === == ==== ==========
  1: [ほ ] W   2: 307B HIRAGANA LETTER HO
  2: [け ] W   2: 3051 HIRAGANA LETTER KE
  3: [゙ ] W   2: 3099 COMBINING KATAKANA-HIRAGANA VOICED SOUND MARK
  4: [は ] W   2: 306F HIRAGANA LETTER HA
  5: [け ] W   2: 3051 HIRAGANA LETTER KE
  6: [゙ ] W   2: 3099 COMBINING KATAKANA-HIRAGANA VOICED SOUND MARK
  7: ['\n'] N   1: 000A None
```

More examples.

```
unicode.py read -f sample/hoge.nfd.txt
unicode.py read -f sample/hoge.nfc.txt -o output.txt
unicode.py read -f sample/hoge.nfc.txt -n NFD -l
```

Usage.

```
% unicode.py read -h
usage: unicode.py read [-h] [-f INPUT_FILE] [-o OUTPUT_FILE] [-l] [-c] [-E]
                       [-n NORMALIZE_MODE]

optional arguments:
  -h, --help            show this help message and exit
  -f INPUT_FILE         specify the filename for input.default is stdin.
  -o OUTPUT_FILE        specify the filename for output.default is stdout.
  -l                    show the unicode name for each charactor.
  -c                    add the number of charactors to the tail.
  -E                    disable to handle the input text as EAA.
  -n NORMALIZE_MODE, --normalize-mode NORMALIZE_MODE
                        specify a mode to normalize. valid mode is: ['NFC',
                        'NFKC', 'NFD', 'NFKD']
```

## Displaying Charactors from Unicode Code Points, or Unicode name.

Examples.

```
% unicode.py show 1F64b 1f3fb
🙋🏻
% unicode.py show 307B 3051 3099
ほげ
% unicode.py show 845B e0100
葛󠄀
```

You can find the unicode name of each code point.

```
% unicode.py show 307B 3051 3099 -l
  307B: ほ : HIRAGANA LETTER HO
  3051: け : HIRAGANA LETTER KE
  3099: ゙ : COMBINING KATAKANA-HIRAGANA VOICED SOUND MARK
```

With the -s option,
you can see the characors of a range of two code points.

```
% unicode.py show 3041 304F -s
ぁあぃいぅうぇえぉおかがきぎく
```

If you want to specify the code points in integer,
you can use the -i option.
So, below commands result same output.

```
% unicode.py show 12353 12367 -s -i 
ぁあぃいぅうぇえぉおかがきぎく
```

You can see the charactors from a part of or full Unicode name.

```
% unicode.py show -n 'SMILING FACE WITH OPEN MOUTH'  
😃😄😅😆
```

Usage.

```
% unicode.py show -h
usage: unicode.py show [-h] [-s] [-l] [-i] [-n] [-x] [-N] arg [arg ...]

positional arguments:
  arg               a code point in hex.

optional arguments:
  -h, --help        show this help message and exit
  -s                indicate to show a series of the chars specified by the
                    two code points.
  -l                show the chars in virtical with the unicode name.
  -i                specify that the arg is a code point in integer.
  -n                specify that the arg is a part of a unicode name.
  -x                disable to show a unicode name of the option -l.
  -N, --no-newline  disable to add a newline.
```

## Listing Unicode Charactors.

You can see the charactors in a category you specified.
Firstly, you can see a list of categories in the 1st level.

```
% unicode.py list
-c 'European Scripts'
-c 'Modifier Letters'
-c 'Combining Marks'
-c 'African Scripts'
-c 'Middle Eastern Scripts'
-c 'Central Asian Scripts'
-c 'South Asian Scripts'
-c 'Southeast Asian Scripts'
-c 'Indonesia & Oceania Scripts'
-c 'East Asian Scripts'
-c 'American Scripts'
-c 'Other'
-c 'Notational Systems'
-c 'Punctuation'
-c 'Alphanumeric Symbols'
-c 'Technical Symbols'
-c 'Numbers & Digits'
-c 'Mathematical Symbols'
-c 'Emoji & Pictographs'
-c 'Other Symbols'
-c 'Specials'
-c 'Private Use'
-c 'Surrogates'
-c 'Noncharacters in Charts'
```

You can pick one of them.  Let's see Emoji and Pictographs.

```
% unicode.py list -c 'Emoji & Pictographs'
-c 'Emoji & Pictographs' -k 'Dingbats'
-c 'Emoji & Pictographs' -k 'Ornamental Dingbats'
-c 'Emoji & Pictographs' -k 'Emoticons'
-c 'Emoji & Pictographs' -k 'Miscellaneous Symbols'
-c 'Emoji & Pictographs' -k 'Miscellaneous Symbols And Pictographs'
-c 'Emoji & Pictographs' -k 'Supplemental Symbols and Pictographs'
-c 'Emoji & Pictographs' -k 'Symbols and Pictographs Extended-A'
-c 'Emoji & Pictographs' -k 'Transport and Map Symbols'
```

Now, you can see a list of the charactores in 'Emoticons'

```
% unicode.py list -c 'Emoji & Pictographs' -k 'Emoticons'
Emoticons 1F600-1F64F 80
      0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
   0 😔 😕 😖 😗 😘 😙 😚 😛 😜 😝 😞 😟 😠 😡 😢 😣 😤 😥 😦 😧
   1 😨 😩 😪 😫 😬 😭 😮 😯 😰 😱 😲 😳 😴 😵 😶 😷 😸 😹 😺 😻
   2 😼 😽 😾 😿 🙀 🙁 🙂 🙃 🙄 🙅 🙆 🙇 🙈 🙉 🙊 🙋 🙌 🙍 🙎 🙏
```

Or, just specify a part of 'Emoticons' like below.

```
% unicode.py list -k emoti
Emoticons 1F600-1F64F 80
      0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
   0 😔 😕 😖 😗 😘 😙 😚 😛 😜 😝 😞 😟 😠 😡 😢 😣 😤 😥 😦 😧
   1 😨 😩 😪 😫 😬 😭 😮 😯 😰 😱 😲 😳 😴 😵 😶 😷 😸 😹 😺 😻
   2 😼 😽 😾 😿 🙀 🙁 🙂 🙃 🙄 🙅 🙆 🙇 🙈 🙉 🙊 🙋 🙌 🙍 🙎 🙏
```

More examples.

```
unicode.py list -c scripts -a
unicode.py list -c scripts -k rokee
unicode.py list -c 'East Asian Scripts' -k 'CJK Extension C'
```

Usage.

```
% unicode.py list -h
usage: unicode.py list [-h] [-c CATEGORY_HINT] [-a] [--show-code-point]
                       [-k KEYWORD] [--strict] [--columns NB_COLUMNS]

optional arguments:
  -h, --help            show this help message and exit
  -c CATEGORY_HINT      specify a category or a part of category name.
  -a                    show all chars under the category specified.
  --show-code-point     show the range of code point.
  -k KEYWORD            specify a keyword of the unicode sub category name.
  --strict              specify to search strictly.
  --columns NB_COLUMNS  specify the number of the columns to show.
```

