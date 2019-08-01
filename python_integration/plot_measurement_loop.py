import matplotlib.pyplot as plt
import csv

filename = 'measurement-loop-2019-08-01-13-06-20'
init_select = 1200
pulse_select = 200

#Data colums
init_amp = []
pulse_amp =[]
idx = [] 
time = []
voltage = []
deformation = []

with open(filename + '.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for row in csv_reader:
        if(int(row[0]) == init_select and int(row[1]) == pulse_select):
            init_amp.append(float(row[0]))
            pulse_amp.append(float(row[1]))
            idx.append(int(row[2]))
            time.append(float(row[3]))
            voltage.append(float(row[4]))
            deformation.append(float(row[5]))

plt.figure(1)
plt.plot(time, voltage)
plt.xlabel('Time')
plt.title("Voltage with Init: %4.0f, Pulse: %4.0f" % (init_select, pulse_select) )

plt.figure(2)
plt.plot(time, deformation, label='Deformation')
plt.xlabel('Time')
plt.title("Deformation with Init: %4.0f, Pulse: %4.0f" % (init_select, pulse_select) )
plt.legend()
plt.show()