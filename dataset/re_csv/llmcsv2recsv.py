import re
import pandas as pd

def get_offsets(sentence, head, tail):
    head_offset = -1
    tail_offset = -1

    head_pos = sentence.find(head)
    if head_pos != -1:
        head_offset = head_pos

    tail_pos = sentence.find(tail)
    if tail_pos != -1:
        tail_offset = tail_pos

    return head_offset, tail_offset


df = pd.read_csv('train.csv')

new_df = df.copy()
for i, row in df.iterrows():
    sentence = row['input']
    head = str(row['subject'])
    tail = str(row['object'])

    head_offset, tail_offset = get_offsets(sentence, head, tail)

    if head_offset == -1 or tail_offset == -1:
        new_df = new_df.drop(index=i)
    else:
        new_df.loc[i, 'head_offset'] = head_offset
        new_df.loc[i, 'tail_offset'] = tail_offset

new_df.to_csv('re_train.csv', index=False, encoding='utf_8_sig')