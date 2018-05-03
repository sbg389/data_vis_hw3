import json
import altair as alt
import pandas as pd
import os
from pandas.io.json import json_normalize


def createChart(data, zip):

    color_expression    = "(indexof(lower(datum.cuisine), search.term)>=0) || (highlight._vgsid_==datum._vgsid_)"
    color_condition     = alt.ConditionalPredicateValueDef(color_expression, "SteelBlue")
    highlight_selection = alt.selection_single(name="highlight", on="mouseover", empty="none")
    search_selection    = alt.selection_single(name="search", on="mouseover", empty="none", fields=["term"],
    bind=alt.VgGenericBinding('input'))

    vis2 = alt.Chart(data) \
        .mark_bar(stroke="Black") \
        .encode(
            alt.X("total:Q", axis=alt.Axis(title="Restaurants")),
            alt.Y('cuisine:O', sort=alt.SortField(field="total", op="argmax")),
            alt.ColorValue("LightGrey", condition=color_condition),
            ).properties(
                selection=(highlight_selection + search_selection),
                )
    return vis2

def loadData():
    
    #Set base path (source from Huy)
    basePath = os.path.dirname(__file__)
    
    #Load data fom local JSON file (using path)
    
    nyc_restaurant_data = json.load(open(os.path.join(basePath,'nyc_restaurants_by_cuisine.json'), 'r'))
    
    #use the normalize method to flatten the data into a pandas datafrae
    dfNYCRestaurant = json_normalize(nyc_restaurant_data)
    return dfNYCRestaurant