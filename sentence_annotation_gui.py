#!/usr/bin/python3

import tkinter as tk
from nltk.grammar import CFG
from nltk.parse import generate
import pandas as pd

# function that generates n sentences given the grammar
def sent_generator(grammar, n):
    return generate.generate(grammar, n=n)

# function that formats the sentences nicely
def get_sentences(sentences):
    new_sentences = []
    for sentence in sentences:
        new_sentences.append(' '.join(sentence))
    return new_sentences

# function that clears the previous sentence from the text window and displays the new one
def next_sent():
    global ratings, sentences, index, next_button, drop, intro_label
    sentence_display.delete("1.0", tk.END)
    
    # if there is a next sentence
    if index < len(sentences) - 1:
        index += 1
        # saves the rating for the previous sentence so it can be added to the csv
        ratings.append(rating.get())
        rating.set("select")
        sentence_display.insert("1.0", sentences[index])
    
    # else if the current sentence is the last one
    else:
        # get the rating for the last sentence
        ratings.append(rating.get())
        # once all sentences have been displayed, remove everything besides the exit button and display a thank you message
        sentence_display.destroy()
        label = tk.Label(root, text="Thank you for rating these sentences!\n", font=30)
        label.place(x=150, y=15)
        next_button.destroy()
        drop.destroy()
        intro_label.destroy()

# to replace 'select' ratings with an empty string
def clean_data(ratings):
    for i in range(len(ratings)):
        if ratings[i] == 'select':
            ratings[i] = ''
    return ratings

def get_data(sentences, ratings):
    data = []
    for i in range(len(sentences)):
        try:
            data.append([sentences[i], ratings[i]])
        except IndexError:
            data.append([sentences[i], ""])
    return data

if __name__ == '__main__':

    toy_grammar = """
    S -> NP VP
    NP -> Det N
    PP -> P NP
    VP -> 'meowed' | 'chased' NP | 'stretched' PP | 'played' PP
    Det -> 'the' | 'a'
    N -> 'cat' | 'toy' | 'bed'
    P -> 'on' | 'with'
    """

    grammar = CFG.fromstring(toy_grammar)
    sentences = get_sentences(sent_generator(grammar, 10))
        
    # create GUI window
    root = tk.Tk() 
    root.title("Sentence Annotator")
    # width x height
    root.geometry("700x300") 

    # instruction label to be displayed at the top of the window
    intro_label = tk.Label(root, text="Please rate the sentence in the white box using the dropdown menu.\nDisregard punctuation and capitalization.\n", justify=tk.LEFT, font=30)
    intro_label.place(x=75, y=15)

    # makes a text box for the sentences to be displayed in
    sentence_display = tk.Text(root, height=3, width=40, font=16)
    sentence_display.place(x=50, y=75)

    # dropdown options 
    options = ["1", "2", "3", "4", "5"]

    # datatype of menu text 
    rating = tk.StringVar() 

    # initial menu text 
    rating.set("select") 

    # creates the actual drop down menu
    drop = tk.OptionMenu(root, rating, *options) 
    drop.config(height=2, width=5, font=16)
    drop.place(x=475, y=75)

    # sets the index of which sentence the process is on
    index = 0

    # displays the first sentence
    sentence_display.insert("1.0", sentences[0])

    # button to move on to the next sentence, calls the next_sent function to display the next sentences
    next_button = tk.Button(root, text="Next", command=next_sent) 
    next_button.config(height=2, width=6, font=16)
    next_button.place(x=600, y=75)

    # label to display what each number rating means in the window at all times
    schema = tk.Label(root, text="(1) valid, natural sentence\n(2) marked\n(3) grammatical but does not make sense\n(4) ungrammatical, but at least part of it holds coherent meaning\n(5) completely ungrammatical, holds no meaning", justify=tk.LEFT, font=12)
    schema.place(x=50, y=150)

    # initialize the list of ratings
    ratings = []

    root.mainloop() 

    # to save the sentences and their ratings to a csv
    # first clean the ratings so that 'select' is replaced with an empty string
    clean_ratings = clean_data(ratings)

    # then get the data as a list of lists of sentence-rating pairs
    data = get_data(sentences, clean_ratings)

    # save the data to a csv with the columns 'sentence' and 'rating'
    df = pd.DataFrame(data, columns=["Sentence", "Rating"])
    df.to_csv('sentence_ratings.csv', index=False)
