# function 
def plot_marimekko_chart(df, width_var, width_label_var, share_var, sort_category):
    
    """
    this function plots a mekko plot from a data frame. 
    
    it needs: 
    - a dataframe (df),
    - the name of the name of the horizonal width data column (width_var), 
    - the name of the width label column (width_label_var), 
    - the name of the column containing the vertical grouping (share_var), 
    - and the name of the category within share_var which should be used for sorting and which will be above zero.  
    """
    
    #aggregating sum by groups
    my_data = pd.DataFrame(
        df
        .groupby([width_label_var, share_var])[width_var]
        .agg('sum')
        .reset_index()
    )

    print(my_data)
    
    #calculate shares
    my_data["Anteil"] = -my_data[width_var] / my_data.groupby(width_label_var)[width_var].transform('sum')
    
    # mark elektro as only positive
    my_data.loc[my_data.Kraftstoffart == sort_category, "Anteil"] = my_data.Anteil * -1    

    #make wide table from query dataframe
    data_wide = (
        my_data
        .pivot_table(index=[width_label_var],columns=share_var, values='Anteil')
        .sort_values(by=[sort_category], ascending=False)
        .fillna(0)
    )
    
    #define widths of mekko plot
    widths = (
        my_data.groupby(width_label_var)
        .sum(width_var)[width_var]
        .reindex(data_wide.index) #apply sorting order of other dataframe
    )
    
    #define labels for mekko plot
    labels = data_wide.index.to_list()

    #define data dict for mekko plot
    data = data_wide.to_dict('list')

    #mekko plot 
    fig = go.Figure()
    
    #iterate through the groups
    for key in data:
        fig.add_trace(go.Bar(name = key,
                     y = data[key],
                     x = np.cumsum(widths) - widths,
                     width = widths, 
                     offset = 0,
                     customdata=np.transpose([labels, widths*data[key]]),
                     hovertemplate="<br>".join([
                         "%{customdata[0]}",
                         "Gesamtsumme: %{width}",
                         "Anteil: %{y:.2%}",
                         "Anteilssumme: %{customdata[1]}"
                         ])
                 ))

    fig.layout.yaxis.tickformat = ',.0%'              
    fig.update_layout(barmode = "relative") 

    fig.show()
    


# test function
plot_marimekko_chart(my_data, 'column_1', 'column_2', 'column_3', 'category_within_column_3')
