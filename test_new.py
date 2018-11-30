import pandas, re
df = pandas.read_csv(r"C:\Users\AB73171\Documents\python\PC360.csv", sep = ",")
def test(df, num_rator, denom_rator, new_col_name):
    re_list = []
    i = 0
    for x in df[num_rator]:
        if pandas.isna(x):
            df.ix[i, new_col_name] = ''
            continue
        elif bool(re.search("\d+", x)):
            df.ix[i, new_col_name] = int(int(x)/int(df.ix[i, denom_rator]))
        else:
            df.ix[i, new_col_name] = ''
            continue
    i = i+1
df.fillna('')       
test(df, 'UP-Actual', 'UP-Provisioned', 'Up-Prov Rate')
df['Up-Prov Rate']
#pandas.isna(df['UP-Actual'])
