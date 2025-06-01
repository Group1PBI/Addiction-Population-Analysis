import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
#dataset
df = pd.read_csv('addiction_population_data.csv')
#cleaning
#calculated column
df['drinking_age'] = np.where(df['age']> df['age_started_drinking'],df['age']-df['age_started_drinking'],np.nan)
df['smoking_age'] = np.where(df['age']>df['age_started_smoking'],df['age']-df['age_started_smoking'],np.nan)
df['smoking_level'] = np.where(df['smokes_per_day']<9,'Light Smoker',np.where(df['smokes_per_day']<16,'Moderate Smoker','Heavy Smoker'))
df['drinking_level'] = np.where(df['drinks_per_week']==0,'Non Drinker',np.where(df['drinks_per_week']<8,'Moderate Drinker','Heavy Drinker'))
df['smoking_starting_level'] = np.where(df['age_started_smoking']<18,'Early Start',np.where(df['age_started_smoking']<26,'Adult Start','Late Start'))
df['drinking_starting_level'] = np.where(df['age_started_drinking']<18,'Early Start',np.where(df['age_started_drinking']<26,'Adult Start','Late Start'))
df['bmi_level'] = np.where(df['bmi']<25,'Normal',np.where(df['bmi']<30,'Overweight','Obese'))
#dashboard
tab = st.radio('Select Section',['Cover','KPI','Charts1','Charts2','Charts3','Comments & Insights'])

if tab not in ['Cover','Comments & Insights']:
    st.sidebar.title('Filters')
    smoking_level_fil = ['all'] + df['smoking_level'].unique().tolist()
    drinking_level_fil = ['all'] + df['drinking_level'].unique().tolist()
    drinking_starting_level_fil =['all'] + df['drinking_starting_level'].unique().tolist()
    smoking_starting_level_fil = ['all'] + df['smoking_starting_level'].unique().tolist()
    a=st.sidebar.selectbox(label='Smoking Level',options= smoking_level_fil)
    b=st.sidebar.selectbox(label='Drinking Level',options= drinking_level_fil)
    c=st.sidebar.selectbox(label='Drinking Starting Level',options= drinking_starting_level_fil)
    d=st.sidebar.selectbox(label='Smoking Starting Level',options= smoking_starting_level_fil)
    if a != 'all':
        df = df[df['smoking_level']==a]
    if b != 'all':
        df = df[df['drinking_level']==b]
    if c != 'all':
        df = df[df['drinking_starting_level']==c]
    if d != 'all':
        df = df[df['smoking_starting_level']==d]

if tab == 'Cover':
    st.image('addiction.jpg')
    st.markdown("<h1 style='text-align: center; color: #3C6F98;'>Addiction Population Analysis</h1>", unsafe_allow_html=True)
    st.markdown('''<div style='text-align: right; direction: rtl;'><h3> الغرض من التقرير
    </h3>نناقش فى هذا التقرير تأثير التدخين وشرب الكحوليات بدرجاتهم (مثلا مدخن شره او متوسط او خفيف) على عينة  اشخاص من سن 15 الى 79 سنة بمدد تدخين او شرب كحول من 1 الى 68 سنة رجال وسيدات من 243 دولة حيث ندرس عدد المدخنين والمتعاطيين فى كل دولة ومن كل نوع وتأثير الادمان على التعليم والوظيفة والحياة الاسرية وانجاب الاطفال والسمنة والعلاقة بين طول فترة الادمان والنجاح فى الاقلاع عنه وايضا تأثير الادمان على الصحة العقلية والنوم والرياضة واهمية تأثير الدعم الاجتماعى  واخيرا بعض التعليقات والاستنتاجات  </div>''',unsafe_allow_html=True)
    st.subheader('Disclaimer: The information provided in this text is not factual and is for illustrative purposes only')

if tab == 'KPI':
#measures
    st.metric(label='Total Drinkers',value= df[df['drinks_per_week']!=0]['drinks_per_week'].count())
    st.metric(label='Total Smokers', value= df[df['smokes_per_day']!=0]['smokes_per_day'].count())
    No_Of_Countries = df['country'].nunique()
    st.metric(label='Countries',value=No_Of_Countries)
