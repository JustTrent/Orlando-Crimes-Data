#!/usr/bin/env python
# coding: utf-8
# Trent Nguyen
# just.trent.n@gmail.com
#%%
import gmaps
#import numpy as np
#import pandas as pd
#import calendar
import ipywidgets as widgets
from IPython.display import display
#%%


#%%
class clHeatMap:
    
    def __init__(self, data, sDateColName, sLocationColName):
        '''
        Display heatmap with that will change with the years slider.
        data = DataFrame with 1 column of TimeStamp, 1 column of GPS coordinates
        sDateColName = name of Time Date column; TimeStamp type
        sLocationColName = name of GPS coordinates column; 
            format = (float64: Latitude, float64: Longitude)
        '''
    
        self._data = data
        self._heatmap = None
        self._slider = None
        self._DateColName = sDateColName
        self._LocationColName = sLocationColName
        
        _initYear = min(data[sDateColName].dt.year)
        
        title = widgets.HTML('<h3>Orlando Crimes, by Years</h3>')
        
        map_fig = self._RenderMap(_initYear)
        controls = self._RenderControls(_initYear)
        self._container = widgets.VBox([title, controls, map_fig])
        

    def Render(self):
        display(self._container)                

    def ReturnMap(self):
        return self._container
        
    def _OnYearChange(self, change):
#        year = self._slider.value        
#        self._heatmap.locations = self._LocationsForYear(year)
        self._heatmap.locations = self._LocationsForYear(change['new'])
        
        return self._container

    def _LocationsForYear(self, year):
        
        ret = self._data[self._data[self._DateColName].dt.year == year][ self._LocationColName ]
        
        return ret

    def _RenderMap(self, initial_year):
        
        fig = gmaps.figure()
        self._heatmap = gmaps.heatmap_layer(
            self._LocationsForYear(initial_year),
            max_intensity=100,
            point_radius=8
        )
        fig.add_layer(self._heatmap)
        return fig
    
    def _RenderControls(self, initial_year):
        self._slider = widgets.IntSlider(
            value=initial_year,
            min=min(self._data[self._DateColName].dt.year),
            max=max(self._data[self._DateColName].dt.year),
            description='Year',
            continuous_update=False,
            step=1,
            readout=True
        )
        
#        self._total_box = widgets.Label(
#            value=self._total_casualties_text_for_year(initial_year)
#        )
        
        self._slider.observe(self._OnYearChange, names='value')
        
        controls = widgets.HBox(
            [self._slider],
            layout={'justify_content': 'space-between'}
        )
        return controls

#%%
#'''        
#testdata = pd.DataFrame()
#testdata['Date'] = pd.to_datetime( ['2013-02-19 12:41:00', '2014-08-06 02:55:00', '2014-10-30 22:15:00', '2016-01-06 10:39:00', '2015-10-06 06:55:00'])
#testdata['Location'] = [(28.54518403, -81.40556136), (28.44153996, -81.23261223), (28.51884164, -81.46848512), (28.52377872, -81.43230433),(28.53921282, -81.38900691)]
#'''

#%%
#'''
#testmap = clHeatMap(testdata, 'Date', 'Location')
#testmap.Render()
#'''
