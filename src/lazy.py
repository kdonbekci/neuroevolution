# from config import Configuration
# from tensorflow.keras import backend as K
# from tensorflow.keras.utils import plot_model
# K.set_floatx(Configuration.MODEL_FLOAT_PRECISION)
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Dense, Activation, Input, Lambda, Concatenate, Add
# from tensorflow.keras.models import load_model, save_model
# from sklearn.model_selection import train_test_split
#
# a = Input(shape=(2,))
# b = Input(shape=(1,))
# concat = Concatenate()([a,b])
# concat
# add = Add()([a,b])
# c = Dense(5)(concat)
# d = Dense(5)(add)
# model = Model(inputs=[a,b], outputs=[c, d])
# model.summary()
#
# a.graph
# b.graph
# plot_model(model)
# sess = tf.Session()
# sess.run()
