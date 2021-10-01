import requirements as req

alt = 200e3
i = 45
lat = 28.5

vcirc = req.v_circ(alt)
dv = vcirc + req.v_grav(alt) - req.v_rot(vcirc, lat, i) + 300
