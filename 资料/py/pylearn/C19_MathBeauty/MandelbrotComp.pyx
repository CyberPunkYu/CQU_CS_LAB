def getEscapeTime(complex c):
    "计算参数c的逃逸时间，该逃逸速度将用作点的颜色"
    cdef complex z = 0
    cdef int i
    for i in range(100):
        if z.real * z.real + z.imag*z.imag > 4:
            return i
        z = z*z + c
    return i
