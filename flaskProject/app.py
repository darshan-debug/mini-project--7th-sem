from flask import Flask,render_template,request
import joblib
import numpy as np
import os

port = int(os.environ.get('PORT', 5000))

model_knn=joblib.load('knn_model.pkl')
model_nbc=joblib.load('nbc_model.pkl')
model_lr=joblib.load('lr_model.pkl')
model_rf=joblib.load('rf_model.pkl')
model_ab=joblib.load('ab_model.pkl')

x_mean=np.array([4.95849457e+01, 9.00306748e+00, 2.92590845e-02 ,5.89900897e-03, 3.10523832e-01 ,2.36724870e+02 ,1.32352407e+02 ,8.28934639e+01, 2.58019986e+01 ,7.58789523e+01 ,8.19697971e+01])
x_std=np.array([8.57114852, 11.87782862 , 0.16853187  ,0.07657813 , 0.4627081 , 44.32123288, 22.03549643, 11.90944427 , 4.07047223, 12.02375836 ,22.83391071])



app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=["POST","GET"])
def predict():
    #d1=request.values.get("b")
    names=['b','e','f','g','h','j','k','l','m','n','o']
    #print(d1,flush=True)
    int_features=[int(request.values.get(x)) for x in names]
    
    final_features=[np.array(int_features)]
    #print(final_features,flush=True)
    
    pred_knn=model_knn.predict(final_features)
    pred_nbc=model_nbc.predict(final_features)    
    pred_rf=model_rf.predict(final_features)
    pred_ab=model_ab.predict(final_features)

    #normalising input, before passing it to lr_model
    np_final_features=np.array(final_features)
    normalised_np_final_features=(np_final_features-x_mean)/x_std
    pred_lr=model_lr.predict(normalised_np_final_features)
    
    #print(pred_knn,"prediction@@@@@@",flush=True)


    return  ('<h1> Prediction Results:</h1><br><h3>0:no sign of CVD<br> 1:significant possibility of CVD</h3><br>knn model: '+ str(pred_knn[0])+'<br> nbc model: '+str(pred_nbc[0])+'<br> lr model: '+str(pred_lr[0])+'<br> rf model: '+str(pred_rf[0])+'<br> ab model: '+str(pred_ab[0])+"<br><br>final result can be obatained from <br> 1)majority voting of above,or <br>2)weighted avg-giving higher weightage to models with higher accuracy")

if(__name__=="__main__"):
    app.run(host='0.0.0.0', port=port)
