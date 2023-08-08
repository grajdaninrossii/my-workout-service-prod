
from tensorflow.keras.layers import Flatten, Dense, Dropout, Normalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import AUC
# import tensorflow as tf

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
from random import randint

# from sklearn.preprocessing import StandardScaler

from tensorflow import keras

neuronet_model = keras.models.load_model('./saved_neuronet_model/model_6')


neuronet_model.summary()
# **Загрузка данных**

url = "./data_count_exercise_test.csv"
data_workout_exercises = pd.read_csv(url)
# del data_workout_exercises['Unnamed: 0']

data_workout_exercises['target_count'] += np.random.randint(-2, 3, size=data_workout_exercises['target_count'].shape[0])
data_workout_exercises.head()


data_workout_exercises['target_count'].where(
    ~(data_workout_exercises.target_count < 0),
    other=0,
    inplace=True
    )
# for ids in sorted(data_workout_exercises['id_exercise'].unique()):
#     df = data_workout_exercises.loc[data_workout_exercises['id_exercise'] == ids]
#     print('Упражнение id:', ids)
#     print('Среднее количество повторений женщины:', df.loc[df['id_gender'] == 2][['target_count']].mean())
#     print('Среднее количество повторений мужчины:', df.loc[df['id_gender'] == 1][['target_count']].mean())
#     print('Макс. кол-во повторений:', df['target_count'].max())
#     print('Мин. кол-во повторений:', df['target_count'].min())
#     print()

# data_workout_exercises.isna().sum()

# dataset = data_workout_exercises.dropna()

# Разделяем данные на тренировочные и тестовые
train_dataset = data_workout_exercises.sample(frac=0.8, random_state=0)
test_dataset = data_workout_exercises.drop(train_dataset.index)

sns.pairplot(train_dataset[['target_count', 'age', 'push_ups']], diag_kind='kde')

train_dataset.describe().transpose()

sns.heatmap(data_workout_exercises.corr(), annot=True, annot_kws={"size": 7})

train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels = train_features.pop('target_count')
test_labels = test_features.pop('target_count')

test_features[:1].shape
 
# **Нормализация**

normalizer = Normalization(axis=-1)

normalizer.adapt(np.array(train_features))

print(normalizer.mean.numpy())
 
# **Создание модели**

linear_model = Sequential([
    normalizer,
    Dense(128, activation='relu'),
    Dropout(0.1),
    Dense(64, activation='relu'),
    Dense(1)
])

linear_model.predict(train_features[:10])

linear_model.layers[1].kernel
 
# **Обучение**

linear_model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='mean_absolute_error')

history = linear_model.fit(
    train_features,
    train_labels,
    epochs=1000,
    batch_size=64,
    # Suppress logging.
    # verbose=0,
    # Calculate validation results on 20% of the training data.
    validation_split = 0.2
)
 
# **Проверка**

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()

def plot_loss(history):
  plt.plot(history.history['loss'], label='loss')
  plt.plot(history.history['val_loss'], label='val_loss')
  plt.ylim([0, 10])
  plt.xlabel('Epoch')
  plt.ylabel('Error [MPG]')
  plt.legend()
  plt.grid(True)

plot_loss(history)

from sklearn.metrics import r2_score
r2_score(test_labels, linear_model.predict(test_features), multioutput='variance_weighted')

print(test_labels[:10], np.round(linear_model.predict(test_features[:10])), test_features[:10])

linear_model.save('saved_neuronet_model/model_6')

linear_model.save('saved_neuronet_model/model_6.h5')