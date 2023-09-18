def calculate_calories(age, gender, weight_kg, height_cm, body_type, body_fat_percentage_goal, activity_level):

    if gender == "male":
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    
    elif gender == "female":

        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    
    else:

        raise ValueError("Invalid Gender")
    
    if body_type == "ectomorph":
        bmr *= 1.1 

    elif body_type == "endomorph":

        bmr *= 0.9

    if body_fat_percentage_goal < 20:
        bmr *= 1.05

    calories = bmr * activity_level

    return calories

def get_macronutrient_ratios(goal, meals_per_day, gender):

    list1 = []
    if goal == "Muscle Gain":

        list1.append(0.25)
        list1.append(0.35)
        list1.append(0.45)
        list1.append(0.55)
        list1.append(0.15)
        list1.append(0.25)
    
    elif goal == "Weight Loss":

        list1.append(0.25)
        list1.append(0.35)
        list1.append(0.3)
        list1.append(0.4)
        list1.append(0.2)
        list1.append(0.3)

    else:

        list1.append(0.2)
        list1.append(0.3)
        list1.append(0.4)
        list1.append(0.5)
        list1.append(0.2)
        list1.append(0.35)      

    if gender == "male":
        min_vitamin_a = 0.7 / meals_per_day
        max_vitamin_a = 0.9 / meals_per_day
    else:
        min_vitamin_a = 0.6 / meals_per_day
        max_vitamin_a = 0.7 / meals_per_day

    min_fiber_per_meal = 25 / meals_per_day
    max_fiber_per_meal = 35 / meals_per_day

    list1.append(min_vitamin_a)
    list1.append(max_vitamin_a)
    list1.append(min_fiber_per_meal)
    list1.append(max_fiber_per_meal)
    return list1