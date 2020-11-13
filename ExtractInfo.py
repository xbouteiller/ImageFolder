import numpy as np
import pandas as pd 
import os
import sys
import re
import time


def _listdir_fullpath(p, s):
    import os

    d=os.path.join(p, s)
    return [os.path.join(d, f) for f in os.listdir(d) if f.endswith('.csv')]


def parse_folder(path):
    '''
    parse the folder tree and store the full path to target file in a list
    '''
    import os
    import time
    import re
    import pandas as pd


    file_root=[]
    listOfFiles = []


    try:
        file_root = [os.path.join(path, f) for f in os.listdir(path) if f.enswith('.csv')]
        listOfFiles.append(file_root)
        # print(file_root)
    except:
        print('no file detected within root directory')
        pass

    try:
        for pa, subdirs, files in os.walk(path):
            for s in subdirs:
                listOfFiles.append(_listdir_fullpath(p=pa, s=s))
    except:
        print('no file detected within childs directory')
        pass
    try:
        [print("- find : {0} matching files in folder {1}".format(len(i),j)) for i,j in zip(listOfFiles, range(1,len(listOfFiles)+1))]
    except:
        print('no files detected at all')
        pass

    time.sleep(0.1)

    return listOfFiles

def print_listofiles(listOfFiles):
    '''
    print full path to target file
    '''
    # Print the files
    for elem in listOfFiles:
        print(elem)


def extract_name_info(t):
    term = re.findall(r'([a-zA-Z]+)(\d*)-(\d+)?-?(\d+)-(\w{1})',t)
    term = pd.DataFrame(term, columns = ['Rep','Tree', 'Number', 'PicNumber', 'Type'])
    return term

def append_df(df, dfa):
    dfa = pd.concat([dfa]*df.shape[0], ignore_index=True)
    # print('dfa repeated---------------')
    # print(dfa)
    df_c = pd.concat([df, dfa], axis = 1, sort=False)
    return df_c


# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float"
    if progress < 0:
        progress = 0
        status = "Halt..."
    if progress >= 1:
        progress = 1
        status = "Done..."
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1:.2f}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


#%%
if __name__ =="__main__":

    path = os.getcwd()
    print('\nWorking directory is {}\n'.format(path))
    
    directory = os.path.join(os.path.split(path)[0], 'output')
    directory1 = os.path.join(os.path.split(path)[0], 'output/D')
    directory2 = os.path.join(os.path.split(path)[0], 'output/ND')

    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(directory1):
        os.makedirs(directory1)
    if not os.path.exists(directory2):
        os.makedirs(directory2)

    lof = parse_folder(path)
    # print(lof)

    dffull = pd.DataFrame([], columns = ['Measure','Area', 'Perim.', 'Major', 'Minor', 'Angle', 'Median'] + ['Rep','Tree', 'Number', 'PicNumber', 'Type'])
    # print('df_full---------------')
    # print(dffull)

    total_file = []
    [total_file.append(len(l))  for l in lof]
    total_file = sum(total_file) 

    prog = 0
    print("\n\nStarting extraction")
    for lf in lof:
        if len(lf)>0:
            # print('len list > 0')
            # print(lf)
            for l in lf:
                # print(os.path.basename(l))
                dfa = extract_name_info(os.path.basename(l))
                # print('dfa appended---------------')
                # print(dfa)

                df = pd.read_csv(l, sep = ',')
                df = df.rename(columns = {' ':'Measure'})
                # print('df---------------')
                # print(df)

                df_c = append_df(df=df, dfa=dfa)
                # print('df_c---------------')
                # print(df_c)
                
                # print('shape-----------')
                # print(dffull.shape)
                # print(df_c.shape)
                dffull = pd.concat([dffull, df_c], axis =0, ignore_index=True, sort=False)
                # print('df_full---------------')
                # print(dffull)

                # print('path join---------------')
                # print(os.path.join(directory1,os.path.basename(l)))
                Type = df_c['Rep'][0]
                if Type=='D':
                    df_c.to_csv(os.path.join(directory1,os.path.basename(l)))
                else:
                    if Type=='ND':
                        df_c.to_csv(os.path.join(directory2,os.path.basename(l)))
                    else:
                        print('File {} is neither D nor ND type {}'.format(l, Type)) 

                prog += 1
                time.sleep(0.01)
                update_progress(prog/total_file)

        else:
            pass



    dffull.to_csv(os.path.join(directory,'output.csv'))


    


    print("\nExtraction completed")