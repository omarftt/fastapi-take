import pandas as pd

# Define a function to map dates to hours
def categorize_hour_base(date):
    hour = date.hour
    return hour

# Define a function to map dates to hours
def categorize_hour(date):
    hour = date.hour
    if hour ==23 or 0 <= hour < 5:
        return 'Late Night'
    elif 5 <= hour < 11:
        return 'Morning'
    elif 11 <= hour < 17:
        return 'Afternoon'
    else:
        return 'Evening'

# Función para realizar preprocesamiento
def pre_processing(values):

    df = pd.DataFrame([values], columns=["order_id", "store_id", "to_user_distance","to_user_elevation","total_earning","created_at"])

    ## Limpiar columna de fecha
    df = df[df['created_at'].str.len() <= 20]

    ## Convertir a fecha, sacar hora y categoria de la hora
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['hour_base'] = df['created_at'].apply(categorize_hour_base)
    df['hour_category'] = df['created_at'].apply(categorize_hour)

    ## One hot encoding
    df['hour_category'] = df['hour_category'].map({'Afternoon': 'Afternoon', 'Evening': 'Evening', 'Late Night': 'Late Night', 'Morning': 'Morning'})
    df_encoded = pd.get_dummies(df, columns=['hour_category'], prefix='', prefix_sep='')

    ## Agregando columnas faltantes
    columns = ['to_user_distance','to_user_elevation','total_earning','Afternoon','Evening','Late Night','Morning']
    for col in columns:
        if col not in list(df_encoded.columns):
            df_encoded[col] = 0


    ## Seleccionando columnas de procesamiento
    columns_selected = ['to_user_distance','to_user_elevation','total_earning','Afternoon','Evening','Late Night','Morning']
    df_selected = df_encoded[columns_selected]
    print('here',df_selected)


    # Escalar los valores proporcionados
    # scaled_values = scaler.transform(df_selected)

    return df_selected


def apply_prediction(X,model):
    # Realizar la predicción utilizando el modelo cargado
    prediction = model.predict(X)
    return prediction