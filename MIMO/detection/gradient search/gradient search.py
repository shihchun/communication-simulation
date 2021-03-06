import numpy as np
import matplotlib.pyplot as plt

snr_db = [0] * 12
snr = [0] * 12
ber = [0] * 12
visited_node = [0]*12
Nt = 2  # 傳送端天線數
Nr = 2  # 接收端天線數
N = 10000  # 執行N次來找錯誤率
for i in range(len(snr)):
    snr_db[i] = 2 * i
    snr[i] = np.power(10, snr_db[i] / 10)

# 這裡採用 Nt x Nr 的MIMO系統，所以原本通道矩陣為 Nr x Nt
# 但在sphere decoding中，因為我們會將向量取實部、虛部來組合，所以通道矩陣也會跟著變成2Nr x 2Nt 矩陣
H = [[0j] * Nt for i in range(Nr)]
H = np.matrix(H)
H_new = [[0j] * (2*Nt) for i in range(2*Nr)]

#H_new = [[-0.28783567+0.j,-0.07330052+0.j, 0.67747695+0.j,-1.45852323+0.j],
    # [0.76937994 + 0.j , 0.44818599 + 0.j ,- 0.55490332 + 0.j , 0.29253252 + 0.j],
   #  [-0.67747695 + 0.j , 1.45852323 + 0.j, - 0.28783567 + 0.j ,- 0.07330052 + 0.j],
    # [0.55490332 + 0.j ,- 0.29253252 + 0.j , 0.76937994 + 0.j , 0.44818599 + 0.j]]

H_new = np.matrix(H_new)
symbol = [0] * Nt      # 因為有Nt根天線，而且接收端不採用任何分集技術，所以會送Nt個不同symbol
symbol_new = [0]*2*Nt  # 除此之外我們還採用將傳送向量取實部、虛部重新組合後，所以向量元素變兩倍
y = [0] * Nr           # 接收端的向量
y_new = [0]*2*Nr       # 將接收端的向量，對其取實部、虛部重新組合後得到的新向量

# 定義星座點，QPSK symbol值域為{1+j , 1-j , -1+j , -1-j }
# 則實部、虛部值域皆為{ -1, 1 }
constellation = [1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]
constellation_new = [-1, 1]

plt.figure('BER')
plt.figure('Average visited node')

