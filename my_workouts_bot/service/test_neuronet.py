from tensorflow import keras

neuronet_model = keras.models.load_model('./neuronet_models/model_4')
[20, 100.0, 15.0, 100.0, 100.0, 22.0, 1, 22, 1]
for i in range(1, 23):
    # id_exercise	push_ups	running_3km	squats	press	pull_ups	id_gender	age	feeling	target_count
    data: list[float] = [
            i, # Косяк с индексами)
            10, # Отжимания
            30, # бег 3 км
            40,# приседания
            40, # пресс
            0, # подтягивания
            2,
            22,
            2
            ]
    predict_target = (i, round(neuronet_model.predict(data,verbose=None)[0][0]))

    print(predict_target)

# print(set([1, 2, 3]) & set([2]))