if tab == 'Charts1':
#visualizations
    d = df.groupby(['drinking_age'])['bmi'].mean().reset_index()
    fig = px.line(d,x='drinking_age',y='bmi',title='Average BMI by Drinking Age')
    d1 = df.groupby(['smoking_age'])['bmi'].mean().reset_index()
    fig1 = px.line(d1, x='smoking_age',y='bmi',title='Average BMI by Smoking Age')
    d2 = df.groupby(['gender'])['smoking_age'].mean().reset_index()
    fig2 = px.pie(d2,names='gender',values='smoking_age',hole=.6,title='Average Smoking Age by Gender')
    d3 = df.groupby(['gender'])['drinking_age'].mean().reset_index()
    fig3 = px.pie(d3,names='gender',values='drinking_age',hole=.6,title='Average Drinking Age by Gender')
    d4 = df.groupby(['education_level'])[['drinking_age','smoking_age']].mean().reset_index()
    fig4 = px.bar(d4,x='education_level',y=['drinking_age','smoking_age'],title='Average of Drinking & Smoking Ages by Education level',text_auto='.2s')
    fig4.update_layout(yaxis={'title':'','showticklabels':False})
    d5 = df.groupby('marital_status')[['drinking_age','smoking_age']].mean().reset_index()
    fig5 = px.bar(d5,x='marital_status',y=['drinking_age','smoking_age'],title='Average of Drinking & Smoking Ages by Marital Status',text_auto='0.2s')
    fig5.update_layout(yaxis={'title':'','showticklabels':False})
    d6 = df.groupby('employment_status')[['drinking_age','smoking_age']].mean().reset_index()
    fig6 = px.bar(d6,x='employment_status',y=['drinking_age','smoking_age'],title='Average of Drinking & Smoking Ages by Employment Status',text_auto='0.2s')
    fig6.update_layout(yaxis= {'title':'','showticklabels':False})
    col1,col2 = st.columns(2)
    with col1:
        for figure in [fig,fig2,fig4,fig6]:
            st.plotly_chart(figure,use_container_width=True)
    with col2:
        for figur in [fig1,fig3,fig5]:
            st.plotly_chart(figur,use_container_width=True)
if tab == 'Charts2':
    d7 = df.groupby('smoking_age')['children_count'].mean().reset_index()
    fig7 = px.line(d7,x='smoking_age',y='children_count',title='Average of Children Count by Smoking Age')
    d8 = df.groupby('drinking_age')['children_count'].mean().reset_index()
    fig8 = px.line(d8,x='drinking_age',y='children_count',title='Average of Children Count by Drinking Age')
    d9 = df.groupby('smoking_age')['attempts_to_quit_smoking'].mean().reset_index()
    fig9 = px.line(d9,x='smoking_age',y='attempts_to_quit_smoking',title='Average of Attempts to Quit Smoking by Smoking Age')
    d10 = df.groupby('drinking_age')['attempts_to_quit_drinking'].mean().reset_index()
    fig10 = px.line(d10,x='drinking_age',y='attempts_to_quit_drinking',title='Average of Attempts to Quit Drinking by Drinking Age')
    d11 = df.groupby('has_health_issues')['drinking_age'].count().reset_index()
    fig11 = px.pie(d11,names='has_health_issues',values='drinking_age',hole=0.6,title='No of Drinkers by Health Issues')
    d12 = df.groupby('has_health_issues')['smoking_age'].count().reset_index()
    fig12 = px.pie(d12,names='has_health_issues',values='smoking_age',hole=0.6,title='No of Smokers by Health Issues')
    d13 = df.groupby('mental_health_status')['drinking_age'].count().reset_index()
    fig13 = px.pie(d13,names='mental_health_status',values='drinking_age',hole=0.6,title='No of Drinkers by Mental Health')
    d14 = df.groupby('mental_health_status')['smoking_age'].count().reset_index()
    fig14 = px.pie(d14,names='mental_health_status',values='smoking_age',hole=0.6,title='No of Smokers by Mental Health')
    col3,col4 = st.columns(2)
    with col3:
        for figure1 in [fig7,fig9,fig11,fig13]:
            st.plotly_chart(figure1,use_container_width=True)
    with col4:
        for figur1 in [fig8,fig10,fig12,fig14]:
            st.plotly_chart(figur1,use_container_width=True)
