# Supervised learning techniques to forecast Bitcoin price returns  

This is an attempt at algorithmic trading strategy using supervised learning techniques to decide on the optimal position for the next 1hr return of Bitcoin, For data, we utilized various observable market data points, including prices and technical indicators for crypto and non-crypto assets.

## Technologies Used:
- Tensorflow
- Sklearn
- Google Colab
- APIs (Messari and Genesis)


## Model 
We chose a classification model over a regression model in order to focus on the decision of having a position
There are 5 classification fields:  large short, small short, no position, small long; large long
Recurrent Neural Networks (RNN) use output from previous intervals to inform the current interval
We chose a **bidirectional LSTM recurrent neural network** for time series forecasting in TensorFlow

## Contributors:

- Lee Copeland
- Vishnu Kurella
- Ahmad Sadraei
- Ling Zhou

