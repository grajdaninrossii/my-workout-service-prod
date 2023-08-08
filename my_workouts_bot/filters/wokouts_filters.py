from telegram.ext import filters
from keyboards.keyboard_buttons import (
    ChoiceTrainButtons,
    Go2TestTrainButtons,
    TypeTrainButtons,
    SelectFeelingButtons,
    ActionInTrainButtons,
    TrainReviewButtons
)

# Выбор в разделе тренировки
test_train_filter = filters.Regex(ChoiceTrainButtons.test_train)
user_train_filter = filters.Regex(ChoiceTrainButtons.user_train)
go_2_test_train_filter = filters.Regex(Go2TestTrainButtons.yes)

# Выбор типа тренировки
select_feeling_filter = filters.Regex(ChoiceTrainButtons.train)
type_train_filter = filters.Regex(SelectFeelingButtons.bad) | filters.Regex(SelectFeelingButtons.okey) | filters.Regex(SelectFeelingButtons.excellent)
generate_train_filter = filters.Regex(TypeTrainButtons.fast) | filters.Regex(TypeTrainButtons.standart) | filters.Regex(TypeTrainButtons.stretching)

# Тренировка
next_action_in_train_filters = filters.Regex(ActionInTrainButtons.next_exercise) | filters.Regex(ActionInTrainButtons.without_warmup)
train_review_filter = filters.Regex(TrainReviewButtons.optim) | filters.Regex(TrainReviewButtons.hard) | filters.Regex(TrainReviewButtons.easy)