import pygtool_beta
import xarray as xr
class gtXarray():
    def __init__(self,file,count=1,x=128,y=64,z=36,
                      freq='D',cyclic=False,start=0,end=None):
        self.x=x
        self.y=y
        self.z=z
        self.cyclic=cyclic
        if (z==1 or z==None):
            data=pygtool_beta.read2D(file,count=count,x=self.x,
                                                      y=self.y )
        else:
            data=pygtool_beta.read3D(file,count=count,x = self.x,
                                                      y = self.y,
                                                      z = self.z)
        lon,lat = pygtool_beta.readgrid(x=self.x
                                       ,y=self.y).getlonlat(cyclic=self.cyclic)
        self.head   = data.getheader()
        self.time   = data.getDatetimeIndex(freq=freq)
        self.arr    = data.to_dataarray(start=start,end=end,cyclic=self.cyclic)
        self.item   = self.head[2].decode().strip()
        self.title  = self.head[13].decode().strip()
        self.unit   = self.head[15].decode().strip()
        self.attrs_dict = {'Convention':'COARDS',
                               'title'     :self.title,
                               'unit'      :self.unit
                          }        
        if (z == 1 or z == None):
            self.src_dict   = {self.item:(['time','lat','lon'],self.arr)}
            self.coord_dict = {'time' : self.time,
                               'lat'  : ('lat',lat,{'units':'degrees_north'}),
                               'lon'  : ('lon',lon,{'units':'degrees_east'})
            }
        else:
            self.sigma  = pygtool_beta.readalt(z=self.z).getsig()
            self.src_dict    = {self.item:(['time','sigma','lat','lon'],self.arr)}
            self.coord_dict = {'time' :self.time,
                               'sigma':self.sigma,
                               'lat'  :('lat',lat,{'units':'degrees_north'}),
                               'lon'  :('lon',lon,{'units':'degrees_east'})
            }
    def to_dataset(self):
        ds = xr.Dataset(
            self.src_dict,
            coords = self.coord_dict,
            attrs  = self.attrs_dict
        )
        return ds
