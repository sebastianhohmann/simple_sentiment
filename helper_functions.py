import pandas as pd
import re
import numpy as np

def split_into_sentences(text):

    """
    source:
    https://stackoverflow.com/questions/4576077/python-split-text-on-sentences
    """

    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|me|edu)"
    digits = "([0-9])"    

    if isinstance(text, str) == False:
        return []

    else:
        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = re.sub(prefixes,"\\1<prd>",text)
        text = re.sub(websites,"<prd>\\1",text)
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text) 
        text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
        text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
        text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
        if "”" in text: text = text.replace(".”","”.")
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        if "e.g." in text: text = text.replace("e.g.","e<prd>g<prd>")
        if "i.e." in text: text = text.replace("i.e.","i<prd>e<prd>")
        if "..." in text: text = text.replace("...","<prd><prd><prd>")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace("<prd>",".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        if sentences == []:
            return[text.strip()]
        else:
            return sentences

 
def unstack_listcol(df, lst_col):

    """
    source:
    https://stackoverflow.com/questions/42012152/unstack-a-pandas-column-containing-lists-into-multiple-rows
    """

    ret = pd.DataFrame({\
                        col:np.repeat(df[col].values, df[lst_col].str.len())\
                        for col in df.columns.difference([lst_col])\
                        }).assign(**{lst_col:np.concatenate(df[lst_col].values)})[df.columns.tolist()]    

    return ret        

def count_alpha(text):
    filtered = [c.lower() for c in text if c.isalpha()]
    cnt = len(filtered)
    return cnt    



def clean_text(string): 
    # Turn warnings off because BeautifulSoup give some we don't care about
    # warnings.filterwarnings('ignore')
    
    # Remove xml formatting.
    review_text = BeautifulSoup(string, "lxml").get_text() 
    
    # Turn warnings back on
    # warnings.resetwarnings()
    
    # Remove all characters not in the English alphabet
    string = re.sub("[^a-zA-Z]"," ", string)
    
    # Set all characters to lower case.
    string = string.lower()
    
    return string