if tab == 'Charts3':
    d15 = df.groupby('drinking_age')['sleep_hours'].mean().reset_index()
    fig15 = px.line(d15,x='drinking_age',y='sleep_hours',title='Average of Sleep Hours by Drinking Age')
    d16 = df.groupby('smoking_age')['sleep_hours'].mean().reset_index()
    fig16 = px.line(d16,x='smoking_age',y='sleep_hours',title='Average of Sleep Hours by Smoking Age')
    d17 = df.groupby('diet_quality')['smoking_age'].count().reset_index()
    fig17 = px.pie(d17,names='diet_quality',values='smoking_age',title='Total Smokers by Diet Quality',hole=0.6)
    d18 = df.groupby('diet_quality')['drinking_age'].count().reset_index()
    fig18 = px.pie(d18,names='diet_quality',values='drinking_age',title='Total Drinkers by Diet Quality',hole=0.6)
    d19 = df.groupby('exercise_frequency')['smoking_age'].count().reset_index()
    fig19 = px.pie(d19,names='exercise_frequency',values='smoking_age',title='Total Smokers by Exercise',hole=0.6)
    d20 = df.groupby('exercise_frequency')['drinking_age'].count().reset_index()
    fig20 = px.pie(d20,names='exercise_frequency',values='drinking_age',title='Total Drinkers by Exercise',hole=0.6)
    d21 = df.groupby('social_support')['smoking_age'].count().reset_index()
    fig21 = px.pie(d21,names='social_support',values='smoking_age',title='Total Smokers by Social Support',hole=0.6)
    d22 = df.groupby('social_support')['drinking_age'].count().reset_index()
    fig22 = px.pie(d22,names='social_support',values='drinking_age',title='Total Drinkers by Social Support',hole=0.6)
    d23 = df.groupby('therapy_history')['smoking_age'].count().reset_index()
    fig23 = px.pie(d23,names='therapy_history',values='smoking_age',title='Total Smokers by Therapy History',hole=0.6)
    d24 = df.groupby('therapy_history')['drinking_age'].count().reset_index()
    fig24 = px.pie(d24,names='therapy_history',values='drinking_age',title='Total Drinkers by Therapy History',hole=0.6)
    col5,col6 = st.columns(2)
    with col5:
        for figure2 in [fig15,fig17,fig19,fig21,fig23]:
            st.plotly_chart(figure2,use_container_width=True)
    with col6:
        for figur2 in [fig16,fig18,fig20,fig22,fig24]:
            st.plotly_chart(figur2,use_container_width=True)

