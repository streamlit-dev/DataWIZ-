from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def clean_data(df):
    df = df.drop_duplicates()
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna('Unknown')
    return df

def generate_plot(df):
    fig, ax = plt.subplots(figsize=(8,4), facecolor='#0F172A')
    df.isnull().sum().plot(kind='bar', ax=ax, color='#3B82F6')
    ax.set_facecolor('#1E293B')
    ax.tick_params(colors='white')
    ax.set_title('Missing Values After Cleaning', color='white')
    for spine in ax.spines.values():
        spine.set_color('white')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            original_shape = df.shape
            df_clean = clean_data(df)
            plot_url = generate_plot(df_clean)
            return render_template('index.html',
                                 cleaned=True,
                                 shape_before=original_shape,
                                 shape_after=df_clean.shape,
                                 plot_url=plot_url,
                                 data=df_clean.head().to_html(classes='table', index=False))
    return render_template('index.html', cleaned=False)

if __name__ == '__main__':
    app.run(debug=True)