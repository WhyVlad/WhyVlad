#!/usr/bin/env python
import Functions
import time
tic = time.perf_counter()
MAGIC = Functions.getZTMAGIC()
YFToken = Functions.getYFSecurityToken()
MyList = Functions.getYFJSonDataSourcesList()
Functions.updateYFDataSources(MAGIC,YFToken,MyList)
print(MAGIC)
