import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean(al):
	#reformat useful columns
	al['Date'] = pd.to_datetime(al['Date of Sale (dd/mm/yyyy)'], format='%d/%m/%Y')
	al['Full Market Price'] = al['Not Full Market Price'].replace({'Yes':0, 'No':1})
	al['VAT exclusive'] = al['VAT Exclusive'].replace({'Yes':1, 'No':0})
	al['Price'] = (al.iloc[:,4]
        	.str.replace(',', '')
        	.str.slice(1)
        	.astype('float32')
)

	#remove all the unnecessary columns
	al = (al
		.drop('Price ()', axis=1)
		.drop('Eircode', axis=1)
		.drop('Property Size Description', axis=1)
		.drop('Not Full Market Price' ,axis=1)
		.drop('VAT Exclusive',axis=1)

	)
	return al

def price_by_year_Dublin(df):
	dub = df[df['County'] == 'Dublin']
	dub['Date'] = pd.to_datetime(dub['Date'])
	dubyearmean = dub.groupby(pd.Grouper(key='Date', freq='Y'))['Price'].mean()
	#plot
	plt.figure(figsize=(10, 6))
	plt.bar(dubyearmean.index.year, dubyearmean.values)
	plt.xlabel('Year')
	plt.ylabel('Average Price')
	plt.title('Average Price per Year')

	plt.show()

df = pd.read_csv("PPR-ALL.csv", encoding='ISO-8859-1', low_memory=False)
cleaned = clean(df)
price_by_year_Dublin(cleaned)
