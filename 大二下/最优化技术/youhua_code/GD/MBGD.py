

def batch_generator(x, y, batch_size):         //batch生成器
    nsamples = len(x)
    batch_num = int(nsamples / batch_size)
    indexes = np.random.permutation(nsamples)
    for i in range(batch_num):
        yield (x[indexes[i*batch_size:(i+1)*batch_size]], 
                y[indexes[i*batch_size:(i+1)*batch_size]])
 
 
for epoch in range(epoches):
    for x_batch, y_batch in batch_generator(X_train, y_train, batch_size):
        y_hat = np.dot(weight, x_batch.T)
        deviation = y_hat - y_batch.reshape(y_hat.shape)
        gradient = 1/len(x_batch) * np.dot(deviation, x_batch)
        weight = weight - learning_rate*gradient
