patient = ('2012011', 'Eric Zhang', 'male', 77, True, (67,22,78))
#下述代码会发生执行错误
patient[1] = 'NEW VALUE'
patientSort = patient.sort()
patient.remove(77)
patient.clear()