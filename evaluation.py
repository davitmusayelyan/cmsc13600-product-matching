import datetime
import csv
from analyze import match

def eval_matching(your_matching):
    f = open('Amzon_GoogleProducts_perfectMapping.csv', 'r', encoding = "ISO-8859-1")
    reader = csv.reader(f, delimiter=',', quotechar='"')
    matches = set()
    proposed_matches = set()

    tp = set()
    fp = set()
    fn = set()
    tn = set()

    for row in reader:
        matches.add((row[0],row[1]))
        #print((row[0],row[1]))

    for m in your_matching:
        proposed_matches.add(m)

        if m in matches:
            tp.add(m)
        else:
            fp.add(m)

    for m in matches:
        if m not in proposed_matches:
            fn.add(m)

    if len(your_matching) == 0:
        prec = 1.0
    else:
        prec = len(tp)/(len(tp) + len(fp))

    rec = len(tp)/(len(tp) + len(fn))

    return {'precision': prec, 
            'recall': rec,
            'accuracy': 2*(prec*rec)/(prec+rec) }

#prints out the accuracy
now = datetime.datetime.now()
out = eval_matching(match())
timing = (datetime.datetime.now()-now).total_seconds()
print("----Accuracy----", "----Precision----", "----Recall----",)
print(out['accuracy'], out['precision'] ,out['recall'])
print("---- Timing ----")
print(timing,"seconds")
