#%%
change="+2,411.4 (+4.94%)"
change_num= change.rsplit(' ', 1)[0]
change_per=change.rsplit(' ', 1)[1]

rounded_change=round(float(change_num.replace(',', '')),2)

change=change[0]+str(rounded_change)+' '+change_per


# %%