if tab == 'Comments & Insights':
    st.markdown('''<div style='text-align: right; direction:rtl;'>من خلال النتائج التى توصلنا اليها فى هذا التقرير فى عينة بحث يبلغ عددها 3000 شخص يتضح لنا الاّتى
<h3>يتضح عند فلترة البيانات عند التدخين المفرط و التدخين فى سن مبكر</h3><ol>
<li>ان قيم المتوسط والوسيط متقاربة لذا لايوجد ارقام شاذة </li>
<li>ان الاشخاص فى عينة البيانات معظمهم(حوالى 70%) غير مصابين بالسمنة وذالك لأن التدخين طبيا يؤدى الى فقدان الشهية وتوزيع دهون غير صحى ونمط اكل غير صحى</li>
<li>وان متوسط عمر التدخين للرجال حوالى 41 سنة وللسيدات حوالى 36 سنة</li>
<li>واعلى متوسط عمر تدخين شره من اصحاب الشهادات الابتدائية الذين ابتدأوا التدخين مبكرا بقيمة 42 سنة</li>
<li>وايضا اعلى متوسط عمر تدخين شره من الموظفين الذين ابتدأوا التدخين مبكرا عند 39 سنة ثم يليهم الطلبة ثم الذين لا يعملون</li>
<li>واعلى متوسط عمر تدخين شره من الارامل الذين ابتدأوا التدخين مبكرا عند 35 سنة ثم المتزوجين ثم المنفصلين</li>
<li>واعلى متوسط عمر تدخين فى الصين وباكستان عند 68 سنة</li>
<li>اعلى متوسط عمر تدخين شره من الذين ابتدأوا التدخين مبكرا عند 68 سنة لديه طفل واحد واقل عمر 18 سنة ولديه اكبر عدد اطفال (5)اطفال</li>
<li>اعلى عمر تدخين شره من الذين ابتدأوا التدخين مبكرا لدية اكبر متوسط عدد مرات محولات عن الاقلاع هو 8 محاولات لعمر تدخين 50 سنة</li>
<li>ولدينا متوسط اكبر عدد ساعات نوم 8.3 ساعة لعمر تدخين 56 سنة ويقل عدد الساعات تقريبيا مع انخفاض عمر التدخين</li>
<li>وحوالى 64 % من المدخنين الشرهين الذين ابتدأوا التدخين مبكرا لديهم مشاكل صحية من التدخين وحوالى 37% منهم لديهم مشاكل كبيرة فى الصحة النفسية والعقلية و34% متوسط</li>
<li>و 46% من العينة التى قمنا بالفلترة عليها لدية جودة نظام غذائى جيدة و 27% متوسط و 27% يمارسون الرياضة يوميا و 27% لا يمارسون الرياضة ابدا وحوالى 57 % لهم تاريخ فى المرض النفسى وحوالى 55 % ليس لديهم دعم اجتماعى اصلا او ضعيف </li>
</ol>
من خلال النتائج التى توصلنا اليها فى هذا التقرير فى عينة بحث يبلغ عددها 2980 شخص يتضح لنا الاّتى
<h3>يتضح عند فلترة البيانات عند الشرب المفرط و الشرب فى سن مبكر</h3><ol>
<li>ان الاشخاص فى عينة البيانات معظمهم (حوالى 75%) غير مصابين بالسمنة وذالك لأن الشرب طبيا يؤدى الى فقدان الشهية ومدمنى الكحول لديهم دائما سوء تغذية</li>
<li>وان متوسط عمر الشرب للرجال حوالى 38 سنة وللسيدات حوالى 39 سنة</li>
<li>واعلى متوسط عمر شرب شره من حاملى شهادة الثانوية الذين ابتدأوا الشرب مبكرا عند 42 سنة</li>
<li>وايضا اعلى متوسط عمر شرب شره من الذين يعملون كموظف حر الذين ابتدأوا الشرب مبكرا عند 40 سنة ثم يليهم الذين لا يعملون</li>
<li>واعلى متوسط عمر شرب شره من المتزوجين الذين ابتدأوا الشرب مبكرا عند 38 سنة ثم العزاب</li>
<li>واعلى متوسط عمر شرب فى اوروجواى عند  67 سنة ثم الكونغو</li>
<li>اعلى متوسط عمر شرب شره من الذين ابتدأوا الشرب مبكرا عند  66 سنة لديه 4 اطفال واقل عمر 11 سنة ولديه اكبر عدد اطفال (5)اطفال</li>
<li>اعلى عمر شرب شره من الذين ابتدأوا الشرب مبكرا ولدية اكبر متوسط عدد مرات محولات عن الاقلاع هو 9 محاولات لعمر تدخين 26 سنة</li>
<li>ولدينا متوسط اكبر عدد ساعات نوم 10 ساعات لعمر تدخين 5 سنين ويقل عدد الساعات تقريبيا مع زيادة عمر الشرب</li>
<li>وحوالى 49.5 % من شاربى الكحول الشرهين الذين ابتدأوا الشرب مبكرا لديهم مشاكل صحية من الشرب وحوالى 40% منهم لديهم مشاكل كبيرة فى الصحة النفسية والعقلية و30% متوسط</li>
<li>و 37% من العينة التى قمنا بالفلترة عليها لدية جودة نظام غذائى سئ و 29% متوسط و 26% يمارسون الرياضة يوميا و 28% لا يمارسون الرياضة ابدا وحوالى 67 % لهم تاريخ فى المرض النفسى وحوالى 48 % ليس لديهم دعم اجتماعى اصلا او ضعيف </li>
</ol></div>''',unsafe_allow_html=True)