for k in range(2):
    for i in range(len(snr_db)):
        error = 0
        total = 0
        visit = 0 #用來紀錄經過幾個node

        K = int(np.log2(len(constellation)))  # 代表一個symbol含有K個bit
        # 接下來要算平均一個symbol有多少能量
        energy = 0
        for m in range(len(constellation)):
            energy += abs(constellation[m]) ** 2
        Es = energy / len(constellation)      # 平均一個symbol有Es的能量
        Eb = Es / K                           # 平均一個bit有Eb能量
        # 因為沒有像space-time coding 一樣重複送data，所以Eb不會再變大
        No = Eb / snr[i]                      # 最後決定K

        for j in range(N):
            for m in range(len(symbol)):  # 決定傳送向量，要送哪些實數元素
                b = np.random.random()  # 產生一個 (0,1) uniform 分布的隨機變數，來決定要送哪個symbol
                for n in range(len(constellation)):
                    if b <= (n + 1) / len(constellation):
                        symbol[m] = constellation[n]
                        break
                symbol_new[m] = symbol[m].real
                symbol_new[m + Nt] = symbol[m].imag

            # 決定MIMO的通道矩陣
            for m in range(Nr):
                for n in range(Nt):
                    H[m, n] = 1 / np.sqrt(2) * np.random.randn() + 1j / np.sqrt(2) * np.random.randn()

                    H_new[m, n] = H[m, n].real
                    H_new[m, n + Nt] = -H[m, n].imag
                    H_new[m + Nr, n] = H[m, n].imag
                    H_new[m + Nr, n + Nt] = H[m, n].real

            # 接下來決定接收端收到的向量y (共有Nr 的元素)
            for m in range(Nr):
                y[m] = 0
            for m in range(Nr):
                for n in range(Nt):
                    y[m] += H[m, n]*symbol[n]
                y[m] += np.sqrt(No/2)*np.random.randn() + 1j*np.sqrt(No/2)*np.random.randn()
                y_new[m] = y[m].real
                y_new[m+Nr] = y[m].imag



            # 接下要先定義gradient_search
            # 用遞迴的方式找出所有可能的錯誤
            def gradient_search(H, detect, optimal_detection, y, current, s0, order, max_differential_metric, constellation):
                # H為通道矩陣、detect向量代表傳送端可能送出的向量、optimal_detection向量是存放detect後的傳送端最有可能送出的向量、current則是紀錄目前遞迴到第幾層
                # y則是接收端實際收到的向量、s0為初始猜測傳送端送出的相量
                # order為要detect到第幾層、max_differential_metric存放目前統計到最大的differential metric
                # constellation為星座點的集合
                visit = 0
                # visit用來紀錄經過幾個nod
                if (current == order) or (current == len(detect)):

                    metric_1 = 0
                    y0 = H * (np.matrix(s0).transpose())
                    for m in range(len(y)):
                        metric_1 += abs(y[m] - y0[m, 0]) ** 2

                    metric_2 = 0
                    y1 = H * (np.matrix(detect).transpose())
                    for m in range(len(y)):
                        metric_2 += abs(y[m] - y1[m, 0]) ** 2

                    if metric_1 - metric_2 > max_differential_metric[0]:
                        max_differential_metric[0] = metric_1 - metric_2
                        for i in range(len(detect)):
                            optimal_detection[i] = detect[i]


                else:
                    #假設猜測的初始傳送向量s0，其第current個元素是正確的
                    visit += 1
                    visit += gradient_search(H, detect, optimal_detection, y, current+1, s0, order, max_differential_metric, constellation)

                    #假設猜測的初始傳送向量s0，其第current個元素是錯誤的
                    for i in range(len(constellation)):
                        if s0[current] != constellation[i]:
                            visit += 1
                            temp = detect[current]
                            detect[current] = constellation[i]
                            visit += gradient_search(H, detect, optimal_detection, y, current+1, s0, order, max_differential_metric, constellation)
                            detect[current] = temp

                return visit

            # 我們也定義一個ML detection
            def ML_detection(H, detect, optimal_detection, y, current, min_distance, constellation):
                # H為通道矩陣、detect向量代表傳送端可能送出的向量、optimal_detection向量是存放detect後的傳送端最有可能送出的向量
                # y則是接收端實際收到的向量、current為目前遞迴到的位置、min_distance紀錄目前detection最小的距離差
                # constellation為星座點的集合
                visit = 0
                # visit用來紀錄經過幾個node
                Nt = H.shape[1]
                Nr = H.shape[0]
                if current == Nt:
                    # 找出detect向量和接收端收到的y向量間的距離
                    detect_y = [0] * Nr  # detect_y為detect向量經過通道矩陣後的結果
                    for i in range(Nr):
                        for j in range(Nt):
                            detect_y[i] += H[i, j] * detect[j]
                    # 接下來找出detect_y向量和y向量間距
                    s = 0
                    for i in range(Nr):
                        s += abs(y[i] - detect_y[i]) ** 2
                    s = np.sqrt(s)
                    # 所以s 即為兩向量間的距離的平方

                    # 如果detect出來的結果比之前的結果好，就更新optimal_detection向量
                    if s < min_distance[0]:
                        min_distance[0] = s
                        for i in range(Nt):
                            optimal_detection[i] = detect[i]
                else:
                    for i in range(len(constellation)):
                        detect[current] = constellation[i]
                        visit += 1
                        visit += ML_detection(H, detect, optimal_detection, y, current + 1, min_distance, constellation)
                return visit


            if k == 0:
                # 使用gradient_search
                detect = [0] * (Nt*2)
                optimal_detection = [0] * (Nt*2)
                s0 = [1] * (Nt*2)
                #決定s0向量的元素
                for m in range(len(s0)):
                    s0[m] = 0
                    for n in range(2*Nr):
                        s0[m] += H_new[n,m] * y_new[m]
                    if s0[m] > 0 :
                        s0[m] = 1
                    else:
                        s0[m] = -1

                # 讓detect向量變得跟s0向量一樣
                for m in range(len(s0)):
                    detect[m] = symbol_new[m]
                    s0[m] = symbol_new[m]

                current = 0
                order = 2*Nt
                max_differential_metric = [-10**9]

                visit += gradient_search(H_new, detect, optimal_detection, y_new, current, s0, order, max_differential_metric, constellation_new)

            elif k == 1:
                # 使用ML detection
                detect = [0] * (Nt*2)
                optimal_detection = [0] * (Nt*2)
                min_distance = [10 ** 9]
                visit += ML_detection(H_new, detect, optimal_detection, y_new, 0, min_distance, constellation_new)

            # 接下來計算QPSK錯幾個bit
            for m in range(len(symbol_new)):
                if abs(optimal_detection[m].real - symbol_new[m].real) == 2:
                    error += 1
                if abs(optimal_detection[m].imag - symbol_new[m].imag) == 2:
                    error += 1

        ber[i] = error / (K * Nt * N)  # 除以K是因為一個symbol有K個bit
        visited_node[i] = visit / N

    if k == 0:
        plt.figure('BER')
        plt.semilogy(snr_db, ber, marker='o', label='QPSK (gradient_search order={0})'.format(order))
        plt.figure('Average visited node')
        plt.plot(snr_db, visited_node, marker='o', label='QPSK (gradient_search order={0})'.format(order))
    elif k == 1:
        plt.figure('BER')
        plt.semilogy(snr_db, ber, marker='o', label='QPSK (ML decoding)')
        plt.figure('Average visited node')
        plt.plot(snr_db, visited_node, marker='o', label='QPSK (ML decoding)')

plt.figure('BER')
plt.xlabel('Eb/No , dB')
plt.ylabel('ber')
plt.legend()
plt.grid(True, which='both')

plt.figure('Average visited node')
plt.xlabel('Eb/No , dB')
plt.ylabel('Average visited node')
plt.legend()
plt.grid(True, which='both')
plt.show()