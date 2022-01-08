import os

def export_faq_csv(df_out, name):

    path = f'../data/'

    if not os.path.isdir(path):
        os.makedirs(path)

    df_out.to_csv(f'{path}/{name}_faq.csv')