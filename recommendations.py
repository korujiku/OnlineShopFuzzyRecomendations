import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def generate_recommendations(user_data):
    # Пример рекомендаций, основанных на возрастных категориях и интересах
    age = user_data['age']
    interests = user_data['interests']

    # Системы управления для фуззификации возрастов и интересов
    age_range = ctrl.Antecedent(np.arange(0, 81, 1), 'age')
    interest_range = ctrl.Antecedent(np.arange(0, 6, 1), 'interest')

    # Рейтинг возраста (например, дети, подростки, взрослые и пожилые)
    age_range['child'] = fuzz.trimf(age_range.universe, [18, 18, 20])
    age_range['adult'] = fuzz.trimf(age_range.universe, [18, 35, 60])
    age_range['senior'] = fuzz.trimf(age_range.universe, [50, 80, 80])

    # Рейтинг интересов (все это просто для примера)
    interest_range['tech'] = fuzz.trimf(interest_range.universe, [0, 0, 1])
    interest_range['fashion'] = fuzz.trimf(interest_range.universe, [1, 1, 2])
    interest_range['sports'] = fuzz.trimf(interest_range.universe, [2, 2, 3])
    interest_range['music'] = fuzz.trimf(interest_range.universe, [3, 3, 4])
    interest_range['art'] = fuzz.trimf(interest_range.universe, [4, 4, 5])

    # Создание правил
    rule1 = ctrl.Rule(age_range['adult'] & interest_range['tech'], 'tech')
    rule2 = ctrl.Rule(age_range['child'] & interest_range['fashion'], 'fashion')
    rule3 = ctrl.Rule(age_range['senior'] & interest_range['music'], 'music')

    recommendation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    recommender = ctrl.ControlSystemSimulation(recommendation_ctrl)

    # Ввод данных для рекомендаций
    recommender.input['age'] = age
    recommender.input['interest'] = interests  # Для примера, техно-интерес
    recommender.compute()

    return recommender.output['interest']
