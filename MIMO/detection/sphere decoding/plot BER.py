import numpy as np
import matplotlib.pyplot as plt

Nr = 2
constellation_num = 3

if constellation_num == 1:
    constellaion_name = 'QPSK'
elif constellation_num == 2:
    constellaion_name = '16QAM'
elif constellation_num == 3:
    constellaion_name = '64QAM'

if Nr == 2:
    if constellaion_name == 'QPSK':
        snr = [3.010299956639812 ,5.0102999566398125, 7.0102999566398125, 9.010299956639813, 11.010299956639813 ,13.010299956639813, 15.010299956639813, 17.010299956639813, 19.010299956639813 ,21.010299956639813 ,23.010299956639813 ,25.010299956639813 ,27.010299956639813  ]
    if constellaion_name == '16QAM':
        snr = [3.010299956639812, 5.5102999566398125, 8.010299956639813, 10.510299956639813, 13.010299956639813, 15.510299956639813, 18.010299956639813, 20.510299956639813, 23.010299956639813, 25.510299956639813, 28.010299956639813, 30.510299956639813, 33.01029995663981  ]
    if constellaion_name == '64QAM':
        snr = [3.010299956639812, 6.0102999566398125, 9.010299956639813, 12.010299956639813, 15.010299956639813 ,18.010299956639813, 21.010299956639813, 24.010299956639813 ,27.010299956639813 ,30.010299956639813 ,33.01029995663981 ,36.01029995663981 ,39.01029995663981 ]
elif Nr == 4:
    if constellaion_name == 'QPSK':
        snr =  [0.0, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5, 15.0, 16.5, 18.0]
    if constellaion_name == '16QAM':
        snr = [0.0 ,1.9 ,3.8 ,5.699999999999999 ,7.6 ,9.5 ,11.399999999999999, 13.299999999999999, 15.2, 17.099999999999998, 19.0, 20.9 ,22.799999999999997 ]
    if constellaion_name == '64QAM':
        snr = [0.0, 2.3, 4.6, 6.8999999999999995, 9.2, 11.5, 13.799999999999999, 16.099999999999998, 18.4, 20.7, 23.0, 25.299999999999997, 27.599999999999998]


ber1 = [0.22460039166666668 ,0.17382538333333333 ,0.12232576666666667 ,0.07432002916666666 ,0.037424175 ,0.015627345833333334 ,0.005613691666666667 ,0.0017871125 ,0.0005245375 ,0.00014124583333333332 ,3.695e-05 ,1.0029166666666667e-05 ,2.7958333333333334e-06   ]
plt.semilogy(snr,ber1,marker = 'o',label='branch=[2,3,8,8]'.format(constellaion_name))
#ber1 = [0.22463491666666666 ,0.1737168 ,0.12234528333333333 ,0.07425305 ,0.03743045 ,0.015628033333333333 ,0.005613716666666667 ,0.0018000416666666666 ,0.0005342166666666667 ,0.0001495 ,4.270833333333333e-05 ,1.2033333333333334e-05 ,3.5666666666666667e-06 ]
#plt.semilogy(snr,ber1,marker = 'o',label='branch=[2,4,6,8]'.format(constellaion_name))
#ber1 = [0.22477961666666665 ,0.17384954166666666 ,0.12251763333333333 ,0.07443115 ,0.037497325 ,0.015708708333333335 ,0.005640283333333333 ,0.001820975 ,0.0005373916666666667 ,0.00015094166666666667 ,4.046666666666667e-05 ,1.1741666666666666e-05 ,3.0583333333333334e-06  ]
#plt.semilogy(snr,ber1,marker = 'o',label='branch=[2,2,8,8]'.format(constellaion_name))
#ber1 = [0.22452531666666667 ,0.17379454166666666 ,0.12231465833333334 ,0.07427365 ,0.037393775 ,0.015624641666666666 ,0.005628925 ,0.0017849 ,0.0005186083333333333 ,0.00013924166666666666 ,3.735833333333333e-05 ,9.258333333333332e-06 ,2.1166666666666666e-06  ]
#plt.semilogy(snr,ber1,marker = 'o',label='branch=[2,4,8,8]'.format(constellaion_name))
#ber1 = [0.22691825, 0.17538941666666666, 0.12387025 ,0.07589525, 0.038705916666666666, 0.016584, 0.006136, 0.0020709166666666667, 0.0006873333333333333 ,0.000242 ,8.941666666666667e-05 ,3.483333333333333e-05 ,1.4416666666666667e-05  ]
#plt.semilogy(snr,ber1,marker = 'o',label='SD-BF-soft(5)'.format(constellaion_name))
#ber1 = [0.22486266666666666, 0.17367875, 0.122514 ,0.0742325, 0.037656166666666664, 0.01567525, 0.0057, 0.0018841666666666666, 0.0005720833333333333, 0.00019675 ,6.2e-05 ,2.225e-05, 7.525e-06 ]
#plt.semilogy(snr,ber1,marker = 'o',label='SD-BF-soft(6)'.format(constellaion_name))
#ber1 = [0.22669208333333332, 0.17488983333333333, 0.123328, 0.07567808333333334, 0.03848583333333333, 0.016413416666666666, 0.005931583333333333 ,0.0019581666666666666 ,0.0005970833333333334 ,0.0001665 ,5.2333333333333336e-05 ,1.5916666666666666e-05, 5.0833333333333335e-06  ]
#plt.semilogy(snr,ber1,marker = 'o',label='SD-BF-soft(7)'.format(constellaion_name))
#ber1 = [0.22455975, 0.17362033333333332 ,0.12234025 ,0.07428183333333334, 0.037463416666666666, 0.015653416666666666, 0.005564916666666667, 0.0017913333333333334 ,0.0005375 ,0.000138, 3.9916666666666663e-05, 9.5e-06, 2.0833333333333334e-06  ]
#plt.semilogy(snr,ber1,marker = 'o',label='SD-BF-soft(8)'.format(constellaion_name))



if Nr == 2:
    if constellaion_name == 'QPSK':
        ber = [0.08698105, 0.05292785, 0.029031225, 0.01455505, 0.006733625 ,0.002981925 ,0.00126145 ,0.000511875, 0.0002136 ,8.385e-05 ,3.3725e-05, 1.4225e-05, 5.9e-06 ]
    if constellaion_name == '16QAM':
        ber = [0.1686901625, 0.1186008875, 0.0733288, 0.039247575 ,0.018208725, 0.0074320375, 0.0027901125, 0.0009668875, 0.0003223875 ,0.0001040875, 3.46e-05, 1.03375e-05 ,3.15e-06  ]
    if constellaion_name == '64QAM':
        ber = [0.22451341666666666, 0.17355816666666668 ,0.12235333333333333 ,0.07435666666666667, 0.03724375 ,0.015678166666666667, 0.005537916666666667, 0.00178375 ,0.0005044166666666667 ,0.00014083333333333333 ,3.316666666666667e-05 ,8e-06 ,2.1666666666666665e-06 ]
plt.semilogy(snr,ber,marker = 'o',label='ML detection')
ticks = [0] * 20
for i in range(20):
    ticks[i] = 2 * i
plt.xticks(ticks)
plt.xlim(min(snr) - 1, max(snr) + 1)
plt.xlabel('Eb/No , dB')
plt.ylabel('ber')
plt.grid(True, which='both')
plt.legend()
plt.show()