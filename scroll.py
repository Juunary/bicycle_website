import sys
Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel = 2023,10,26,"Seoul","Random"

if Get_selectedCity=='Seoul':
    Get_selectedCity=0
else:
    Get_selectedCity=1

if Get_vselectedModel=='Random':
    Get_vselectedModel=1
elif Get_vselectedModel=='Time_series':
    Get_vselectedModel==2

def data_customerpick():
    return Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel
