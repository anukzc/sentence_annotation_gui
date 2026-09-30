# sentence_annotation_gui

A GUI for annotating sentences.

The script generates sentences from a small context-free grammar using NLTK, shows them one at a time in a Tkinter window, and asks the annotator to rate each one. When the window is closed, the sentences and their ratings are saved to a CSV file.

## Requirements

- Python 3
- [NLTK](https://www.nltk.org/)
- [pandas](https://pandas.pydata.org/)
- Tkinter (included with most Python installations)

Install the dependencies with:

```bash
pip install nltk pandas
```

## Usage

```bash
python sentence_annotation_gui.py
```

1. Read the sentence shown in the white box.
2. Choose a rating from the dropdown menu.
3. Click **Next** to go to the next sentence.
4. After the last sentence, a thank-you message appears. Close the window to save the results.

Punctuation and capitalization should be ignored when rating.

## Rating scale

| Rating | Meaning |
| --- | --- |
| 1 | Valid, natural sentence |
| 2 | Marked |
| 3 | Grammatical but does not make sense |
| 4 | Ungrammatical, but at least part of it holds coherent meaning |
| 5 | Completely ungrammatical, holds no meaning |

## Output

Results are written to `sentence_ratings.csv` in the current working directory, with two columns:

- `Sentence`: the generated sentence
- `Rating`: the rating chosen (left empty if no rating was selected, or if the window was closed before reaching that sentence)

## Configuration

The grammar (`toy_grammar`) and the number of sentences generated (10 by default) are set in the `if __name__ == '__main__':` block of `sentence_annotation_gui.py`.
