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
cat sample/hoge.nfd.txt | unicode read -n NFD -l
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
Below command, you can see a list of categories in the 1st level.

```
% unicode.py list
0: European Scripts
1: Modifier Letters
2: Combining Marks
3: African Scripts
4: Middle Eastern Scripts
5: Central Asian Scripts
6: South Asian Scripts
7: Southeast Asian Scripts
8: Indonesia & Oceania Scripts
9: East Asian Scripts
10: American Scripts
11: Other
12: Notational Systems
13: Punctuation
14: Alphanumeric Symbols
15: Technical Symbols
16: Numbers & Digits
17: Mathematical Symbols
18: Emoji & Pictographs
19: Other Symbols
20: Specials
21: Private Use
22: Surrogates
23: Noncharacters in Charts
```

You can pick one of them to see.  Let's see Emoji and Pictographs.
With the -c option, you can see a list of subcategories under the category.

```
% unicode.py list -c 'Emoji & Pictographs'
## Emoji & Pictographs
0: 'Dingbats'
1: 'Ornamental Dingbats'
2: 'Emoticons'
3: 'Miscellaneous Symbols'
4: 'Miscellaneous Symbols And Pictographs'
5: 'Supplemental Symbols and Pictographs'
6: 'Symbols and Pictographs Extended-A'
7: 'Transport and Map Symbols'
```

You can specify a case insensitive part of the name, or the number of the index.
Below two commands result same output.

```
% unicode.py list -c emoji
% unicode.py list -c 18
```

Now, you can see a list of the charactores in 'Emoticons'

```
% unicode.py list -c 'Emoji & Pictographs' -k Emoticons
Emoticons 1F600-1F64F 80
      0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
   0 😔 😕 😖 😗 😘 😙 😚 😛 😜 😝 😞 😟 😠 😡 😢 😣 😤 😥 😦 😧
   1 😨 😩 😪 😫 😬 😭 😮 😯 😰 😱 😲 😳 😴 😵 😶 😷 😸 😹 😺 😻
   2 😼 😽 😾 😿 🙀 🙁 🙂 🙃 🙄 🙅 🙆 🙇 🙈 🙉 🙊 🙋 🙌 🙍 🙎 🙏
```

You can use the -k option as same as the -c option.
So, below two commands result same output.

```
% unicode list -c emoji -k 2
% unicode list -c 18 -k emoti
```

Or, you can just specify 'emoti' as it can search with the entire db.

```
% unicode.py list -k emoti
Emoticons 1F600-1F64F 80
      0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
   0 😔 😕 😖 😗 😘 😙 😚 😛 😜 😝 😞 😟 😠 😡 😢 😣 😤 😥 😦 😧
   1 😨 😩 😪 😫 😬 😭 😮 😯 😰 😱 😲 😳 😴 😵 😶 😷 😸 😹 😺 😻
   2 😼 😽 😾 😿 🙀 🙁 🙂 🙃 🙄 🙅 🙆 🙇 🙈 🙉 🙊 🙋 🙌 🙍 🙎 🙏
```

With the -a option, you can see the entire charactors under the Emoji and Pictgraphs.

```
unicode.py l -c emoji -a
```

You may see many squares.  That means your terminal doesn't support the symbols.

Usage.

```
% unicode.py list -h
usage: unicode list [-h] [-c CATEGORY_HINT] [-a] [-r] [-k KEYWORD_HINT]
                    [--columns NB_COLUMNS]

options:
  -h, --help            show this help message and exit
  -c CATEGORY_HINT      specify a unicode category, which is case-insensitive,
                        can be a part of the name, can be a number in the
                        list.
  -a                    show all chars under the category specified.
  -r                    show the range of code point. It is not valid when the
                        hint unique a subategory or the -a option is used.
  -k KEYWORD_HINT       specify a unicode sub category name, which is case-
                        insensitive, can be a part of the name, can be a
                        number in the list.
  --columns NB_COLUMNS  specify the number of the columns to show.
```

