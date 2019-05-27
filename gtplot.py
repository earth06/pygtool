import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm
import pandas as pd 
import numpy as np
import cartopy.crs as ccrs
import carto_kit as ckit

sformat=ticker.ScalarFormatter(useMathText=True)

@ticker.FuncFormatter
def latformatter(y,pos):
    if y== 0:
        NS='°'
    elif y <0:
        NS='°S'
    else:
        NS='°N'
    return '{:.0f}{}'.format(np.abs(y),NS)
@ticker.FuncFormatter
def lonformatter(x,pos):
    if x in [0,180,360] :
        EW='°'
    elif (0 < x < 180):
        EW='°E'
    else:
        x=360-x
        EW='°W'
    return '{:.0f}{}'.format(x,EW)
def set_lonticks(ax,dlon=30,labelsize=16):
    """
    set xticks as logitude
    
    Parameter
    ----------
    ax  :matplotlib.axes
    dlon:float
        logitude interval:30 default
    labelsize:int 
        tick label size:16 default
    Return
    ----------
    ax
    """
    ax.xaxis.set_major_locator(ticker.MultipleLocator(dlon))
    ax.xaxis.set_major_formatter(lonformatter)
    ax.xaxis.set_tick_params(labelsize=labelsize)
    return ax
def set_latticks(ax,dlat=15,labelsize=16):
    """
    set xticks as latitude
    
    Parameter
    ----------
    ax  :matplotlib.axes
    dlat:float
        logitude interval:15 default
    labelsize:int
        tick label size:16 default
    Return
    ----------
    ax
    """
    ax.xaxis.set_major_locator(ticker.MultipleLocator(dlat))
    ax.xaxis.set_major_formatter(latformatter)
    ax.xaxis.set_tick_params(labelsize=labelsize)
    return ax


def MMlabel(ax,labelsize=18):
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \n %Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[7]))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
    ax.tick_prams(labelsize=labelsize)
    return ax

def DDlabel(ax,labelsize=18):
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \n %Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[7]))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
    ax.tick_prams(labelsize=labelsize)
    return ax

def contourf(xx,yy,arr,div=20,clabelsize=14,powerlimits=(-1,3)):
    """
    Parameter
    ---------------
    xx,yy  :array_like
    arr    :array_like
            input data
    div    :int or float
            the number of contour
    powerlimits:tuple
           exponent range 

    Return
    ----------------
    fig
    ax

    """
    sformat.set_powerlimits((powerlimits))
    fig=plt.figure(figsize=(10,5),facecolor='w')
    ax=fig.add_subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=180))
    cax=fig.add_axes([0.25,0,0.5,0.05])
    ax=ckit.set_geogrid(ax)
    delta=(arr.max()-arr.min())/(div)
    interval=np.arange(arr.min(),abs(arr.max())*2 +delta,delta)[0:int(div)+1]

    cf=ax.contourf(xx,yy,arr
        ,levels=interval
        ,transform=ccrs.PlateCarree())
    cbar=fig.colorbar(cf,cax
#        ,ticks=interval[::2]
        ,format=sformat
        ,orientation='horizontal')

    cbar.ax.tick_params(labelsize=clabelsize)
    cbar.ax.xaxis.offsetText.set_fontsize(14)
    return fig,ax
def logcontourf(xx,yy,arr,subs=(1.0,),clabelsize=14,offsetTextsize=14):
    """
    Parameter
    ---------------
    xx,yy  :array_like
    arr    :array_like
            input data
    subs   :sequence of float 'all','auto',None,
           default=(1,) ex) (1.0,2.0) 

    Return
    ----------------
    fig
    ax

    """
    fig=plt.figure(figsize=(10,5),facecolor='w')
    ax=fig.add_subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=180))
    cax=fig.add_axes([0.25,0,0.5,0.05])
    ax=ckit.set_geogrid(ax)

    cf=ax.contourf(xx,yy,arr
        ,locator=ticker.LogLocator(subs=subs)
        ,transform=ccrs.PlateCarree())
    cbar=fig.colorbar(cf,cax
        ,orientation='horizontal')
    cbar.ax.tick_params(labelsize=clabelsize)
    cbar.ax.xaxis.offsetText.set_fontsize(offsetTextsize)
    return fig,ax

